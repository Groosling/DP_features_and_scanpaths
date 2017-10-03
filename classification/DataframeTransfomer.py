import pandas as pd
from configparser import ConfigParser
import codecs

config = ConfigParser()
# Open the file with the correct encoding
with codecs.open('config.ini', 'r', encoding='utf-8') as f:
    config.readfp(f)

def featuresToDataframe(listOfDictionaryofDictionaries):
    dataframe = pd.DataFrame()
    for dictonaryOfDictionaries in listOfDictionaryofDictionaries:
        d = pd.DataFrame.from_dict(dictonaryOfDictionaries, orient='index')
        dataframe = pd.concat([dataframe, d], axis=1)
    dataframe.index.name = "participant"
    return dataframe

def saveDataframe(dataframe):
    dataframe.to_csv(config.get('classification', 'csvPath'))

def loadDataFrame():
    df = pd.read_csv(config.get('classification', 'csvPath'), index_col='participant')
    ignoredPaticipants = config.get('participants', 'ignored').split("\n")
    df.drop(ignoredPaticipants, inplace=True)
    return df
