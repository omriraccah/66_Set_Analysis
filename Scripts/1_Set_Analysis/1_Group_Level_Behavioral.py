"""#########################################################################
This script:
1) Calculates totals, rates, and averages of relevant data
2) Does basic restructuring of data
3) Combines data with qualtrics data
#########################################################################"""
import numpy as np
import pandas as pd
from paths import *

AT = pd.read_pickle(processed_dir + processed_data_pickle_filename)  # AT = All Trials
ATND = AT[AT['has_decoy'] == False]  # ATND = All Trials No Decoys

# Ignore malformed trials (only selects trials that have an empty 'malformed' field)
ATND = ATND[ATND['malformed'] == ""]

# Starts a new dataframe called "GL" which will store the group-level calculated fields. The following line
# counts how many times a certain choice (e.g. 'shifted') was made within a certain set  (e.g., the pentatonic),
# within a certain subject (e.g., SSS0001)
GL = ATND.groupby(['subject', 'set']).count().reset_index()
GL = GL.iloc[:, :2]  # Selects only the first 3 columns

# We also calculate the mean RT within the same grouping (of a certain choice, within a certain set, within a certain
# subject)
shifted_rt = ATND[ATND['chose'] == 'shifted'].groupby(['subject', 'set'])['rt'].mean().reset_index()
shifted_rt = shifted_rt.rename(columns={'rt':'rt shifted'})

swapped_rt = ATND[ATND['chose'] == 'swapped'].groupby(['subject', 'set'])['rt'].mean().reset_index()
swapped_rt = swapped_rt.rename(columns={'rt':'rt swapped'})

neither_rt = ATND[ATND['chose'] == 'neither'].groupby(['subject', 'set'])['rt'].mean().reset_index()
neither_rt = neither_rt.rename(columns={'rt':'rt neither'})


# The df is merged with the mean RTs.
GL = pd.merge(GL, shifted_rt, on=['subject', 'set'])
GL = pd.merge(GL, swapped_rt, on=['subject', 'set'])
GL = pd.merge(GL, neither_rt, on=['subject', 'set'])

shifted_count = ATND[ATND['chose'] == 'shifted'].groupby(['subject', 'set'])['name'].count().reset_index()
shifted_count = shifted_count.rename(columns={'name':'# shifted'})

swapped_count = ATND[ATND['chose'] == 'swapped'].groupby(['subject', 'set'])['name'].count().reset_index()
swapped_count = swapped_count.rename(columns={'name':'# swapped'})

neither_count = ATND[ATND['chose'] == 'neither'].groupby(['subject', 'set'])['name'].count().reset_index()
neither_count = neither_count.rename(columns={'name':'# neither'})

# The df is merged with the mean number of trials for each condition.
GL = pd.merge(GL, shifted_count, on=['subject', 'set'])
GL = pd.merge(GL, swapped_count, on=['subject', 'set'])
GL = pd.merge(GL, neither_count, on=['subject', 'set'])

# holds the TOTAL number of trials that subject saw for that set.
GL['# trials'] = GL['# shifted'] + GL['# swapped'] + GL['# neither']

# The total number of trials if we ignore neithers.
GL['# no_neither_trials'] = GL['# trials'] - GL['# neither']

# Iterates through the different conditions (shifted, swapped, neither) and calculates their rate (0 through 1).
GL['rate shifted'] = GL['# shifted'] / GL['# trials']
GL['rate swapped'] = GL['# swapped'] / GL['# trials']
GL['rate neither'] = GL['# neither'] / GL['# trials']

# Calculates the rate of shifted and swapped when neithers are ignored. (NN=No Neithers)
GL['rate_NN_shifted'] = GL['# shifted'] / GL['# no_neither_trials']
GL['rate_NN_swapped'] = GL['# neither'] / GL['# no_neither_trials']

GL['rate shifted - rate swapped'] = GL['rate shifted'] - GL['rate swapped']
GL['rate shifted - rate swapped (NN)'] = GL['rate_NN_shifted'] - GL['rate_NN_swapped']

# Add the section number of each subject
temp = ATND.groupby(['subject'])['section'].mean().reset_index()
GL = pd.merge(GL, temp, on=['subject'])
GL['section'] = GL['section'].apply(np.floor)

# Merge with qualtrics so richer crossections can be achieved. (The same code appear in 3_reprocess_raw.py)
qualtrics = pd.read_csv(qualtrics_processed_dir + "qualtrics.csv")
GL = pd.merge(GL, qualtrics, on="subject")

# Combine with set features based on set
features = pd.read_csv(DATA_DIR + "5-note-sets-with-features.csv")
GL = pd.merge(GL, features, on="set")
GL.to_csv(processed_dir + 'group_level_results.csv')  # Saving to file.
