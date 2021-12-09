"""#########################################################################
This script:
1) Combines all of the reponses by all of the subjects into 1 big file
2) Does basic restructuring of data
3) Combines data with qualtrics data
#########################################################################"""
import os
import path
from paths import *
import json
import pandas as pd
from datetime import datetime


all_responses = []

for directory in os.listdir(raw_data_dir):
    print("Processing:", directory)
    for filename in os.listdir(raw_data_dir + directory + "/csv"):
        if filename.startswith("SSS"):
            with open(raw_data_dir + directory + "/csv/" + filename) as json_file:
                data = json.load(json_file)
                for response in data:
                    if (response['name'] == 'choice'):
                        # By a previous coding error, some responses did not store the set that was used to generate them.
                        # Therefore, those are skipped
                        if('set' not in response): continue

                        # Re-format lists as [space] delineated strings ([0,1,2] into "0 1 2")
                        # for sets
                        response['set'] = [str(int) for int in response['set']]
                        response['set'] = ' '.join(response['set'])

                        # for the probe's pitches
                        response['probe_pitches'] = [str(int) for int in response['probe_pitches']]
                        response['probe_pitches'] = ' '.join(response['probe_pitches'])

                        # for the shifted melody's pitches
                        response['shifted_pitches'] = [str(int) for int in response['shifted_pitches']]
                        response['shifted_pitches'] = ' '.join(response['shifted_pitches'])

                        # for the swapped melody's pitches
                        response['swapped_pitches'] = [str(int) for int in response['swapped_pitches']]
                        response['swapped_pitches'] = ' '.join(response['swapped_pitches'])

                        # Store as "option 1" and "option 2" the order in which the subject heard the test melodies
                        response['option_1'] = response['order'][0]
                        response['option_2'] = response['order'][1]

                        # Convert "time" from a string to a datetime object
                        response['time'] = datetime.fromisoformat(response['time'].replace("Z", "+00:00"))

                        # Store the subject's response contextually: shifted, swapped, or neither (rather than 1st, 2nd, or neither)
                        if (response['response'] == "1st"):
                            response['chose'] = response['option_1']
                        elif (response['response'] == "2nd"):
                            response['chose'] = response['option_2']
                        elif (response['response'] == "neither"):
                            response['chose'] = "neither"
                        else:
                            response['chose'] = "Error"

                        # Append response to the list of all responses for all subjects
                        all_responses.append(response)

all_responses = pd.DataFrame.from_dict(all_responses)
all_responses = all_responses.sort_values(by=['subject', 'time','time_elapsed'])

#Combine with qualtrics based on subject ID
qualtrics = pd.read_csv(qualtrics_processed_dir + "qualtrics.csv")
qualtrics = qualtrics.rename(columns={'sub':'subject'})
all_responses = pd.merge(all_responses, qualtrics, on="subject")


# Saving the dataframe to a pickle (better than CSV because it remembers variable object types)
all_responses.to_pickle(processed_dir + processed_data_pickle_filename)

print("Data saved to processed data directory (see paths.py)")
