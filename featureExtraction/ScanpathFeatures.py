from algorithm.Dotplot import *
from algorithm.Position_based_Weighted_Models import *
from algorithm.Spam import *
from algorithm.Sta import *
import pandas as pd

from configparser import ConfigParser
import codecs

parser = ConfigParser()
# Open the file with the correct encoding
with codecs.open('config.ini', 'r', encoding='utf-8') as f:
    parser.readfp(f)

import time

ALGORITHM_STA = 1
ALGORITHM_PBWM = 2
ALGORITHM_DOTPLOT = 3
ALGORITHM_SPAM = 4

def spamAlgorithm(my_dataset, myEnv):
    start_time = time.time()
    spam = Spam(my_dataset, myEnv)
    res_data = spam.spamRun(mod=1, simplify=True)
    print("--- %s seconds ---" % (time.time() - start_time))
    return res_data

def staAlgorithm(my_dataset, myEnv):
    start_time = time.time()
    sta = Sta(my_dataset, myEnv)
    res_data = sta.sta_run(mod=1, simplify=True)
    print("--- %s seconds ---" % (time.time() - start_time))
    return res_data

def positionBasedWeightedModelsAlgorithm(my_dataset, myEnv):
    start_time = time.time()
    pbwm  = Position_based_Weighted_Models(my_dataset)
    res_data = pbwm.run_PBWM(mod=1,simplify=True,)
    # print (res_data)

    print("--- %s seconds ---" % (time.time() - start_time))
    return res_data

def applyCommonScanpatAlgoritmusOnDatasets(listOfDatasets, myEnv, algoritmusIndentifier):
    results = []
    for dataset in listOfDatasets:
        results.append(applyCommonScanpathAlgorithm(dataset, myEnv, algoritmusIndentifier))
    for result in results:
        for i in range (0, len(results)):
            normalizeCoef = 1
            if results[i] != result:

                if bool(int(parser.get('sequence', 'normalizeSimilarity'))) and len(results[i]["fixations"]) > 0:
                    normalizeCoef = len(results[i]["fixations"])
                similarityToAnotherGroup  = calcSimilarityForDataset(result["sequences"], results[i]["fixations"], listOfDatasets[0].aois)
                result["overallSimilarityTo" + str(i)] = similarityToAnotherGroup["OverAllSimilarity"] / normalizeCoef
                result["similarityTo" + str(i)] = {k: v / normalizeCoef for k, v in similarityToAnotherGroup["similarity"].items()}
            else:
                if bool(int(parser.get('sequence', 'normalizeSimilarity'))) and len(result["fixations"]) > 0:
                    normalizeCoef = len(result["fixations"])
                result["overallSimilarityTo" + str(i)] = result.pop("OverAllSimilarity") / normalizeCoef
                result["similarityTo" + str(i)] = {k: v / normalizeCoef for k, v in result.pop("similarity").items()}
    return results


def dotplotAlgorithm(my_dataset, myEnv):
    start_time = time.time()
    dotplot = Dotplot(my_dataset, myEnv)
    res_data = dotplot.runDotplot(simplify=True, mod=1)
    # print (common_sequence)
    print("--- %s seconds ---" % (time.time() - start_time))
    return res_data

def applyCommonScanpathAlgorithm(my_dataset, myEnv, mod):
    """
    Apply algorithm for extraction of common scanpath
    Args:
        my_dataset: dataset
        mod:     1 apply STA
                 2 apply Position Based Weighted Models
                 3 apply Dotplot
                 4 apply SPAM
    Returns: common scanpath

    """
    case = {
      1: staAlgorithm,
      2: positionBasedWeightedModelsAlgorithm,
      3: dotplotAlgorithm,
      4: spamAlgorithm,
    }
    myFunc = case[mod]
    return myFunc(my_dataset, myEnv)

def calculateScanpathFeatures(listofDataset, myEnv):
    results = {}
    results["PBWM"] = (applyCommonScanpatAlgoritmusOnDatasets(listofDataset, myEnv, ALGORITHM_PBWM))
    results["DOTPLOT"] = (applyCommonScanpatAlgoritmusOnDatasets(listofDataset, myEnv, ALGORITHM_DOTPLOT))
    results["STA"] = (applyCommonScanpatAlgoritmusOnDatasets(listofDataset, myEnv, ALGORITHM_STA))
    results["SPAM"] = (applyCommonScanpatAlgoritmusOnDatasets(listofDataset, myEnv, ALGORITHM_SPAM))
    return scanpathFeaturesToDataframe(results)


def scanpathFeaturesToDataframe(results):
    dataframe = pd.DataFrame()
    for key, listOfResults in results.items():
        singleAlgorithDF = [pd.DataFrame(), pd.DataFrame()]
        for i in range(0, len(listOfResults)):
            for j in range(0, len(listOfResults)):
                dfTemp = pd.DataFrame.from_dict(listOfResults[i]["similarityTo" + str(j)],  orient='index')
                dfTemp.rename(columns={0: key + "_similarityTo" + str(j)}, inplace=True)
                singleAlgorithDF[j] = pd.concat([singleAlgorithDF[j], dfTemp],axis=0)
        for i in range(1, len(listOfResults)):
            singleAlgorithDF[0] = pd.concat([singleAlgorithDF[0],singleAlgorithDF[i]], axis=1)
        dataframe = pd.concat([dataframe, singleAlgorithDF[0]], axis=1)
    return dataframe
