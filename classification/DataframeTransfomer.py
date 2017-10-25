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

def saveDataframe(dataframe, taskId):
    dataframe.to_csv(config.get('classification', 'csvPath').format(taskId=str(taskId)))

def loadDataFrame(taskId):
    df = pd.read_csv(config.get('classification', 'csvPath').format(taskId=str(taskId)), index_col='participant')
    # ignoredPaticipants = config.get('participants', 'ignored').split("\n")
    # if len( ignoredPaticipants) > 0:
    #     df.drop(ignoredPaticipants, inplace=True)
    return df
