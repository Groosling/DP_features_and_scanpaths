from libs.RQA import DynamicalSystemsModule as RecurrenceFunctions
from libs.RQA import SpatioTemporalEyeTrackingModule as ReoccurrenceFunctions
from configparser import ConfigParser
import codecs

parser = ConfigParser()
with codecs.open('config.ini', 'r', encoding='utf-8') as f:
    parser.readfp(f)

def createFileForRQADemo(dataset):
    keys = list(dataset.participants.keys())
    for key in keys:
        results = {}
        fixations = []
        outputFile = open("output/RQA/" + key + ".txt", 'w')
        for fixation in dataset.participants[key]:
            outputFile.write( fixation[3] + "," + fixation[4] + "," + fixation[2] + "\n")
        outputFile.close()

def extractRQAFeatures(dataset):

    reoccurrence = {}
    keys = list( dataset.participants.keys())
    for key in keys:
        results = {}
        fixations = []
        for fixation in dataset.participants[key]:
            fixations.append([int(fixation[3]), int(fixation[4])])

        # reoccurrences
        clusteringDistanceThreshold = int(parser.get('RQA', 'clusteringDistanceThreshold'))
        matrix = ReoccurrenceFunctions.CreateReoccurrenceMatrix(fixations, clusteringDistanceThreshold=clusteringDistanceThreshold)
        try:
            results["reoccurrence"] = ReoccurrenceFunctions.getReoccurrence(matrix)
        except:
            results["reoccurrence"] = 0

        try:
            results["reoccurrenceRate"] = ReoccurrenceFunctions.getReoccurrenceRate(matrix)
        except:
            results["reoccurrenceRate"] = 0
        try:
            results["reoccurrenceDeterminism"] = ReoccurrenceFunctions.getDeterminism(matrix)
        except:
            results["reoccurrenceDeterminism"] = 0
        try:
            results["reoccurrenceLaminarity"] = ReoccurrenceFunctions.getLaminarity(matrix)
        except:
            results["reoccurrenceLaminarity"] = 0
        try:
            results["reoccurrenceCORM"] = ReoccurrenceFunctions.getCORM(matrix)
        except:
            results["reoccurrenceCORM"] = 0

        #reccurrences
        timeDelayValue = int(parser.get('RQA', 'timeDelayValue'))
        numTimeDelaySamples = int(parser.get('RQA', 'numTimeDelaySamples'))
        phaseSpaceClusteringThreshold = float(parser.get('RQA', 'phaseSpaceClusteringThreshold'))
        fixationsXYPhaseSpaceData = RecurrenceFunctions.TimeDelayEmbedding(timeSeriesObservations=fixations,
                                                                           delayStep=timeDelayValue,
                                                                           delaySamples=numTimeDelaySamples)
        recurrenceMatrixData = RecurrenceFunctions.CreateRecurrenceMatrix(phaseSpaceData=fixationsXYPhaseSpaceData,
                                                                          clusteringDistanceThreshold= 	phaseSpaceClusteringThreshold );
        try:
            results["recurrence"] = RecurrenceFunctions.getRecurrence(recurrenceMatrixData, numTimeDelaySamples)
        except:
            results["recurrence"] = 0
        try:
            results["recurrenceRate"] = RecurrenceFunctions.getRecurrenceRate(recurrenceMatrixData, numTimeDelaySamples)
        except:
            results["recurrenceRate"] = 0
        try:
            (results["recurrenceMeanX"], results["recurrenceMeanY"]) = RecurrenceFunctions.getRecurrenceMean(recurrenceMatrixData, numTimeDelaySamples);
        except:
            results["recurrenceMeanX"], results["recurrenceMeanY"] = [0,0]
        try:
            (results["recurrenceStandardDeviationX"],results["recurrenceStandardDeviationY"]) = RecurrenceFunctions.getRecurrenceStandardDeviation(recurrenceMatrixData,
                                                                                                 numTimeDelaySamples)
        except:
            results["recurrenceStandardDeviationX"], results["recurrenceStandardDeviationY"] = [0,0]
        reoccurrence[key] = results

    return reoccurrence