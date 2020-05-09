# imports
import sys
import pandas as pd
from sqlalchemy import create_engine

def load_data(train_file_path, test_file_path):
    """
    """
    # train = pd.read_csv('train_set.csv',  encoding='latin-1')

    train = pd.read_csv(train_file_path, encoding='latin-1')
    test = pd.read_csv(test_file_path, encoding='latin-1')

    return train, test

def clean(df):
  """
  Data cleaning and processing of text data. 

  INPUT:
  df: dataframe(object): 

  OUTPUT
  df: dataframe(object): cleaned dataframe object for 
  """

  # duplicated rows
  print("\nDroping duplicated rows . . .") 
  print("Total rows :", len(df))  
  df = df.drop_duplicates( keep='first')
  print("Total rows after removing duplicate :", len(df))

  # replacing more than one empty space
  print("\nReplacing more than one spaces . . . ")
  df['text'] = df['text'].str.replace(r'\b\w\b','').str.replace(r'\s+', ' ')

  # lower case
  print("\nConverting to lowercase . . .")
  df['text'] = df['text'].apply(lambda x: " ".join(x.lower() for x in x.split()))

  # replacing single words
  print("\nReplacing single words . . . ")
  df['text'] = df['text'].str.replace('[^\w\s]','')

  # stopwords
#   print("\nReplacing stop words . . .") 
#   df['text'] = df['text'].apply(lambda x: " ".join(x for x in x.split() if x not in stop))

  # spelling correction 
#   print("\nSpelling correction . . . .")
#   train['text'][:5].apply(lambda x: str(TextBlob(x).correct()))

  return df


def save_data(df, database_file_name):
    """
    """

    engine = create_engine('sqlite:///{}'.format(database_file_name))
    db_file_name = database_file_name.split("/")[-1] # extract file name from file path

    table_name = db_file_name.split(".")[0]
    df.to_sql(table_name, engine, index=False, if_exists='replace')





def main():

    if len(sys.argv) == 4:

        train_filepath, test_filepath, database_filepath = sys.argv[1:]

        print('Loading data...\n    train: {}\n    test: {}'
            .format(train_filepath, test_filepath))
        
        train_set, test_set = load_data(train_filepath, test_filepath)
        
        print('Loading complete ...\n')

        print("Cleaning data...")
        df = clean(train_set)
        print("Cleaning complete...")

        print('Saving data...\n    DATABASE: {}'.format(database_filepath))
        save_data(df, database_filepath)

        print("Cleaned data saved to database....")

    else:
        print('Please provide the correct filepaths')


# run
if __name__ == '__main__':
    main()

