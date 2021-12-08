import pandas as pd
from paths import *
# TODO: DOUBLE AND TRIPLE CHECK THAT THIS CODE WORKS AS EXPECTED
# ATND = All Trials No Decoys
AT = pd.read_pickle(processed_dir + processed_data_pickle_filename)
ATND = AT[AT['has_decoy']==False]

# Column to hold subject names
# totals = pd.DataFrame(AT['subject'])

totals = ATND.groupby(['subject','set','chose']).size().reset_index().rename(columns={0:'>subject>set>condition:count'})
temp = ATND.groupby(['subject','set']).size().reset_index().rename(columns={0:'>subject>set:count'})
totals = pd.merge(totals, temp, on=['subject', 'set'])
totals['>subject>set>condition:bias'] = totals['>subject>set>condition:count']/totals['>subject>set:count']
totals['>subject>set>condition:rt_mean'] = ATND.groupby(['subject','set','chose'], as_index=False)['rt'].transform('mean')

totals.to_csv(processed_dir + 'totals.csv')

