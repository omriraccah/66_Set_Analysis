import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import pyplot

from paths import *
import pandas as pd

data = pd.read_csv(processed_dir + 'totals.csv')

#subjects that selected "neither" more than half the time (on entire task regardless of set)
neither_inclined_subs = data.groupby('subject').sum()
neither_inclined_subs = neither_inclined_subs[neither_inclined_subs['no_neither_trials']<60].index.values

#remove those subjects
data = data[~data['subject'].isin(neither_inclined_subs)]

plot_order = data.groupby('set').mean().sort_values(by=["rate shifted"], ascending=False).index.values
fig, ax = pyplot.subplots(figsize=(8, 12))
sns.pointplot(ax=ax, y="set", x="rate shifted", data=data, order=plot_order, height=15, aspect=11.7 / 2)
plt.show()

plot_order = data.groupby('set').mean().sort_values(by=["rate_NN_shifted"], ascending=False).index.values
fig, ax = pyplot.subplots(figsize=(8, 12))
sns.pointplot(ax=ax, y="set", x="rate_NN_shifted", data=data, order=plot_order, height=15, aspect=11.7 / 2)
plt.show()
