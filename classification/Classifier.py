from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn import linear_model, datasets
from sklearn.model_selection import cross_val_score
from sklearn import svm
from scipy.stats import zscore
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from random import shuffle
from statistics import mean
import itertools
import operator
import math
import numpy as np
import pandas as pd


from configparser import ConfigParser
import codecs

config = ConfigParser()
# Open the file with the correct encoding
with codecs.open('config.ini', 'r', encoding='utf-8') as f:
    config.readfp(f)


class Classifier:
    def __init__(self):
        self.DF_MEAN = pd.DataFrame()
        self.DF_MIN = pd.DataFrame()
        self.DF_MAX = pd.DataFrame()
        self.dfDifference = pd.DataFrame()
        self.weights = {}

    # function responsible for returning accuracy, precision, recall and roc-auc score
    def getScores(self,yTrue, yPredicted):
        return (accuracy_score(yTrue, yPredicted),
                precision_score(yTrue, yPredicted, pos_label=0),
                recall_score(yTrue, yPredicted, pos_label=0))
                # roc_auc_score(yTrue, yPredicted))

    def customSplit(self, allData, seed=0, splitRatio =0.2):
        xTrainDf = pd.DataFrame()
        xTestDf = pd.DataFrame()
        yTrainDf = pd.DataFrame()
        yTestDf = pd.DataFrame()
        for i in range (0, len(allData)):

            xTrain, xTest, yTrain, yTest = train_test_split(allData[i]["data"].sort_index(),
                                                            allData[i]["predicted"].sort_index(), test_size=splitRatio, random_state=seed)
            self.deleteUnsucsefullTasks(i + 1, xTrain, xTest, yTrain, yTest)
            xTrainDf = pd.concat([xTrainDf, xTrain])
            xTestDf = pd.concat([xTestDf, xTest])
            yTrainDf = pd.concat([yTrainDf, yTrain])
            yTestDf = pd.concat([yTestDf, yTest])

        return [xTrainDf, xTestDf, yTrainDf, yTestDf]

    def deleteUnsucsefullTasks(self,taskNuber, xTrain, xTest, yTrain, yTest):
        participantsList = config.get('delete', str(taskNuber)).split("\n")

        for participant in participantsList:
            if participant in xTrain.index:
                xTrain.drop(participant, inplace=True)
            if participant in xTest.index:
                xTest.drop(participant, inplace=True)
            if participant in yTrain.index:
                yTrain.drop(participant, inplace=True)
            if participant in yTest.index:
                yTest.drop(participant, inplace=True)

    def normalizeDataframe(self, df, trainng=True):
        if trainng:
            self.DF_MEAN = df.mean()
            self.DF_MIN = df.min()
            self.DF_MAX = df.max()
            self.dfDifference = self.DF_MAX  - self.DF_MIN
            self.dfDifference[self.dfDifference == 0] = .1


        return (df - self.DF_MEAN) / (self.dfDifference)



    def getAllParticipants(self):
        allParticipants = []
        counter = 1
        while counter:
            try:
                allParticipants.extend(config.get('participants', 'group' + str(counter)).split('\n'))
                counter += 1
            except:
                break
        return allParticipants


    def splitDataFor10CrosValidation(self, iteration, splits, participants, allData):
        testParticipants = splits[iteration]
        trainParticipants = participants.copy()
        for item in testParticipants:
            trainParticipants.remove(item)

        dfTrain = None
        dfTest =  None
        for i in range(0, len(allData)):
            data = pd.concat([allData[i]["data"], allData[i]["predicted"]], axis=1)
            testDf = data.loc[data.index.intersection(testParticipants)]
            trainDf = data.loc[data.index.intersection(trainParticipants)]
            if dfTrain is not None and dfTest is not None:
                dfTrain =  pd.concat([dfTrain, trainDf], axis=0)
                dfTest =  pd.concat([dfTest, testDf], axis=0)
            else:
                dfTrain = trainDf
                dfTest =testDf
        yTrainDf = pd.DataFrame()
        yTestDf =  pd.DataFrame()
        yTrainDf["predicted"] = dfTrain.pop("predicted")
        yTestDf["predicted"] = dfTest.pop("predicted")
        return dfTrain, dfTest, yTrainDf, yTestDf


    def testModel(self, allData):
        participants = self.getAllParticipants()
        shuffle(participants)
        splits = np.array_split(participants, 10)
        scores = []

        importance = {}
        for i in range(10):
            xTrainDf, xTestDf, yTrainDf, yTestDf = self.splitDataFor10CrosValidation(i, splits, participants, allData)
            clf = linear_model.LogisticRegression(C=1e5)
            clf.fit(xTrainDf, yTrainDf["predicted"].tolist())
            dfPredicted = clf.predict(xTestDf)
            print(dfPredicted)
            scores.append(self.getScores(yTestDf["predicted"].tolist(), dfPredicted))
            print(self.getScores(yTestDf["predicted"].tolist(), dfPredicted))
            # print out importance of logistic regresion
            rfImportances = pd.DataFrame()
            rfImportances["name"] = xTrainDf.columns.values.tolist()
            rfImportances["importance"] = clf.coef_[0].tolist()
            result = rfImportances.sort_values(by=['importance'], ascending=False)

            # importance over all interations
            for index, row in result.iterrows():
                if row['name'] not in importance.keys():
                    importance[row['name']] = []
                importance[row['name']].append(row['importance'])
        for key in importance.keys():
            importance[key] = sum(importance[key]) / float(len(importance[key]))
        sorted_x = sorted(importance.items(), key=operator.itemgetter(1), reverse=True)

        print(*map(mean, zip(*scores)))
        print("Logistic regresion weights:")
        for s in sorted_x:
            print(*s)




    def correalationsAfterDataSplittingAnReduction(self, allData):
        xTrainDf, xTestDf, yTrainDf, yTestDf = self.customSplit(allData, seed=0 * 53, splitRatio=0.2)
#         xTrainDf = self.normalizeDataframe(xTrainDf, trainng=True)
#         xTestDf = self.normalizeDataframe(xTestDf, trainng=False)
        trainDf = pd.concat([xTrainDf,xTestDf])
        testDf = pd.concat([yTrainDf,yTestDf])
        allDf = pd.concat([trainDf, testDf], axis=1)
        tmp = allDf.corr(method='spearman')["predicted"]
        correlations = tmp.drop("predicted").abs().sort_values(ascending=False)
        print(correlations)

