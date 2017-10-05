from algorithm.Dotplot import *
from algorithm.Position_based_Weighted_Models import *
from algorithm.Spam import *
from algorithm.Sta import *

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
    print (res_data)

    print("--- %s seconds ---" % (time.time() - start_time))
    return res_data

def applyCommonScanpatAlgoritmusOnDatasets(listOfDatasets, myEnv, algoritmusIndentifier):
    results = []
    for dataset in listOfDatasets:
        results.append(applyCommonScanpathAlgorithm(dataset, myEnv, algoritmusIndentifier))
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
    results = []
    results.append(applyCommonScanpatAlgoritmusOnDatasets(listofDataset, myEnv, ALGORITHM_PBWM))
    results.append(applyCommonScanpatAlgoritmusOnDatasets(listofDataset, myEnv, ALGORITHM_DOTPLOT))
    results.append(applyCommonScanpatAlgoritmusOnDatasets(listofDataset, myEnv, ALGORITHM_STA))
    results.append(applyCommonScanpatAlgoritmusOnDatasets(listofDataset, myEnv, ALGORITHM_SPAM))
    return results
