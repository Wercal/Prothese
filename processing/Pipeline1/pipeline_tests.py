import numpy as np

# importing piepline utilities
from pipeline_buffer import maintain_pipeline_buffer, init_redis_session, reset_pipeline_buff_flags

# iporting threading utilities
from multiprocessing import Process
from multiprocessing.managers import BaseManager


# testing the maintenance of the pipeline buffer by "maintain_pipeline_buffer" a threaded function
def maintain_pipeline_buffer_test():

    # creating a redis connection
    r_server = init_redis_session()

    # launching the buffer maintenance as a subprocess
    buffer_maintenance_p = Process(target=maintain_pipeline_buffer)
    buffer_maintenance_p.start()

    while(r_server.get("buffer_maintained") == "1"):
        if(r_server.get("buffer_ready") == "1"):
            reset_pipeline_buff_flags(r_server)
    
    buffer_maintenance_p.join()
    