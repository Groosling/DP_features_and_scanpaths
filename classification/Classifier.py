from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.model_selection import cross_val_score
from sklearn import svm
from scipy.stats import zscore
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from statistics import mean
import itertools

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
        # reduce data to contains same number of elements for each class
        trainDf =  pd.concat([xTrainDf, yTrainDf], axis=1)
        testDf = pd.concat([xTestDf, yTestDf], axis=1)
        print(1)
        trainHist = trainDf["predicted"].value_counts().sort_values()
        testHist =  testDf["predicted"].value_counts().sort_values()
        print("0 = novice, 1 = skilled")
        print("Values distribution train data: ")
        print(trainHist)
        print("Values distribution test data: ")
        print(testHist)
        # Same number of data in both classes
        # Train data
        trainSmallerClass = trainHist.index.values[0]
        trainSmallCount = trainHist.values[0]
        trainBiggerClass = trainHist.index.values[1]
        smallDF  = trainDf[trainDf["predicted"] == trainSmallerClass]
        bigDF  = trainDf[trainDf["predicted"] == trainBiggerClass]
        bigDF = bigDF.head(n=trainSmallCount)
        # yTrainDf["predicted"] = smallDF
        trainDf = pd.DataFrame()
        trainDf= pd.concat([smallDF,bigDF], axis=0)
        yTrainDf = pd.DataFrame()
        yTrainDf["predicted"] = trainDf["predicted"]
        xTrainDf = pd.DataFrame()
        xTrainDf = trainDf.drop("predicted", axis=1)

        # Test data
        testSmallerClass = testHist.index.values[0]
        testSmallCount = testHist.values[0]
        testBiggerClass = testHist.index.values[1]
        smallDF  = testDf[testDf["predicted"] == testSmallerClass]
        bigDF  = testDf[testDf["predicted"] == testBiggerClass]
        bigDF = bigDF.head(n=testSmallCount)
        testDf = pd.DataFrame()
        testDf= pd.concat([smallDF,bigDF], axis=0)
        yTestDf = pd.DataFrame()
        yTestDf["predicted"] = testDf["predicted"]
        xTestDf = pd.DataFrame()
        xTestDf = testDf.drop("predicted", axis=1)

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

    def featureSelection(self, allData):
        for data in allData:
            data["data"].drop(["tester21",

                               "tester23",
                               "tester24"
                              ], inplace=True)

            data["predicted"].drop(["tester21", "tester23", "tester24"], inplace=True)
        # allData = allData[:1]
        return allData


    def testModel(self, allData):
        scores = []
        # allData = self.featureSelection(allData)
        for i in range(5):
            xTrainDf, xTestDf, yTrainDf, yTestDf = self.customSplit(allData, seed=i*53, splitRatio=0.2)
            # clf = KNeighborsClassifier(n_neighbors=1)
            # clf = RandomForestClassifier()
            clf = svm.SVC(kernel='rbf', class_weight='balanced', C=1, gamma=0.0001)
            # clf = svm.SVC(kernel='rbf', class_weight={1:1.3, 0:1}, C=1, gamma=0.0001)
            xTrainDf = self.normalizeDataframe(xTrainDf, trainng=True)
            clf.fit(xTrainDf, yTrainDf["predicted"].tolist())
            xTestDf = self.normalizeDataframe(xTestDf, trainng=False)
            dfPredicted = clf.predict(xTestDf)
            print(dfPredicted)
            scores.append(self.getScores(yTestDf["predicted"].tolist(), dfPredicted))
            print(self.getScores(yTestDf["predicted"].tolist(), dfPredicted))
        print("Crossvalidation average: ")
        print("------------------------")
        print(*map(mean, zip(*scores)))

    def correalationsAfterDataSplittingAnReduction(self, allData):
        xTrainDf, xTestDf, yTrainDf, yTestDf = self.customSplit(allData, seed=0 * 53, splitRatio=0.2)
        xTrainDf = self.normalizeDataframe(xTrainDf, trainng=True)
        xTestDf = self.normalizeDataframe(xTestDf, trainng=False)
        trainDf = pd.concat([xTrainDf,xTestDf])
        testDf = pd.concat([yTrainDf,yTestDf])
        allDf = pd.concat([trainDf, testDf], axis=1)
        tmp = allDf.corr(method='spearman')["predicted"]
        correlations = tmp.drop("predicted").abs().sort_values(ascending=False)
        print(correlations)