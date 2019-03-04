# Diamonds are a Data Scientists Best Friend

#import the pandas and numpy library 
import numpy as np
import pandas as pd


# read the diamonds CSV file 
# build a DataFrame from the data
df = pd.read_csv('diamonds.csv')


print (df.head(10))
print()

# calculate total value of diamonds
sum = df.price.sum()
print ("Total $ Value of Diamonds: ${:0,.2f}".format( sum))

# calculate mean price of diamonds

mean = df.price.mean()
print ("Mean $ Value of Diamonds: ${:0,.2f}".format(mean))

#  summarize the data
descrip = df.carat.describe()
print()
print (descrip)


descrip = df.describe(include='object')
print()
print (descrip)


