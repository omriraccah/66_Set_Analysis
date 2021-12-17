"""#########################################################################
This script:
1) merges multiple qualtrics csvs (from multiple surveys)
2) only keeps the relevant task sets (SSS... and SSS2v....)
3) Keeps only the most recent taskset when more than one subject completed the same taskset (e.g., if on Monday SSS0001 
was completed and on Tuesday SSS0001 was completed by another participant. Only the Tuesday data will be saved.)
4) Saves the cleaned up and merged file (qualtrics.csv) to the designated folder (see paths.py)
#########################################################################"""

from paths import *
import pandas as pd
import os

data_frames = []
# loop through survey files and store all completed set names
for filename in os.listdir(qualtrics_dir):
    if filename.endswith(".csv"):
        # load survey data
        curr_survey = pd.read_csv(qualtrics_dir + filename)

        # drop rows 1 and 2 (they contain redundant qualtrics headers)
        curr_survey = curr_survey.iloc[2:, :]

        #append to main frame
        data_frames.append(curr_survey)

# The qualtrics files contain all the subjects for the 66-set study (SSS and SSS2v), the likert-scale study (SSSQ) and
# other unrelated studies (OVS and NOVS). The following lines filter only the relevant sets.
qualtrics = pd.concat(data_frames, sort=True, ignore_index=True)

# We only keep sets that have a prefix of SSS + number (e.g., SSS0001, but also SSS2v0001)
qualtrics = qualtrics.loc[lambda x: x['sub'].str.contains('SSS\d', regex=True)]  # regex for SSS+digit

# Some sets have been taken by more than one participant. We only keep the most recent one.
# We sort by sub (task-set) and by 'EndDate', and then we only keep that first row for each 'sub'
qualtrics = qualtrics.sort_values(by=['sub', 'EndDate'], ascending=False).groupby('sub', as_index=False).first()

qualtrics = qualtrics.rename(
    columns={
        'sub': 'subject',
        'Q1': 'subject_age',
        'Q2': 'subject_gender',
        'Q3': 'Would you consider yourself a musical person? (0-10)',
        'Q4': 'How many years of formal musical training do you have?',
        'Q5': 'Do you play any instruments (with or without formal training)?',
        'Q6': 'Which instruments do you play (if any)?',
        'Q8_1': 'I understood the instructions of the task',
        'Q8_2': 'I found the task difficult',
        'Q9': 'What general strategy (if any) did you use to judge the similarity across the melodies?',
        'Q10': 'Did this strategy change throughout the task?',
        'Q11': 'How did you listen to the task?',
        'Q13': 'If you have had musical training, how old were you during this period (i.e., age-range)?',
        'Q14': 'What is your first language?',
        'Q15': 'Did you notice any change in the music? Elaborate',
        'Q16': 'How did you arrive at this experiment?',
        'Q18': 'What is your first language (if other)?',
        'Q19': 'Did you notice any particular changes in the music? In other words, did you base your discriminations on specific features of the melodies?',
        'Q20': 'How did your strategy change throughout the task?',
    })

qualtrics = qualtrics.drop([
    'Q3_NPS_GROUP',
    'Q17',
    'DistributionChannel',
    'Duration (in seconds)',
    'EndDate',
    'ExternalReference',
    'Finished',
    'IPAddress',
    'LocationLatitude',
    'LocationLongitude',
    'Progress',
    'RecipientEmail',
    'RecipientFirstName',
    'RecipientLastName',
    'ResponseId',
    'StartDate',
    'Status',
    'UserLanguage',
    "Q9 - Parent Topics",
    "Q9 - Topics",
], axis=1)


# Save the relevant data to file
qualtrics.to_csv(qualtrics_processed_dir + "qualtrics.csv")
