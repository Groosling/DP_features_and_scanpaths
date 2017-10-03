from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.model_selection import cross_val_score
from sklearn import svm
from scipy.stats import zscore
from sklearn.neighbors import KNeighborsClassifier

import numpy as np


# function responsible for returning accuracy, precision, recall and roc-auc score
def getScores(estimator, x, y):
    yPred = estimator.predict(x)
    return (accuracy_score(y, yPred),
            precision_score(y, yPred, pos_label=0),
            recall_score(y, yPred, pos_label=0), roc_auc_score(y, yPred))

def my_scorer(estimator, x, y):
    a, p, r, ra  = getScores(estimator, x, y)
    print (a, p, r, ra)
    return a+p+r+ra

def testModel(trainDataframe, testDataframe):
    numeric_cols = trainDataframe.select_dtypes(include=[np.number]).columns
    trainDataframe[numeric_cols] = trainDataframe[numeric_cols].apply(zscore)

    print("before model")
    # clf = svm.SVC(kernel='rbf', class_weight='balanced', C=1, gamma=0.0001)
    clf = KNeighborsClassifier(n_neighbors=3)
    sss = StratifiedShuffleSplit(n_splits=2, test_size=0.4, random_state=0)
    # scoresSSS = cross_val_score(clf, trainDf, testDf, cv=sss.split(trainDf, testDf))
    scoresSSS = cross_val_score(clf, trainDataframe, testDataframe, cv=sss.split(trainDataframe, testDataframe), scoring=my_scorer)
    print(str(scoresSSS))