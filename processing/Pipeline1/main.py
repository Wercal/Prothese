# importing piepline utilities
from emg_pipeline import get_EMG_pipeline
from pipeline_buffer import fetch_data_from_file

# importing pipeline tests
from pipeline_tests import maintain_pipeline_buffer_test

'''
# fetching pipe line
emg_processor = get_EMG_pipeline()
# fetching training samples from file
training_file_name = "testing_data/Hand_open_4_0.json"
training_samples = fetch_data_from_file(training_file_name)
# testing the pipeline
processed_vals = emg_processor.fit_transform(training_samples[0])
'''

# testing the maintenance of the pipeline buffer
maintain_pipeline_buffer_test()