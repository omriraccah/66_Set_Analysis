"""#########################################################################
This script:
1) Combines all the responses by all the subjects into 1 big file
2) Does basic restructuring of data
3) Combines data with qualtrics data
#########################################################################"""

#TODO: Exclude trials where not all 5 set notes appear (or entire subject)

from paths import *
import json
import pandas as pd
from datetime import datetime


all_responses = []  # Will hold all the responses in one frame

for directory in os.listdir(raw_data_dir):  # Iterating through each subject directory
    print("Processing:", directory)
    for filename in os.listdir(raw_data_dir + directory + "/csv"):  # looks in the /csv directory of each subject
        if filename.startswith("SSS"):  # Only looks at files that start with SSS
            with open(raw_data_dir + directory + "/csv/" + filename) as json_file:
                data = json.load(json_file)  # Loads the data as JSON.
                for response in data:  # each line in the JSON is a trial
                    # Other data is stored in the JSON, but we only care about the "choice" data which is the choice
                    # the subject made upon hearing the melodies
                    if (response['name'] == 'choice'):
                        # By a previous coding error, some responses did not store the set that was used to generate
                        # them. Therefore, those are skipped
                        if('set' not in response):
                            print("Skipping response from {}, because its structure is malformed.".format(directory))
                            continue

                        # Re-format lists as [space] delineated strings ([0,1,2] into "0 1 2" for sets)
                        # Addressing the set as a string rather than as a list makes things easier down the line.
                        response['set'] = [str(int) for int in response['set']]
                        response['set'] = ' '.join(response['set'])

                        # The same reasoning applied to the probe's pitches
                        response['probe_pitches'] = [str(int) for int in response['probe_pitches']]
                        response['probe_pitches'] = ' '.join(response['probe_pitches'])

                        # Same for the shifted melody's pitches
                        response['shifted_pitches'] = [str(int) for int in response['shifted_pitches']]
                        response['shifted_pitches'] = ' '.join(response['shifted_pitches'])

                        # Same for the swapped melody's pitches
                        response['swapped_pitches'] = [str(int) for int in response['swapped_pitches']]
                        response['swapped_pitches'] = ' '.join(response['swapped_pitches'])

                        # Store as "option 1" and "option 2" the order in which the subject heard the test melodies
                        response['option_1'] = response['order'][0]
                        response['option_2'] = response['order'][1]

                        # Convert "time" from a string to a datetime object Note: It appears that the time entry was
                        # not stored correctly (within a subject the time appears to not change), and to calculate
                        # RTs we'll use the designated RT field or the time_elapsed field.
                        response['time'] = datetime.fromisoformat(response['time'].replace("Z", "+00:00"))

                        # Store the subject's response contextually: shifted, swapped, or neither (rather than 1st, 2nd, or neither)
                        if response['response'] == "1st":
                            response['chose'] = response['option_1']
                        elif response['response'] == "2nd":
                            response['chose'] = response['option_2']
                        elif response['response'] == "neither":
                            response['chose'] = "neither"
                        # There shouldn't be any other options, so if there is somehow an additional one,
                        # it requires some investigation.
                        else:
                            response['chose'] = "Error"

                        # Append each response to the list of all responses for all subjects
                        all_responses.append(response)


# Once all responses have been appended, reformat the list of responses into a pd Dataframe.
all_responses = pd.DataFrame.from_dict(all_responses)
# To ensure the order of the dataframe we sort the values first by subject (so a subject's responses are appearing in
# a row), Then within that subject we sort by time, and then by time elapsed (the 'time' parameter can probably be
# omitted).
all_responses = all_responses.sort_values(by=['subject', 'time','time_elapsed'])

# Combine with qualtrics based on subject ID
qualtrics = pd.read_csv(qualtrics_processed_dir + "qualtrics.csv")
qualtrics = qualtrics.rename(columns={'sub':'subject'}) # Renames the column in the qualtrics df from 'sub' to 'subject'
# on="subject" means that the 'subject' on either dataframe corresponded to the same thing and therefore that column
# should be the basis for merging.
all_responses = pd.merge(all_responses, qualtrics, on="subject")


# Saving the dataframe to a pickle (better than CSV because it remembers variable object types)
all_responses.to_pickle(processed_dir + processed_data_pickle_filename)

print("Data saved to processed data directory (see paths.py)")
