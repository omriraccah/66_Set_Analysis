"""#########################################################################
This script uses the data aggregated, formatted, and structured in previous scripts to plot the data
#########################################################################"""

#%% Load dependencies
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import pyplot

from paths import *
import pandas as pd

"""###

WITHIN SUBJECT ANALYSIS

###"""

#%% Load data
within = pd.read_csv(processed_dir + 'group_level_results.csv')

#%% Data Clean-up
# remove subjects that selected "neither" more than half the time (on entire task regardless of set)
neither_inclined_subs = within.groupby('subject').sum()
neither_inclined_subs = neither_inclined_subs[neither_inclined_subs['# no_neither_trials']<60].index.values
within = within[~within['subject'].isin(neither_inclined_subs)]

#%% remove sets with fewer than 10 no_neither trials
within = within[within['# no_neither_trials']>=10].reset_index()

#%% Sanity: Keep only pentatonic trials
within = within[within['set']=="0 2 4 7 9"].reset_index()

#%% Sanity: Keep only N first subjects
within = within.sort_values(by="RecordedDate").head(2000)

#%% Sanity: Only older subjects
within = within[~within['subject'].str.contains('SSS2v',regex=True)]

#%% Sanity: Only new subjects
within = within[within['subject'].str.contains('SSS2v',regex=True)]

#%% Subjects per set
temp = within.groupby('set').count().reset_index()
temp = temp.rename(columns={'subject':'Number of subjects'})
plot_order = temp.sort_values(by=["Number of subjects"], ascending=False)['set'].values
sns.catplot(y="set", x="Number of subjects", kind="bar", data=temp, order=plot_order, height=9)
plt.show()

#%% Avg. trials per subject per set
temp = within.groupby('set').mean().reset_index()
temp = temp.rename(columns={'trials':'Avg. number of trials per subject'})
plot_order = temp.sort_values(by=["Avg. number of trials per subject"], ascending=False)['set'].values
sns.catplot(y="set", x="Avg. number of trials per subject", kind="bar", data=temp, order=plot_order, height=9)
plt.show()

#%% Avg. no_neither_trials per subject per set
temp = within.groupby('set').mean().reset_index()
temp = temp.rename(columns={'no_neither_trials':'Avg. number of trials per subject (ignoring neithers)'})
plot_order = temp.sort_values(by=["Avg. number of trials per subject (ignoring neithers)"], ascending=False)['set'].values
sns.catplot(y="set", x="Avg. number of trials per subject (ignoring neithers)", kind="bar", data=temp, order=plot_order, height=9)
plt.show()

#%% distribution of rate of button presses across the task
temp = within[['subject', 'rate pressed neither (task)','rate pressed 1st (task)','rate pressed 2nd (task)']]
temp = temp.rename(columns={'rate pressed neither (task)':'neither','rate pressed 1st (task)':'1st','rate pressed 2nd (task)':'2nd'})
temp = temp.groupby('subject').mean().stack().reset_index()
temp = temp.rename(columns={'level_1':'pressed',0:'rate'})
sns.displot(data=temp, x="rate", hue="pressed",kind='kde')
plt.show()

#%% distribution of conditions across the task
temp = within[['subject', 'rate shifted','rate swapped','rate neither','set']]
temp = temp.rename(columns={'rate neither':'neither','rate shifted':'shifted','rate swapped':'swapped'})
temp = temp.groupby('subject').mean().stack().reset_index()
temp = temp.rename(columns={'level_1':'chose',0:'rate'})
sns.displot(data=temp, x="rate", hue="chose",kind='kde')
plt.show()

#%% distribution of conditions across the task for specific sets
temp = within[['subject', 'rate shifted','rate swapped','rate neither','set']]
temp = temp[temp['set']=="0 1 2 3 5"]
temp = temp.rename(columns={'rate neither':'neither','rate shifted':'shifted','rate swapped':'swapped'})
temp = temp.groupby('subject').mean().stack().reset_index()
temp = temp.rename(columns={'level_1':'chose',0:'rate'})
sns.displot(data=temp, x="rate", hue="chose",kind='kde')
plt.show()

#%% distribution of some condition (shifted/neither/swapped) across the task for all/specific sets
temp = within[['subject', 'rate neither','rate shifted','rate swapped','set']]
temp1 = temp.groupby('set').mean().sort_values(by='rate shifted')
worst = [*temp1.index.values[0:3]]
best = [*temp1.index.values[-3:]]
sets = worst+best
temp = temp[temp['set'].isin(sets)]

sns.displot(data=temp, x="rate neither", hue="set",kind='kde')
plt.show()

#%% Plot rate_shifted for each set (without ignoring neithers)
plot_order = within.groupby('set').mean().sort_values(by=["rate shifted"], ascending=False).index.values
fig, ax = pyplot.subplots(figsize=(8, 9))
sns.pointplot(ax=ax, y="set", x="rate shifted", data=within, order=plot_order)
plt.show()

#%% Plot rate_neither for each set
plot_order = within.groupby('set').mean().sort_values(by=["rate neither"], ascending=False).index.values
sns.catplot(y="set", x="rate neither", kind="bar", data=within, order=plot_order, height=9)
plt.show()

#%% Plot rate_swapped for each set (without ignoring neithers)
plot_order = within.groupby('set').mean().sort_values(by=["rate swapped"], ascending=False).index.values
fig, ax = pyplot.subplots(figsize=(8, 9))
sns.pointplot(ax=ax, y="set", x="rate swapped", data=within, order=plot_order)
plt.show()

#%% Plot rate_shifted-rate_swapped for each set (without ignoring neithers)
# temp = within[within['section'].isin([0])]
temp =within
# temp = temp[~temp['subject'].str.contains('SSS2v',regex=True)] #without new subjects
# temp=temp[temp['section']==0]
plot_order = temp.groupby('set').mean().sort_values(by=["rate shifted - rate swapped"], ascending=False).index.values
fig, ax = pyplot.subplots(figsize=(8, 9))
sns.pointplot(ax=ax, y="set", x="rate shifted - rate swapped", data=temp, order=plot_order)
plt.show()

#%% Plot rate of shifted (with neithers ignored)
plot_order = within.groupby('set').mean().sort_values(by=["rate_NN_shifted"], ascending=False).index.values
fig, ax = pyplot.subplots(figsize=(8, 9))
sns.pointplot(ax=ax, y="set", x="rate_NN_shifted", data=within, order=plot_order)
plt.show()

#%% Plot rate of shifted-swapped (with neithers ignored) with hues
# temp = within[within['section'].isin([0,5])]
temp =within
# temp = temp[~temp['subject'].str.contains('SSS2v',regex=True)] #without new subjects
# temp['half'] = temp['section']/3
# temp['half'] = temp['half'].apply(np.floor)
# temp=temp[temp['half']==1]
plot_order = temp.groupby('set').mean().sort_values(by=["rate shifted - rate swapped (NN)"], ascending=False).index.values
fig, ax = pyplot.subplots(figsize=(8, 9))
sns.pointplot(ax=ax, y="set", x="rate shifted - rate swapped (NN)", data=temp, order=plot_order)
plt.show()

#%% Plot rate of shifted-swapped with hues
# temp = within[within['section'].isin([0,5])]
temp =within
# plot_order = temp.groupby('set').mean().sort_values(by=["rate shifted - rate swapped"], ascending=False).index.values
plot_order = ["0 2 4 5 7","0 2 4 7 9","0 1 2 3 5"]
fig, ax = pyplot.subplots(figsize=(8, 9))
sns.pointplot(ax=ax, y="set", x="rate shifted - rate swapped", data=temp, order=plot_order, hue="section")
plt.show()

#%% Plot distribution of number of neither trials
sns.displot(data=within, x="# neither")
plt.show()

#%% Plot distribution of rate of swapped trials
sns.displot(data=within, x="rate swapped")
plt.show()

#%% Plot distribution of rate of shifted trials (when ignoring neithers)
sns.displot(data=within, x="rate_NN_shifted")
plt.show()

"""###

ACROSS SUBJECT ANALYSIS

###"""

#%% Load data
across = pd.read_pickle(processed_dir + 'processed_data.pickle')
across = across[across['has_decoy'] == False]

#%% Plot rate_neither for each set
counts = across.groupby('set')['chose'].value_counts().unstack()
counts['total'] = counts['shifted'] + counts['swapped'] + counts['neither']
counts['shifted_rate'] = counts['shifted'] / counts['total']
counts['neither_rate'] = counts['neither'] / counts['total']
counts['not_shifted_rate'] = 1 - counts['shifted_rate']
counts = counts.reset_index().rename(columns={'index':'set'})
plot_order = counts.sort_values(by=["neither_rate"], ascending=False)['set'].values
fig, ax = pyplot.subplots(figsize=(8, 9))
sns.pointplot(ax=ax, y="set", x="neither_rate", data=counts, order=plot_order)
plt.show()


