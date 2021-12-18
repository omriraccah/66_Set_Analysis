#%% Import libs
from scipy import stats
import pandas as pd
from paths import *
import numpy as np

#%% Load data
GL = pd.read_csv(processed_dir + 'group_level_results.csv')  # Load group level data


#%% Get correlation of every sixth of subjects on rate_shifted
matrix = []
for i in range(6):
    row = []
    for j in range(6):
        X = GL[GL['section'] == i].groupby('set')['rate shifted'].mean()

        X = X.sort_index()
        Y = GL[GL['section'] == j].groupby('set')['rate shifted'].mean()
        Y = Y.sort_index()
        R = stats.pearsonr(X,Y)[0]
        row.append(R)
    matrix.append(row)
matrix = pd.DataFrame(matrix)

#%% Get correlation of every half of subjects on rate_shifted
X = GL[GL['section'].isin([0,1,2])].groupby('set')['rate shifted'].mean().sort_index()
Y = GL[GL['section'].isin([3,4,5])].groupby('set')['rate shifted'].mean().sort_index()
R = stats.pearsonr(X,Y)[0]

