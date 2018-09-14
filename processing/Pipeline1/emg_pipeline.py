import pandas as pd
import numpy as np

# pipe line stuff 
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import StandardScaler

# rest zone processing
from rest_zones import cut_rest_zones



# defining transformer for emg data 
class ProcessEMGData(BaseEstimator, TransformerMixin):

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):

        # transforming the data to 2D np array 
        data_mat = np.array(X)
        data_mat = np.transpose(data_mat)

        # checking input array dimensions
        if(data_mat.shape[1] != 50 or data_mat.shape[0] != 8):
            raise ValueError('Invalid input array shape')

        # creating np 2d array full of rms values (interval = 10)
        # rows -> 5 rms vals for 1 emg 
        rms_mat = np.empty((8, 5))
        for i in range(8):
            mat_index = 0
            for y in range(0, 50, 10):
                temp_array = data_mat[i, y:y+10]
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
