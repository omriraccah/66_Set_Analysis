import pandas as pd
from paths import *


# AT = All Trials
AT = pd.read_pickle(processed_dir + processed_data_pickle_filename)

# ATND = All Trials No Decoys
ATND = AT[AT['has_decoy'] == False]

# Column to hold subject names
# totals = pd.DataFrame(AT['subject'])

totals = ATND.groupby(['subject', 'set', 'chose']).size().reset_index().rename(columns={0: '#'})
temp = ATND.groupby(['subject', 'set', 'chose'])['rt'].mean().reset_index()
totals = pd.merge(totals, temp, on=['subject', 'set', 'chose'])
totals = totals.groupby(['subject', 'set', 'chose']).mean().unstack(fill_value=0).reset_index()
totals['trials'] = totals['#'].sum(axis=1)
totals['no_neither_trials'] = totals['trials']-totals[('#','neither')]


temp = totals['#'].div(totals['trials'], axis=0)
for col in temp.columns.values:
    totals['rate', col] = temp[col]

totals['rate_NN_shifted'] = totals[('#','shifted')]/totals['no_neither_trials']
totals['rate_NN_swapped'] = totals[('#','swapped')]/totals['no_neither_trials']


# remove MultiIndex levels (flattens df)
totals.columns = [' '.join(col).strip() for col in totals.columns.values]

# Merge with qualtrics
qualtrics = pd.read_csv(qualtrics_processed_dir + "qualtrics.csv")
qualtrics = qualtrics.rename(columns={'sub':'subject'})

totals = pd.merge(totals, qualtrics, on="subject")



totals.to_csv(processed_dir + 'totals.csv')

