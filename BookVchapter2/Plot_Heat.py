
# Looking at the Shiny Diamonds 

#import the pandas and numpy library 
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

# read the diamonds CSV file 
# build a DataFrame from the data
df = pd.read_csv('diamonds.csv')

# drop the index column
df = df.drop('Unnamed: 0', axis=1)

f, ax = plt.subplots(figsize=(10, 8))
corr = df.corr()
print (corr)
# color
#sns.heatmap(corr, mask=np.zeros_like(corr, dtype=np.bool), 
#        cmap=sns.diverging_palette(220, 10, as_cmap=True),
#                    square=True, ax=ax)

#grayscale

cmap = sns.cubehelix_palette(50, hue=0.05, rot=0, light=0.95, dark=0.05, as_cmap=True)
sns.heatmap(corr, mask=np.zeros_like(corr, dtype=np.bool), 
        cmap=cmap,
                    square=True, ax=ax)

plt.show()

