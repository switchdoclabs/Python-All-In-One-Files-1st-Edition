
# Looking at the Shiny Diamonds 

#import the pandas and numpy library 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# read the diamonds CSV file 
# build a DataFrame from the data
df = pd.read_csv('diamonds.csv')


import matplotlib.pyplot as plt

carat = df.carat
clarity = df.clarity
plt.scatter(clarity, carat)
plt.show()  # or plt.savefig("name.png")


