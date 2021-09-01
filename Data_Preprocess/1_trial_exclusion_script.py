'''
This code goes through the data and marks excluded trials.
NOTE: This code runs purposefully inefficiently as to increase its clarity and modularity.
'''


'''IMPORTS'''
import os
import json

'''DEFAULTS'''
raw_data_folder = '../Raw_Data' #Set folder of all raw data
post_exclusion_folder = '../Post_Trial_Exclusion_Data'

'''MAIN CODE'''
task_sets = os.listdir(raw_data_folder)

#This will contain all of the subjects and their data
subjects = []


#This block loads subjects (one by one) into the subjects list (above)
for task_set in task_sets:
    subject = {
        'task_set': task_set,

        #gets all the json file paths that contain the subject's responses
        'data_files_paths':  [raw_data_folder + '/' + task_set + '/csv/' + file for file in os.listdir(raw_data_folder + '/' + task_set + '/csv') if (file.startswith('SSS'))],

        #will get populated with the subject's responses.
        'data': [],

        #Setting all subjects to NOT be excluded, but this may change later if they don't pass certain criteria
        'excluded':False
    }

    #populates the JSON data into subject['data']
    for path in subject['data_files_paths']:
        with open(path) as jsonfile:
            block_data = json.load(jsonfile)
            subject['data'].append(block_data)

    subjects.append(subject)
print("loaded all subjects into 'subjects'")

#Runs through all subjects and adds the sona ID at the subject level
for subject in subjects:
    #looks at the first trial in the first block, that contains the subjects SONA id. It copies it from there to the subject level
    if('sona' in subject['data'][0][0]):
        subject['sona'] = subject['data'][0][0]['sona']
    else:
        subject['sona'] = "Unknown"

#Runs through all subjects, and all trials, and marks all trials as not excluded
#However, this may change later if they don't pass certain criteria
for subject in subjects:
    for block in subject['data']:
        for trial in block:
            # only look at 'choice' trials. Anything else you can skip.
            if (trial['name'] != "choice"): continue

            # Setting all trials to NOT be excluded, but this may change later if they don't pass certain criteria
            trial['excluded']= False
print("'included' all trials")



#Runs through all subjects, and all trials, and excludes the trial if the subject clicked 'neither'
for subject in subjects:
    for block in subject['data']:
        for trial in block:
            # only look at 'choice' trials. Anything else you can skip.
            if (trial['name'] != "choice"): continue

            if(trial['response']=='neither'): trial['excluded']=True

print("Marked 'neither' trials as excluded.")


#Runs through all subjects, and all trials, and excludes the trial if not all 5 notes of the set were included in the probe
for subject in subjects:
    for block in subject['data']:
        for trial in block:
            # only look at 'choice' trials. Anything else you can skip.
            if (trial['name'] != "choice"): continue

            probe = trial['probe_pitches']
            transposition = min(probe)
            unique_pitches = list(set(sorted([(note-transposition)%12 for note in probe])))
            if(len(unique_pitches)<5):
                trial['excluded'] = True

print("Marked trials with probes that don't contain all 5 notes as excluded.")

#Saves the pre-proccesed data as JSON files in Post_Trial_Exclusion_Data
for subject in subjects:
    if(not os.path.isdir(post_exclusion_folder)):
        os.mkdir(post_exclusion_folder)
    task_set = subject['task_set']
    with open(post_exclusion_folder + "/" + task_set  + ".json", "w") as outfile:
        json.dump(subject, outfile)
print("Saved data with excluded trials marked")









