
from featureExtraction.EmdatAdapter import extractBasicFeatures, loadResults
from featureExtraction.RqaAdapter import extractRQAFeatures
from featureExtraction.ScanpathFeatures import *
from classification.DataframeTransfomer import featuresToDataframe, loadDataFrame, saveDataframe
from classification.SVM import testModel
from classification.Correlations import *

from configparser import ConfigParser
import codecs

config = ConfigParser()
# Open the file with the correct encoding
with codecs.open('config.ini', 'r', encoding='utf-8') as f:
    config.readfp(f)





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

    calculateScanpathFeatures(listOfDataset, my_env)

    # """ Prepare features """
    # allFeatures = []
    # dataset  = my_dataset
    # if not bool(int(config.get('classification', 'useCsv'))):
    #     # basic features
    #     # """
    #     calulateFeatures(dataset)
    #     features = loadResults()
    #     allFeatures.append(features)
    #     print(features)
    #     # """
    #
    #     # RQA Features
    #     rqaFeatures = extractRQAFeatures(dataset)
    #     allFeatures.append(rqaFeatures)
    #     dataframe = featuresToDataframe(allFeatures)
    #     saveDataframe(dataframe)
    # else:
    #     dataframe = loadDataFrame()
    # dfPredicted = my_dataset.getPredictedColumnValues()
    #
    # """  calculate Correlations"""
    # correlations = Correlations()
    # correlations.calculateCorrelations(dataframe, dfPredicted)
    # # correlations.plotBoxplot()
    # # correlations.plotPairsSeaborn()
    # columnNames = correlations.getBestColumnNames(10)
    # dataframe = dataframe[columnNames]
    #
    # """ train and test model """
    # testModel(dataframe,dfPredicted)

    print(5)

    # TODO Skusit odstanit outlayerov  - to neviem ci chcem
    # TODO skusit dostat featury zo scanpathov
    # TODO pozret si mozno nieco k tomu ako davat na zakladny tvar slova vo vyhladavani info























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

