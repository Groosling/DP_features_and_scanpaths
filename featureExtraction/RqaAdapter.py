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
        outputFile = open("outputfolder/" + key + ".txt", 'w')
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
        results["reoccurrence"] = ReoccurrenceFunctions.getReoccurrence(matrix)
        results["reoccurrenceRate"] = ReoccurrenceFunctions.getReoccurrenceRate(matrix)
        results["reoccurrenceDeterminism"] = ReoccurrenceFunctions.getDeterminism(matrix)
        results["reoccurrenceLaminarity"] = ReoccurrenceFunctions.getLaminarity(matrix)
        results["reoccurrenceCORM"] = ReoccurrenceFunctions.getCORM(matrix)

        #reccurrences
        timeDelayValue = int(parser.get('RQA', 'timeDelayValue'))
        numTimeDelaySamples = int(parser.get('RQA', 'numTimeDelaySamples'))
        phaseSpaceClusteringThreshold = float(parser.get('RQA', 'phaseSpaceClusteringThreshold'))
        fixationsXYPhaseSpaceData = RecurrenceFunctions.TimeDelayEmbedding(timeSeriesObservations=fixations,
                                                                           delayStep=timeDelayValue,
                                                                           delaySamples=numTimeDelaySamples)
        recurrenceMatrixData = RecurrenceFunctions.CreateRecurrenceMatrix(phaseSpaceData=fixationsXYPhaseSpaceData,
                                                                          clusteringDistanceThreshold= 	phaseSpaceClusteringThreshold );

        results["recurrence"] = RecurrenceFunctions.getRecurrence(recurrenceMatrixData, numTimeDelaySamples);
        results["recurrenceRate"] = RecurrenceFunctions.getRecurrenceRate(recurrenceMatrixData, numTimeDelaySamples);
        (results["recurrenceMeanX"], results["recurrenceMeanY"]) = RecurrenceFunctions.getRecurrenceMean(recurrenceMatrixData, numTimeDelaySamples);
        (results["recurrenceStandardDeviationX"],results["recurrenceStandardDeviationY"]) = RecurrenceFunctions.getRecurrenceStandardDeviation(recurrenceMatrixData,
                                                                                                 numTimeDelaySamples);
        reoccurrence[key] = results

    return reoccurrence