
from featureExtraction.EmdatAdapter import extractBasicFeatures, loadResults
from featureExtraction.RqaAdapter import extractRQAFeatures
from featureExtraction.ScanpathFeatures import *
from classification.DataframeTransfomer import featuresToDataframe, loadDataFrame, saveDataframe
from classification.Classifier import *
from classification.Correlations import *

from configparser import ConfigParser
import codecs

config = ConfigParser()
# Open the file with the correct encoding
with codecs.open('config.ini', 'r', encoding='utf-8') as f:
    config.readfp(f)




if __name__ == "__main__":
    parser = ConfigParser()
    # Open the file with the correct encoding
    with codecs.open('config.ini', 'r', encoding='utf-8') as f:
        parser.readfp(f)

    # Storage for all loaded data
    # TODO spravit nech to robi v cykle pre vsetko v konfiguraku
    # Environment in which the eye tracking experiment was performed
    scanpathFilePaths = parser.get('run', 'scanpathFilePaths').split("\n")
    aoiFilePaths = parser.get('run', 'aoiFilePaths').split("\n")
    websiteNames = parser.get('run', 'websiteNames').split("\n")
    backgroundPageImages = parser.get('run', 'backgroundPageImages').split("\n")
    dataframes = []
    for i in range(0, len(scanpathFilePaths)):
        data = {}

        my_dataset = Dataset(
                            scanpathFilePaths[i],
                            aoiFilePaths[i],
                            'static/images/datasets/template_sta/placeholder.png', # default stuff
                            websiteNames[i],
        )
        my_env = Environment(0.5, 60, 1920, 1200, 17)
        listOfDataset = my_dataset.getDatasetDividedIntoGroups()

        """ Scanpath features """
        # calculateScanpathFeatures(listOfDataset, my_env)

        """ Prepare features """
        allFeatures = []
        dataset  = my_dataset
        if not bool(int(config.get('classification', 'useCsv'))):
            # basic features
            # """
            extractBasicFeatures(dataset, i+1)
            features = loadResults()
            allFeatures.append(features)
            print(features)
            # """

            # RQA Features
            rqaFeatures = extractRQAFeatures(dataset)
            allFeatures.append(rqaFeatures)

            dataframe = featuresToDataframe(allFeatures)
            saveDataframe(dataframe, i+1)
        else:
            # load
            data["data"] = loadDataFrame(i+1)
            # delete ignored
            if 'tester18' in data["data"].index:
                data["data"].drop(["tester18"], inplace=True)
            # select just important columns
            data["data"] = data["data"][parser.get('classification', 'columnNames').split("\n")]
            data["predicted"] = my_dataset.getPredictedColumnValues()

        dataframes.append(data)
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
    classifier= Classifier()
    classifier.testModel(dataframes)

    print(5)

    # TODO skusit dostat featury zo scanpathov
























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

