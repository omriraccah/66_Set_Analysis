################################################
# This script analyzes the raw subject data to
# compute mean(bias), RT, % neither, within- and
# across-subjects for each of the 66 sets
# (i.e. processed data structure)
################################################

import pandas as pd
import seaborn as sns
import shutil, os
import matplotlib.pyplot as plt
import statistics as stat
import collections
import json
import csv
import re

'''Loads a JSON file'''
def get_json(path):
    json_file = open(path)
    json_file = json_file.read()
    return json.loads(json_file)

################################################
# Initialize relevant paths
################################################
# 2_Raw_data data path: path to store completed sets (i.e. cohort data)
data_path = '/Users/omriraccah/Documents/Projects/Musical_Scales_Project/66_Set_Analysis/2_Raw_data/'

################################################
# Loop through subjects in 2_Raw_data folder
################################################
for filename in os.listdir(data_path):
    if filename.endswith(".json"):
        print('subject: ' + os.path.join(data_path, filename))







################################################
# Exclusion criteria application
################################################
