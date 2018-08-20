import pandas as pd
import numpy as np
import json

# pipe line stuff 
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import StandardScaler


# return list of 50 sample sets
def fetch_data_from_file(file_name): 

    # pulling the json from the file
    training_txt = open(file_name, 'r').read()
    training_json = json.loads(training_txt)
    training_data = training_json["emg"]["data"]

    # getting 2d np array of data
    data_mat = np.array(training_data)
    num_samples = len(training_data)

    training_sets = []
    for i in range(0, num_samples//50): 
        training_sets.append(data_mat[0+50*i:50+50*i])

    return training_sets



# defining transformer for emg data 
class ProcessEMGData(BaseEstimator, TransformerMixin):

    def fit(self, X, y=None): 
        return self

    def transform(self, X, y=None):

        # transforming the data to 2D np array 
        data_mat = np.array(X)

        # creating np 2d array full of rms values (interval = 10)
        # rows -> 5 rms vals for 1 emg 
        rms_mat = np.empty((8, 5))
        for i in range(8):
            mat_index = 0
            for y in range(0, 50, 10):
                temp_array = data_mat[y:y+10, i]
                curr_rms = np.sqrt(np.mean(temp_array**2))
                rms_mat[i][mat_index] = curr_rms
                mat_index += 1

        return rms_mat


# defining processing pipe line
def get_EMG_pipeline(): 
     return Pipeline([
        ('emg_process', ProcessEMGData()),
        ('std_scaler', StandardScaler())
    ])
