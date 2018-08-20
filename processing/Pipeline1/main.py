from EMG_pipeline import get_EMG_pipeline, fetch_data_from_file

# fetching pipe line
emg_processor = get_EMG_pipeline()

# fetching training samples from file
training_file_name = "Hand_close_1_0.json"
training_samples = fetch_data_from_file(training_file_name)

for i in range(len(training_samples)): 
    processed_vals = emg_processor.fit_transform(training_samples[i])
    print(processed_vals)
    print("\n")