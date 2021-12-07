"""#########################################################################
This script:
Reads the processed qualtrics CSV, and based on its entries downloads the relevant raw data into the raw data folder

Note: for this to work, the AWS CLI must be installed, otherwise the downloading must be done manually.
Also Note: This may take a long time. (hours)
#########################################################################"""

from paths import *
import os
import pandas as pd

qual = pd.read_csv(qualtrics_processed_dir + "qualtrics.csv")  # path of qualtrics survey with all relevant responses
subjects = qual['sub'].tolist()[2:]  # extract all subjects from qualtrics data

for SubjectID in subjects: #download each subject's task set
    print("Downloading data for subject: ", SubjectID)
    os.system('aws s3 cp s3://cadseg/{0} {1}{0} --exclude="*audio*" --exclude="*images*" --recursive'
              .format(SubjectID, raw_data_dir))