"""#########################################################################
This script:
1) Calculates totals, rates, and averages of relevant data
2) Does basic restructuring of data
3) Combines data with qualtrics data
#########################################################################"""

import pandas as pd
from paths import *

AT = pd.read_pickle(processed_dir + processed_data_pickle_filename)  # AT = All Trials
ATND = AT[AT['has_decoy'] == False]  # ATND = All Trials No Decoys


# Starts a new dataframe called "GL" which will store the group-level calculated fields. The following line
# counts how many times a certain choice (e.g. 'shifted') was made within a certain set  (e.g., the pentatonic),
# within a certain subject (e.g., SSS0001)
GL = ATND.groupby(['subject', 'set', 'chose']).size().reset_index().rename(columns={0: '#'})

# We also calculate the mean RT within the same grouping (of a certain choice, within a certain set, within a certain
# subject)
temp = ATND.groupby(['subject', 'set', 'chose'])['rt'].mean().reset_index()

# The counts are merged with the mean RTs.
GL = pd.merge(GL, temp, on=['subject', 'set', 'chose'])

# Restructuring the panda from having a seperate row for each condition (shifted, swapped, and neither), to have all
# the data appear within the same row, but in designated columns.
GL = GL.groupby(['subject', 'set', 'chose']).mean().unstack(fill_value=0).reset_index()

# holds the TOTAL number of trials that subject saw for that set.
GL['trials'] = GL['#'].sum(axis=1)



# The total number of trials if we ignore neithers.
GL['no_neither_trials'] = GL['trials'] - GL[('#', 'neither')]

# Iterates through the different conditions (shifted, swapped, neither) and calculates their rate (0 through 1).
temp = GL['#'].div(GL['trials'], axis=0)
for col in temp.columns.values:
    GL['rate', col] = temp[col]

# Calculates the rate of shifted and swapped when neithers are ignored. (NN=No Neithers)
GL['rate_NN_shifted'] = GL[('#', 'shifted')] / GL['no_neither_trials']
GL['rate_NN_swapped'] = GL[('#', 'swapped')] / GL['no_neither_trials']

# remove MultiIndex levels (flattens df)
GL.columns = [' '.join(col).strip() for col in GL.columns.values]


# Merge with qualtrics so richer crossections can be achieved. (The same code appear in 3_reprocess_raw.py)
qualtrics = pd.read_csv(qualtrics_processed_dir + "qualtrics.csv")
GL = pd.merge(GL, qualtrics, on="subject")

# Combine with set features based on set
features = pd.read_csv(DATA_DIR + "5-note-sets-with-features.csv")
GL = pd.merge(GL, features, on="set")


GL.to_csv(processed_dir + 'group_level_results.csv')  # Saving to file.
