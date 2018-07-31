import tensorflow as tf
import numpy as np
import json


""" Array from json data file, credit to Makuchamcham for his Pewter module"""
def json_to_array(filepath, experiment):
    with open(filepath+experiment) as dataf:
        myo_data = json.load(dataf)

    raw_vec_list = []
    n_entrys = len( myo_data["emg"]["data"] )
    for entry in range(0, n_entrys):
        vector = \
        myo_data["emg"]["data"][entry].append(int(myo_data["emg"]["timestamps"][entry]))
        raw_vec_list.append(vector)

    return np.array(raw_vec_list)



""" Clean timestamps to make them more linear """
def clean_time_stamps(array):
    timestamp = 8
    cp_array = array

    array_len = len(array)
    last_time = array[0][timestamp]
    for entry in range(1, array_len):
        cur_time = cp_array[entry][timestamp]
        if entry < array_len-1:
            next_time = cp_array[entry+1][timestamp]

        if cur_time == last_time:
            #add the difference the next and the last
            cur_time += int((last_time + next_time)/2)
            cp_array[entry][timestamp] = cur_time

