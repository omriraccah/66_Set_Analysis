################################################
# This script matches qualtrics IDs to data files in order to
# identify subjects who completed the task + survey (i.e. our cohort)
# These subjects will be moved from All_Sets_Downloaded folder to Raw_Data #
################################################

import pandas as pd
import seaborn as sns
import shutil, os
import matplotlib.pyplot as plt

# Set set path: path to all the sets (completed and uncompleted
set_path = '/Users/omriraccah/Documents/Projects/Musical_Scales_Project/66_Set_Analysis/Data_Preprocess/' \
          'All_Sets_Downloaded/'

# Set survey path: path to survey files
survey_path = '/Users/omriraccah/Documents/Projects/Musical_Scales_Project/66_Set_Analysis/Survey_Data/'

# Raw data path: path to store completed sets (i.e. cohort data)
data_path = '/Users/omriraccah/Documents/Projects/Musical_Scales_Project/66_Set_Analysis/Raw_Data/'

################################################
# Loop through survey files and cross reference
# who completed the task -> move to Raw_Data folder
################################################

# store all sub IDs to look for overlap
All_completed_sets = []

# Get all downloaded sets (possibly not completed)
downloaded_sets = os.listdir(set_path)
downloaded_sets = pd.Series(downloaded_sets)

# get on 'SSS*' prefix and not 'SSSQ*', which is the likert scale response
SSSQ_sets = downloaded_sets.str.contains('SSSQ', case=True, regex=True)
downloaded_sets = downloaded_sets[~SSSQ_sets]

# remove non-valid sona IDs (non-numerical entries; e.g. Debug, Levannah, etc.)
invalid_sona = filter(str.isdigit, downloaded_sets)
downloaded_sets = downloaded_sets[~invalid_sona]



# loop through survey files and store all completed set namesS
for filename in os.listdir(survey_path):
    if filename.endswith(".csv"):
        print(os.path.join(survey_path, filename))

        # load survey data
        curr_survey = pd.read_csv(survey_path + filename)
        # grab set names
        completed_sets = curr_survey['sub']
        All_completed_sets.extend(completed_sets)

All_completed_sets = pd.DataFrame(All_completed_sets)
All_completed_sets = All_completed_sets.drop_duplicates(keep=False)[0]

# get intersection between downloaded and completed sets
overlap_filesToMove = pd.Series(list(set(All_completed_sets).intersection(list(set(downloaded_sets)))))
# copy directory from all sets to Raw_Data
for f in overlap_filesToMove:
    shutil.copytree(set_path + f, data_path + f)

