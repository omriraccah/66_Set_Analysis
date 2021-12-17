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

within = pd.read_csv(processed_dir + 'modes_within.csv')
within['# total'] = within['# correct'] + within['# incorrect']

# remove incomplete subjects (subs with 20/20 responses)
incomplete = within.groupby('subject').sum()
incomplete = incomplete[incomplete['# total'] < 20].index.values

# remove those subjects
within = within[~within['subject'].isin(incomplete)]


# sns.displot(data=within, x="rate correct")
# plt.show()

# plot_order = within.groupby('mode').mean().sort_values(by=["rate correct"], ascending=False).index.values
# fig, ax = pyplot.subplots(figsize=(8, 12))
# sns.pointplot(title="test", ax=ax, y="mode", x="rate correct", data=within, order=plot_order, height=15, aspect=11.7 / 2)
# plt.show()
#
# # Weak subjects (were correct <60% of the time)
# weak = within.groupby('subject').mean()
# weak = weak[weak['rate correct'] < .6].index.values
#
# # remove those subjects
# within = within[~within['subject'].isin(weak)]
#
# plot_order = within.groupby('mode').mean().sort_values(by=["rate correct"], ascending=False).index.values
# fig, ax = pyplot.subplots(figsize=(8, 12))
# sns.pointplot(title="test", ax=ax, y="mode", x="rate correct", data=within, order=plot_order, height=15, aspect=11.7 / 2)
# plt.show()


#
# across = within.groupby("mode").sum().reset_index()
# across['rate correct'] = across["# correct"].div(across['# total'], axis=0)
#
#
#
# plot_order = across.sort_values(by="rate correct", ascending=False)["mode"].values
# fig, ax = pyplot.subplots(figsize=(8, 12))
# sns.pointplot(ax=ax, y="mode", x="rate correct", data=across, order=plot_order, height=15, aspect=11.7 / 2)
# plt.show()
#
#


sub = within.groupby(['subject','mode']).sum().reset_index()
sub = sub[sub['trials']>8]
sub['rate correct'] = sub['# correct'].div(sub['trials'], axis=0)
plot_order = sub.sort_values(by=["rate correct"], ascending=False)["mode"].values
fig, ax = pyplot.subplots(figsize=(8, 12))
sns.pointplot(ax=ax, y="mode", x="rate correct", data=sub, order=["0 3 5 7 10", "0 2 5 7 9", "0 3 5 8 10", "0 2 4 7 9", "0 2 5 7 10"], height=15, aspect=11.7 / 2)
plt.show()

