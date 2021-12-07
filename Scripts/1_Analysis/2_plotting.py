import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import pyplot

from paths import *
import pandas as pd


data = pd.read_csv(processed_dir + 'totals.csv')
data = data[data['chose']=="shifted"].reset_index()

mean = data.groupby(['set'])[">subject>set>condition:bias"].mean().reset_index(name='bias')
plot_order = mean.sort_values(by=["bias"]).set.values
fig, ax = pyplot.subplots(figsize=(8,12))

sns.pointplot(ax=ax, y="set", x=">subject>set>condition:bias", data=data, order=plot_order,height=15, aspect=11.7/2)

plt.show()
