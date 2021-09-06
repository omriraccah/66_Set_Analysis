'''
This code goes through the data and marks excluded trials.
NOTE: This code runs purposefully inefficiently as to increase its clarity and modularity.
'''

'''IMPORTS'''
import os
import json

'''DEFAULTS'''
raw_data_folder = '../Raw_Data'  # Set folder of all raw data
post_exclusion_folder = '../Post_Exclusion_Data'

min_responses_per_set = 10

''' Counters '''
total_trials = 0
excluded_trials = 0
total_sets = 0
excluded_sets = 0
total_subjects = 0
excluded_subjects = 0

per_set_data = {}

'''MAIN CODE'''
task_sets = os.listdir(raw_data_folder)


def load_task_sets():
    """ This will contain all of the subjects and their data """
    subjects = []
    # This block loads subjects (one by one) into the subjects list (above)
    for task_set in task_sets:
        subject = {
            'task_set': task_set,

            # gets all the json file paths that contain the subject's responses
            'data_files_paths': [raw_data_folder + '/' + task_set + '/csv/' + file for file in
                                 os.listdir(raw_data_folder + '/' + task_set + '/csv') if (file.startswith('SSS'))],

            # will get populated with the subject's responses.
            'data': [],

            # Setting all subjects to NOT be excluded, but this may change later if they don't pass certain criteria
            'excluded': False
        }

        # populates the JSON data into subject['data']
        for path in subject['data_files_paths']:
            with open(path) as jsonfile:
                block_data = json.load(jsonfile)
                subject['data'].append(block_data)

        subjects.append(subject)

    # Runs through all subjects and adds the sona ID at the subject level
    for subject in subjects:
        # looks at the first trial in the first block, that contains the subjects SONA id. It copies it from there to the subject level
        if ('sona' in subject['data'][0][0]):
            subject['sona'] = subject['data'][0][0]['sona']
        else:
            subject['sona'] = "Unknown"

    # Runs through all subjects, and all trials, and marks all trials as not excluded
    # However, this may change later if they don't pass certain criteria
    for subject in subjects:
        for block in subject['data']:
            for trial in block:
                # Setting all trials to NOT be excluded, but this may change later if they don't pass certain criteria
                trial['excluded'] = False

    print("loaded all subjects into 'subjects' pre-exclusion")
    return subjects


'''Trial Related Functions'''


def exclude_neither_trials(subjects):
    """ Runs through all subjects, and all trials, and excludes the trial if the subject clicked 'neither' """
    global total_trials,excluded_trials

    for subject in subjects:
        for block in subject['data']:
            for trial in block:
                # If already excluded, continue
                if (trial['excluded']): continue

                total_trials+=1

                if (trial['response'] == 'neither'):
                    trial['excluded'] = True
                    excluded_trials+=1

    print("Marked 'neither' trials as excluded.")
    return subjects


def exclude_incomplete_trials(subjects):
    """ Runs through all subjects, and all trials, and excludes the trial if not all 5 notes of the"""
    global total_trials, excluded_trials
    # set were included in the probe
    for subject in subjects:
        for block in subject['data']:
            for trial in block:
                # If already excluded, continue.
                if (trial['excluded']): continue

                total_trials+=1

                probe = trial['probe_pitches']
                transposition = min(probe)
                unique_pitches = list(set(sorted([(note - transposition) % 12 for note in probe])))
                if (len(unique_pitches) < 5):
                    trial['excluded'] = True
                    excluded_trials+=1
    print("Marked trials with probes that don't contain all 5 notes as excluded.")
    return subjects

def exclude_decoy_trials(subjects):
    for subject in subjects:
        for block in subject['data']:
            for trial in block:
                # If already excluded, continue.
                if (trial['excluded']): continue


                # exclude decoy trials
                if(trial['has_decoy']):
                    trial['excluded'] = True
    print("Excluded decoy trials.")
    return subjects

def exclude_irrelevant_JSON_trials(subjects, keep='choice'):
    """ Runs through all subjects, and all trials, and excludes trials that are of the type specified in 'keep' """
    for subject in subjects:
        for block in subject['data']:
            for trial in block:
                # If already excluded, continue.
                if (trial['excluded']): continue

                if (trial['name'] != keep): trial['excluded'] = True

    print("Excluded irrelevant JSON trials.")
    return subjects

'''Set Related Functions'''

def restructure_data_by_set(subjects):
    """ Takes the randomized trial data, and sorts it by set """
    global total_sets, excluded_sets
    for subject in subjects:
        for block in subject['data']:
            for trial in block:

                # Skip trials that don't have a 'set' parameter
                if ('set' not in trial): continue

                # if the subject doesn't have a list of sets heard, create the list
                if ('sets' not in subject): subject['sets'] = []



                trial_set = ', '.join([str(num) for num in trial['set']])

                # if the set isn't in the global counter of sets, include it
                if (trial_set not in per_set_data): per_set_data[trial_set] = {'total':0, 'excluded':0}

                # if this trial's set doesn't appear in the list of sets heard by the subject, add it
                if (trial_set not in subject['sets']):
                    subject['sets'].append(trial_set)
                    per_set_data[trial_set]['total']+=1
                    total_sets+=1
                    # also make a subject[set] dict that will contain info about that set and all the trials in that set
                    subject[trial_set] = {'excluded_trials': 0, 'total_trials': 0, 'excluded': False, 'trials': []}

                subject[trial_set]['trials'].append(trial)

                # increment the number of total trials for this set for this subject
                subject[trial_set]['total_trials'] += 1


                # if this trial was excluded, increment the number of excluded trials for that set for that subject
                if trial['excluded']: subject[trial_set]['excluded_trials'] += 1
    print("Re-structured data by set.")
    return subjects

def exclude_sets_with_few_trials(subjects, min_trials=min_responses_per_set):
    """ Marks as excluded, sets who do not have enough responses (as set in the defaults) """
    global excluded_sets
    for subject in subjects:
        for set in subject['sets']:

            # if there are less than min_trials after exclusion, mark the entire set as excluded
            if(subject[set]['total_trials']-subject[set]['excluded_trials']<min_trials):
                subject[set]['excluded'] = True
                per_set_data[set]['excluded'] += 1
                excluded_sets+=1


    print("Excluded sets with insufficient trials.")
    return subjects


'''Subject Related Functions'''

def mark_all_subjects_as_included(subjects):
    global total_subjects
    for subject in subjects:
        subject['excluded'] = False
        total_subjects += 1
    return subjects

def exclude_subjects_with_no_sets(subjects):
    """ Mark as excluded any subject that has no valid sets """
    global excluded_subjects
    exclude = True
    for subject in subjects:
        # Skip over subjects that have already been excluded.
        if(subject['excluded']):continue

        for set in subject['sets']:
            if(not subject[set]['excluded']): exclude = False

        subject['excluded'] = exclude
        if(subject['excluded']): excluded_subjects += 1
    return subjects


'''Stats Functions'''

def print_counters():
    print("Total Subjects:", total_subjects)
    print("Remaining Subjects:", total_subjects-excluded_subjects)

    print("Total Sets:", total_sets)
    print("Remaining Sets:", total_sets-excluded_sets, "(",excluded_sets/total_sets,')')

    print("Total Trials", total_trials)
    print("Remaining Trials", total_trials-excluded_trials, "(",excluded_trials/total_trials,')')

    print("per set data for",len(per_set_data),'sets.')
    for set in per_set_data:
        print(set,': remaining',per_set_data[set]['total']-per_set_data[set]['excluded'])


def save_data(subjects):
    # Saves the post_exclusion data as JSON files in Post_Exclusion_Data

    if (not os.path.isdir(post_exclusion_folder)):
        os.mkdir(post_exclusion_folder)

    for subject in subjects:
        task_set = subject['task_set']
        with open(post_exclusion_folder + "/" + task_set + ".json", "w") as outfile:
            json.dump(subject, outfile)
    print("Saved data post exclusion.")

# load subs
subjects = load_task_sets()

# exclude irrelevant trials
subjects = exclude_irrelevant_JSON_trials(subjects)

# exclude neither trials
subjects = exclude_neither_trials(subjects)

# exclude incomplete trials
subjects = exclude_incomplete_trials(subjects)

# exclude decoy trials
subjects = exclude_decoy_trials(subjects)

# restructure data by set
subjects = restructure_data_by_set(subjects)

# exclude sets with insufficient trials
subjects = exclude_sets_with_few_trials(subjects)

# initially include all subjects
mark_all_subjects_as_included(subjects)

# exclude subjects with no sets
subjects = exclude_subjects_with_no_sets(subjects)

print_counters()

save_data(subjects)


