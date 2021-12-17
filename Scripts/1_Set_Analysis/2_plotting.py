"""#########################################################################
This script uses the data aggregated, formatted, and structured in previous scripts to plot the data
#########################################################################"""

import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import pyplot

from paths import *
import pandas as pd

"""###

WITHIN SUBJECT ANALYSIS

###"""

within = pd.read_csv(processed_dir + 'within.csv')

#subjects that selected "neither" more than half the time (on entire task regardless of set)
neither_inclined_subs = within.groupby('subject').sum()
neither_inclined_subs = neither_inclined_subs[neither_inclined_subs['no_neither_trials']<60].index.values

#remove those subjects
within = within[~within['subject'].isin(neither_inclined_subs)]

within['rate shifted - rate swapped'] = within['rate shifted'] - within['rate swapped']
within['rate not shifted'] = within['rate swapped'] + within['rate neither']
within['rate not swapped'] = within['rate shifted'] + within['rate neither']

# # plot_order = within.groupby('set').mean().sort_values(by=["rate shifted"], ascending=False).index.values
# # fig, ax = pyplot.subplots(figsize=(8, 12))
# # sns.pointplot(ax=ax, y="set", x="rate shifted", data=within, order=plot_order, height=15, aspect=11.7 / 2)
# # plt.show()
#
# # plot_order = within.groupby('set').mean().sort_values(by=["rate neither"], ascending=False).index.values
# # fig, ax = pyplot.subplots(figsize=(8, 12))
# # sns.pointplot(ax=ax, y="set", x="rate neither", data=within, order=plot_order, height=15, aspect=11.7 / 2)
# # plt.show()
# #
# # plot_order = within.groupby('set').mean().sort_values(by=["rate swapped"], ascending=False).index.values
# # fig, ax = pyplot.subplots(figsize=(8, 12))
# # sns.pointplot(ax=ax, y="set", x="rate swapped", data=within, order=plot_order, height=15, aspect=11.7 / 2)
# # plt.show()
#
# plot_order = within.groupby('set').mean().sort_values(by=["rate shifted - rate swapped"], ascending=False).index.values
# fig, ax = pyplot.subplots(figsize=(8, 12))
# sns.pointplot(ax=ax, y="set", x="rate shifted - rate swapped", data=within, order=plot_order, height=15, aspect=11.7 / 2)
# plt.show()
#
# # plot_order = within.groupby('set').mean().sort_values(by=["rate not shifted"], ascending=False).index.values
# # fig, ax = pyplot.subplots(figsize=(8, 12))
# # sns.pointplot(ax=ax, y="set", x="rate not shifted", data=within, order=plot_order, height=15, aspect=11.7 / 2)
# # plt.show()
#
# # plot_order = within.groupby('set').mean().sort_values(by=["rate not swapped"], ascending=False).index.values
# # fig, ax = pyplot.subplots(figsize=(8, 12))
# # sns.pointplot(ax=ax, y="set", x="rate not swapped", data=within, order=plot_order, height=15, aspect=11.7 / 2)
# # plt.show()
#
#
#
# plot_order = within.groupby('set').mean().sort_values(by=["rate_NN_shifted"], ascending=False).index.values
# fig, ax = pyplot.subplots(figsize=(8, 12))
# sns.pointplot(ax=ax, y="set", x="rate_NN_shifted", data=within, order=plot_order, height=15, aspect=11.7 / 2)
# plt.show()
#
#
#
#
# plot_order = within.groupby('set').mean().sort_values(by=["rate shifted"], ascending=False).index.values
# fig, ax = pyplot.subplots(figsize=(8, 12))
# sns.pointplot(ax=ax, y="set", x="rate shifted", data=within, order=plot_order, height=15, aspect=11.7 / 2)
# plt.show()

plot_order = within.groupby('set').mean().sort_values(by=["rate neither"], ascending=False).index.values
fig, ax = pyplot.subplots(figsize=(8, 12))
sns.pointplot(ax=ax, y="set", x="rate neither", data=within, order=plot_order, height=15, aspect=11.7 / 2)
plt.show()

"""###

ACROSS SUBJECT ANALYSIS

###"""
# across = pd.read_pickle(processed_dir + 'processed_data.pickle')
# across = across[across['has_decoy'] == False]
#
# counts = across.groupby('set')['chose'].value_counts().unstack()
# counts['total'] = counts['shifted'] + counts['swapped'] + counts['neither']
# counts['shifted_rate'] = counts['shifted'] / counts['total']
# counts['neither_rate'] = counts['neither'] / counts['total']
# counts['not_shifted_rate'] = 1 - counts['shifted_rate']
# counts = counts.reset_index().rename(columns={'index':'set'})
# plot_order = counts.sort_values(by=["neither_rate"], ascending=False)['set'].values
# fig, ax = pyplot.subplots(figsize=(8, 12))
# sns.pointplot(ax=ax, y="set", x="neither_rate", data=counts, order=plot_order, height=15, aspect=11.7 / 2)
# plt.show()



# # plot_order = counts.sort_values(by=["neither_rate"], ascending=False)['set'].values
# fig, ax = pyplot.subplots(figsize=(8, 12))
# sns.countplot(ax=ax,y="chose", hue='set', data=across)
# plt.show()

