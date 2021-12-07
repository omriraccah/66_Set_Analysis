import seaborn as sns
import matplotlib.pyplot as plt

from paths import *
import pandas as pd


data = pd.read_csv(processed_dir + 'totals.csv')
data = data[data['chose']=="shifted"]
# ax = sns.barplot(y="set", x=">subject>set>condition:bias", data=data)
sns.scatterplot(y="set", x=">subject>set>condition:bias", data=data)


plt.show()
print('hello')