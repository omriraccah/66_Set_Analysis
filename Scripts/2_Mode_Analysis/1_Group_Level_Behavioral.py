import pandas as pd
from paths import *

AT = pd.read_pickle(processed_dir + processed_data_pickle_filename)  # AT = All Trials
OD = AT[AT['has_decoy'] == True]  # OD = All Trials With Decoys
OD = OD[OD['set'] == "0 2 4 7 9"]  # The only trials with decoys are from the pentatonic anyway,but just in case.
# OD = OD.head(20)
"""Reconstructing Mode"""

# recovering probes pre-transposition
probes = OD['probe_pitches'].to_list()
swappeds = OD['swapped_pitches'].to_list()
probes = [[int(note) for note in probe.split(" ")] for probe in probes]
swappeds = [[int(note) for note in swapped.split(" ")] for swapped in swappeds]

decoy_position = []
transpositions = OD['transposition'].to_list()
for i in range(len(transpositions)):
    if (probes[i] == swappeds[i]):
        decoy_position.append("swapped")
    else:
        decoy_position.append("shifted")
    transposition = transpositions[i]
    probe = probes[i]
    probe = [note - transposition for note in probe]
    probes[i] = probe

PCs = [sorted(list(set([note % 12 for note in probe]))) for probe in probes]
valids = [len(PC) == 5 for PC in PCs]
PCs = [" ".join([str(note) for note in PC]) for PC in PCs]
OD['valid'] = valids
OD['mode'] = PCs
OD['decoy_pos'] = decoy_position
OD = OD[OD['valid'] == True]
OD['correct'] = ((OD['chose'] != OD['decoy_pos']) & (OD['chose'] != "neither"))

# # Starts a new dataframe called "modes_within" which will store the within-subject calculated fields. The following line
# # counts how many times a subject correctly identified a decoy within a certain mode,
# # within a certain subject (e.g., SSS0001)
modes_within = OD.groupby(['subject', 'mode', 'correct']).size().reset_index().rename(columns={0: '#'})
sanity = OD.groupby(['subject', 'mode']).size().reset_index().rename(columns={0: '#'})

print("asd")

# # We also calculate the mean RT within the same grouping
temp = OD.groupby(['subject', 'mode', 'correct'])['rt'].mean().reset_index()

# The counts are merged with the mean RTs.
modes_within = pd.merge(modes_within, temp, on=['subject', 'mode', 'correct'])

# Restructuring the panda from having a separate row for each condition (correct / incorrect), to have all
# the data appear within the same row, but in designated columns.
modes_within = modes_within.groupby(['subject', 'mode', 'correct']).mean().unstack(fill_value=0).reset_index()


# holds the TOTAL number of trials that subject saw for that set.
modes_within['trials'] = modes_within['#'].sum(axis=1)


# Iterates through the different conditions and calculates their rate (0 through 1).
temp = modes_within['#'].div(modes_within['trials'], axis=0)
for col in temp.columns.values:
    modes_within['rate', col] = temp[col]

# remove MultiIndex levels (flattens df)
columns = [[str(el) for el in col] for col in modes_within.columns.values]
modes_within.columns = [' '.join(col).strip() for col in columns]
modes_within = modes_within.rename(columns={'# False': '# incorrect', '# True': '# correct', 'rt False': 'rt incorrect', 'rt True': 'rt correct','rate False': 'rate incorrect', 'rate True': 'rate correct'})

# Merge with qualtrics so richer crossections can be achieved. (The same code appear in 3_preprocess_raw.py)
qualtrics = pd.read_csv(qualtrics_processed_dir + "qualtrics.csv")
qualtrics = qualtrics.rename(columns={'sub': 'subject'})
modes_within = pd.merge(modes_within, qualtrics, on="subject")

modes_within.to_csv(processed_dir + 'modes_within.csv')  # Saving to file.
