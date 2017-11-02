from structure.Dataset import *
from structure.Environment import *
from classification.DataframeTransfomer import featuresToDataframe, loadDataFrame
from classification.Correlations import *
from classification.Classifier import *

import pandas as pd
from configparser import ConfigParser
import codecs

config = ConfigParser()
# Open the file with the correct encoding
with codecs.open('config.ini', 'r', encoding='utf-8') as f:
    config.readfp(f)

scanpathFilePaths = config.get('run', 'scanpathFilePaths').split("\n")
aoiFilePaths = config.get('run', 'aoiFilePaths').split("\n")
websiteNames = config.get('run', 'websiteNames').split("\n")
backgroundPageImages = config.get('run', 'backgroundPageImages').split("\n")
dataframes = []
for i in range(0, 5):
    data = {}

    my_dataset = Dataset(
        scanpathFilePaths[i],
        aoiFilePaths[i],
        'static/images/datasets/template_sta/placeholder.png',  # default stuff
        websiteNames[i],
    )
    my_env = Environment(0.5, 60, 1920, 1200, 17)
    listOfDataset = my_dataset.getDatasetDividedIntoGroups()

    """ Prepare features """
    allFeatures = []
    dataset = my_dataset
    # load
    data["data"] = loadDataFrame(i + 1)
    # delete ignored
    if 'tester18' in data["data"].index:
        data["data"].drop(["tester18"], inplace=True)
    data["predicted"] = my_dataset.getPredictedColumnValues()
    data["data"].drop(["tester21",

                       "tester23",
                       "tester24",
                       ], inplace=True)
    data["predicted"].drop(["tester21",

                            "tester23",
                            "tester24",
                            ], inplace=True)

    dataframes.append(data)

dfTrain = pd.DataFrame()
dfPredicted = pd.DataFrame()
for dataframe in dataframes:
    dfTrain = pd.concat([dfTrain, dataframe["data"]], axis=0)
    dfPredicted = pd.concat([dfPredicted, dataframe["predicted"]], axis=0)
columns = config.get('classification', 'columnNames').split("\n")
dfTrain = dfTrain[columns]
corr = Correlations()
interAttributesCorrelation = corr.calculateInterAttributesCorrelations(dfTrain)
corrTopredicted = corr.calculateCorrelationsToPredicted(dfTrain, dfPredicted)
resultColumns = corr.deleteHighlyCorrelatedAttributes(interAttributesCorrelation, corrTopredicted)

for dataframe in dataframes:
    dataframe["data"] = dataframe["data"][resultColumns]

classifier= Classifier()
classifier.testModel(dataframes)

