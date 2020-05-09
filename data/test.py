import pandas as pd 

# load the data
train = pd.read_csv('train_set.csv',  encoding='latin-1')
print(train.shape)
train.head()