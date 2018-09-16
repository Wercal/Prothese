import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt

# utilities to remove rest zones
from rest_zones import cut_rest_zones, ActiveData

# importing myo bluetooth utilities
from time import sleep, time
import myo_raw
import sys

# importing multi processing utilities 
from multiprocessing import Process
import pickle
import redis

# defining the pipeline buffer size error
pipeline_buff_size = 25

# defining the amount of output sensors on the myo
n_incoming_sensors = 8

# defining inter-process communications
redis_db_id = 0 

# global containers (each process will fork these containers)
raw_incoming_data = np.zeros((8, 0))
active_data_store = []
data_store_max_size = 5000

# global tuple for pose (enum -> int) conversions

# defining custom bluetooth exception (when connection fails)
class BluetoothFailedConnection(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)



# creating necessary variables for redis session
def init_redis_variables(r_server):

    # defining buffer maintenance flags
    r_server.set("buffer_ready", "0")
    r_server.set("last_seg", "0")
    r_server.set("buffer_maintained", "1")
    r_server.set("incoming_data", "1")
    r_server.set("raw_data_ready", "0")
    r_server.set("reset_buff_size", "0")
    r_server.set("pose_data_ready", "0")

    # defining shared buffer containers
    r_server.set("raw_data", "")
    r_server.set("pipeline_buff", "")
    r_server.set("myo_pose", "")

    return r_server



# resets the buffer maintenace flag after data is read in main process 
def reset_pipeline_buff_flags(r_server):
    r_server.set("buffer_ready", "0")
    r_server.set("last_seg", "0")
    r_server.set("reset_buff_size", "1")



# creates a connected myo bluetooth object
# input : redis server connection
def create_myo_connection(r_server):

    # creating a connection object
    connection_success = False
    n_tries = 20
    while(not connection_success):
        try:
            m = myo_raw.MyoRaw(sys.argv[1] if len(sys.argv) >= 2 else None)
            connection_success = True
        except ValueError:
            print("Myo dongle not found")
            n_tries -= 1
            sleep(1)
            if(n_tries == 0):
                raise BluetoothFailedConnection("Bluetooth connection failed") 
        
    # defining the emg raw value handler
    def proc_emg(emg, moving, times=[]):

        global raw_incoming_data
        
        # appending incoming data to the raw data buffer
        emg_list = list(emg)
        raw_incoming_data = np.c_[raw_incoming_data, emg_list]

        # when raw data buffer reaches max size, transfering it to db
        if(raw_incoming_data.shape[1] == pipeline_buff_size): 
            # parent process is ready for transfer
            if(r_server.get("raw_data_ready") == "0"):
                r_server.set("raw_data", json.dumps(raw_incoming_data.tolist()))
                raw_incoming_data = np.zeros((n_incoming_sensors, 0))
                r_server.set("raw_data_ready", "1")
            # making room for newer data, while waiting for parent
            else : raw_incoming_data = raw_incoming_data[ : , 5 : ]

    # defining the pose handler
    def proc_pose(pose):
        r_server.set("pose_data_ready", "1")
        r_server.set("myo_pose", str(pose.value))

    # attaching the handlers
    m.add_emg_handler(proc_emg)
    m.add_pose_handler(proc_pose)
    
    m.connect()
    print("myo connected") 
   
    return m



# extracts data from the a myo instance and fills the raw_data buffer
# this function is ment to be run a seperate process
# input : redis connection pool
def collect_myo_data(conn_pool):

    # creating redis for shared buffer objects
    r_server = redis.StrictRedis(connection_pool=conn_pool)

    # obtaining a connection to the myo
    try:
        myo_connection = create_myo_connection(r_server)
    except BluetoothFailedConnection :
        r_server.set("incoming_data", "0")
        print("Buffer maintenance thread aborted, failed to connect to myo")
        return 

    # pulling data from the myo
    try :
        while(True): myo_connection.run(1)
    except :
        myo_connection.disconnect()
        r_server.set("incoming_data", "0")
        print("Buffer maintenance thread aborted, error while reading from myo")
        print("myo disconnected")
        return



# maintains the pipeline buffer, which contains data ready for further pipelines
# this function is ment to be run a a seperate process
# input : connection pool for redis
def maintain_pipeline_buffer(conn_pool):

    global active_data_store, data_store_max_size

    # local version of the pipeline buffer
    pipeline_buff = np.empty((n_incoming_sensors, pipeline_buff_size))
    buff_content_size = 0

    # creating redis connection for current process
    r_server = redis.StrictRedis(connection_pool=conn_pool)

    # launching data collecting thread
    data_collection_p = Process(target=collect_myo_data, args=(conn_pool,))
    data_collection_p.start()

    # as long as the program is receiving myo data
    while(r_server.get("incoming_data") == "1"):

        # turning a full raw data buffer to an active data entry
        if(r_server.get("raw_data_ready") == "1"):
            new_raw_data = np.array(json.loads(r_server.get("raw_data")))
            active_data_store.append(cut_rest_zones(new_raw_data))
            r_server.set("raw_data", "")
            r_server.set("raw_data_ready", "0")
            
        # data is availabe to be placed in the pipeline buffer
        if(len(active_data_store) > 0):
            
            # data is not currently available to parent process
            if(r_server.get("buffer_ready") == "0"):

                # making sure pipeline buffer has a valid size
                if(r_server.get("reset_buff_size") == "1"):
                    buff_content_size = 0
                    r_server.set("reset_buff_size", "0")
            
                # adding clensed data to the pipeline buffer
                last_seg_flag, active_data_inst, buff_content_size = fill_pipeline_buff(active_data_store[0], pipeline_buff, buff_content_size)

                # pipeline buffer is full or movement ended
                if((buff_content_size == pipeline_buff_size) or last_seg_flag):
                    r_server.set("pipeline_buff", json.dumps(pipeline_buff.tolist()))
                    if(last_seg_flag):
                        r_server.set("last_seg", "1")
                    r_server.set("buffer_ready", "1")
                    
                # updating the active data piece in the storage
                if(active_data_inst is None):
                    del active_data_store[0]
                else: 
                    active_data_store[0] = active_data_inst

        # maintaining the data store size (safety)
        if(len(active_data_store) > data_store_max_size):
            active_data_store.pop()

    # marking the end of buffer maintenance
    r_server.set("buffer_maintained", "0")
    data_collection_p.join()

    
        
# function to add data to the pipeline buffer
# modifies :
# pipeline buffer (which is passed by reference)
# returns :
# clensed data : none -> remove the element from storage, not none -> replace the element in storage 
# true/false : true -> last buffer fill for current movement, false -> current movement is still under way
def fill_pipeline_buff(clensed_data, pipeline_buff, buff_content_size):

    last_buffer_fill = False
    last_seg_selected = False

    new_content_size = 0

    # getting movement data from the clensed data
    if(not clensed_data.rest_zone_detected):
        new_data = clensed_data.whole_data
    else :
        if(clensed_data.curr_mov_last_seg is not None):
            new_data = clensed_data.curr_mov_last_seg
            last_seg_selected = True
        elif(clensed_data.next_mov_first_seg is not None): 
            new_data = clensed_data.next_mov_first_seg

    # getting space information
    new_data_size = new_data.shape[1]
    available_buff_space = pipeline_buff_size - buff_content_size

    # if the clensed data can all fit in the buffer
    if(new_data_size <= available_buff_space):
        pipeline_buff[ : , buff_content_size : (buff_content_size + new_data_size)] = new_data[ : , : ]
        new_data = None
        new_content_size = buff_content_size + new_data_size
        # handling case where data is last segment for current movement
        if(last_seg_selected):
            last_buffer_fill = True

    # if the new data size exceeds remainning buffer space
    elif(new_data_size > available_buff_space):
        pipeline_buff[ : , buff_content_size : ] = new_data[ : , : available_buff_space]
        new_data = new_data[ : , available_buff_space : ]
        new_content_size = pipeline_buff_size

    # reattaching the movement data to the clensed data object
    if(not clensed_data.rest_zone_detected):
        clensed_data.whole_data = new_data
    else :
        if(clensed_data.curr_mov_last_seg is not None):
            clensed_data.curr_mov_last_seg = new_data
        elif(clensed_data.next_mov_first_seg is not None): 
            clensed_data.next_mov_first_seg = new_data

    # checking if the clensed data is exhausted
    if(clensed_data.whole_data is None and clensed_data.curr_mov_last_seg is None and clensed_data.next_mov_first_seg is None):
        clensed_data = None

    return last_buffer_fill, clensed_data, new_content_size   



# inputs : 
#   target .json file name for extraction
# returns
#   list of (pipeline_buff_size) sample sets from a data file
def fetch_data_from_file(file_name): 

    # defining the list size
    m_size = pipeline_buff_size

    # pulling the json from the file
    training_txt = open(file_name, 'r').read()
    training_json = json.loads(training_txt)
    training_data = training_json["emg"]["data"]

    # getting 2d np array of data
    data_mat = np.array(training_data)
    num_samples = len(training_data)

    training_sets = []
    for i in range(0, num_samples//m_size): 
        training_sets.append(data_mat[0 + m_size*i : m_size + m_size*i])

    return training_sets
