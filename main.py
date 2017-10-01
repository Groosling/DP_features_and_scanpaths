from algorithm.Sta import *
from algorithm.Position_based_Weighted_Models import *
from algorithm.Dotplot import *
from algorithm.Spam import *
import time
from structure import Sequence
from configparser import ConfigParser
import codecs
from featureExtraction import BasicFeatures
from featureExtraction import AgregatedFeatures
from featureExtraction.AoiFeatures import *
from featureExtraction.AngleFeatures import *
from featureExtraction.EmdatAdapter import extractBasicFeatures, loadResults
from featureExtraction.RqaAdapter import extractRQAFeatures, createFileForRQADemo
from display.ScanpathPlotter import ScanpathPlotter
from comparison.FeatureComparison import *


ALGORITHM_STA = 1
ALGORITHM_PBWM = 2
ALGORITHM_DOTPLOT = 3
ALGORITHM_SPAM = 4

def spamAlgorithm(my_dataset, myEnv):
    start_time = time.time()
    spam = Spam(my_dataset, my_env)
    res_data = spam.spamRun(mod=1, simplify=True)
    print("--- %s seconds ---" % (time.time() - start_time))
    return res_data

def staAlgorithm(my_dataset, myEnv):
    start_time = time.time()
    sta = Sta(my_dataset, my_env)
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


def dotplotAlgorithm(my_dataset, myEnv):
    start_time = time.time()
    dotplot = Dotplot(my_dataset, my_env)
    res_data = dotplot.runDotplot(simplify=True, mod=1)
    # print (common_sequence)
    print("--- %s seconds ---" % (time.time() - start_time))
    return res_data

def applyCommonScanpatAlgoritmusOnDatasets(datasets, myEnv, algoritmusIndentifier):
    results = []
    for dataset in datasets:
        results.append(applyCommonScanpathAlgorithm(dataset, myEnv, algoritmusIndentifier))
    return results

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

def calulateFeatures(dataset):
    extractBasicFeatures(dataset)

if __name__ == "__main__":
    parser = ConfigParser()
    # Open the file with the correct encoding
    with codecs.open('config.ini', 'r', encoding='utf-8') as f:
        parser.readfp(f)

    # Storage for all loaded data

    # Environment in which the eye tracking experiment was performed
    my_dataset = Dataset(
                        parser.get('run', 'scanpathFilePath'),
                        parser.get('run', 'AoiFilePath'),
                        'static/images/datasets/template_sta/placeholder.png', # default stuff
                        parser.get('run', 'websiteName'),
    )
    my_env = Environment(0.5, 60, 1920, 1200, 17)
    listOfDataset = my_dataset.getDatasetDividedIntoGroups()

    # basic features
    # """
    calulateFeatures(my_dataset)
    features = loadResults()
    print(features)
    # """

    # RQA Features
    rqaFeatures = extractRQAFeatures(my_dataset)
    print(5)
    # createFileForRQADemo(my_dataset)

    # more datasets
    # results = applyCommonScanpatAlgoritmusOnDatasets(listOfDataset,  my_env, ALGORITHM_PBWM)
    # one dataset
    # results = applyCommonScanpathAlgorithm(my_dataset, my_env, ALGORITHM_PBWM)


    # sequence = Sequence.createSequences(my_dataset, mod=1)
    # sequence = Sequence.getArrayRepresentationOfSequence(sequence)
    # basicFeatures = BasicFeatures.calculateBasicFeatures(my_dataset.participants)
    # result = AgregatedFeatures.calculateAgregatedFeatures(basicFeatures)

    # averageValuesForDataset = compareDatasets(basicFeatures)
    # vec1 = Sequence.calculateVector(0, 0, 2, 2)
    # vec2 = Sequence.calculateVector(0, 0, 0, 3)
    # angle = Sequence.calculateAngle(vec1, vec2)
    # aoisFeatures = AoiFeatures()
    # participantsWithAois = aoisFeatures.createParitcipantsWithAois(my_dataset)
    # result = aoisFeatures.getAoiFeatures(participantsWithAois)
    # angleFeatures = AngleFeatures()
    # angleFeatures.getAngleFeatures(my_dataset)
    # print ("aaa")


    # errorRateArea = 0
    # mySequences = Sequence.createSequences(my_dataset, errorRateArea)
    # for keys, values in mySequences.items():
    #     print(keys)
    #     print(values)
    #
    # mySequences = Sequence.getArrayRepresentationOfSequence(mySequences)
    # processed_sequence = Sequence.applyFixDurationThreshold(mySequences)




    # if res_data is None:
    #     res_data = {}
    #     res_data['fixations'] = []
    # scanPathPlotter = ScanpathPlotter()
    # commonScanpathPositions =scanPathPlotter.scanpathToPlotRepresentation(res_data['fixations'], my_dataset.aois)
    # keys = list(my_dataset.participants.keys())
    # for key in keys:
    #     scanPath = scanPathPlotter.participantToPlotRepresentation(my_dataset.participants[key])
    #     scanPathPlotter.plot2D("Participant " + key,
    #                            "Participant " + key,
    #                            parser.get('run', 'backgroundPageImage'),
    #                            scanPath,
    #                            commonScanpathPositions,
    #                             firstScanpathLegend=key
    #                           )

