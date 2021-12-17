import os
ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) # This is Project Root
DATA_DIR = ROOT_DIR + "/Data/"
qualtrics_dir = ROOT_DIR + '/Data/0_Raw_Qualtrics_CSVs/'
qualtrics_processed_dir = ROOT_DIR + '/Data/1_Consolidated_Qualtrics_CSV/'
raw_data_dir = ROOT_DIR + '/Data/2_Raw_data/'
processed_dir = ROOT_DIR + '/Data/3_Processed_Data/'

processed_data_pickle_filename = "single_trial_results.pickle"
processed_data_csv_filename = "single_trial_results-DEMO.csv"
