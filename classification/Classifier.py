from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.model_selection import cross_val_score
from sklearn import svm
from scipy.stats import zscore
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from statistics import mean

import math
import numpy as np
import pandas as pd

class Classifier:
    def __init__(self):
        self.DF_MEAN = pd.DataFrame()
        self.DF_MIN = pd.DataFrame()
        self.DF_MAX = pd.DataFrame()

    # function responsible for returning accuracy, precision, recall and roc-auc score
    def getScores(self,yTrue, yPredicted):
        return (accuracy_score(yTrue, yPredicted),
                precision_score(yTrue, yPredicted, pos_label=0),
                recall_score(yTrue, yPredicted, pos_label=0), roc_auc_score(yTrue, yPredicted))


    def customSplit(self, allData, seed=0, splitRatio =0.2):
        xTrainDf = pd.DataFrame()
        xTestDf = pd.DataFrame()
        yTrainDf = pd.DataFrame()
        yTestDf = pd.DataFrame()
        for data in allData:
            xTrain, xTest, yTrain, yTest = train_test_split(data["data"], data["predicted"], test_size=splitRatio, random_state=seed)
            xTrainDf = pd.concat([xTrainDf, xTrain])
            xTestDf = pd.concat([xTestDf, xTest])
            yTrainDf = pd.concat([yTrainDf, yTrain])
            yTestDf = pd.concat([yTestDf, yTest])
        return [xTrainDf, xTestDf, yTrainDf, yTestDf]

    def normalizeDataframe(self, df, trainng=True):
        if trainng:
            self.DF_MEAN = df.mean()
            self.DF_MIN = df.min()
            self.DF_MAX = df.max()
        return (df - self.DF_MEAN) / (self.DF_MAX - self.DF_MIN)



    def testModel(self, allData):
        scores = []
        for data in allData:
            data["data"].drop(["tester21", "tester12", "tester23", "tester24", "tester11"], inplace=True)
            data["predicted"].drop(["tester21", "tester12", "tester23", "tester24", "tester11"], inplace=True)
        allData = allData[:4]
        for i in range(5):
            xTrainDf, xTestDf, yTrainDf, yTestDf = self.customSplit(allData, seed=i*53, splitRatio=0.4)
            clf = KNeighborsClassifier(n_neighbors=1)
            clf = svm.SVC(kernel='rbf', class_weight='balanced', C=1, gamma=0.0001)
            # xTrainDf = self.normalizeDataframe(xTrainDf, trainng=True)
            clf.fit(xTrainDf, yTrainDf["predicted"].tolist())
            xTestDf = self.normalizeDataframe(xTestDf, trainng=False)
            dfPredicted = clf.predict(xTestDf)
            print(dfPredicted)
            scores.append(self.getScores(yTestDf["predicted"].tolist(), dfPredicted))
            print(self.getScores(yTestDf["predicted"].tolist(), dfPredicted))
        print("Crossvalidation average: ")
        print("------------------------")
        print(*map(mean, zip(*scores)))


        print(5)
