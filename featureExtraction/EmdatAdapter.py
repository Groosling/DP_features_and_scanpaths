import subprocess
from subprocess import check_output
import os
from configparser import ConfigParser
import codecs

parser = ConfigParser()
with codecs.open('config.ini', 'r', encoding='utf-8') as f:
    parser.readfp(f)


def runEMDAT(args, taskId):
    check_output(parser.get('EMDAT', 'python27Path') + " libs/EMDAT/src/customTest.py " + str(taskId) + args, shell=True).decode()

def prepareAOIFile(dataset):
    file = open("data/allData/aois.aoi", 'w')
    for aoi in dataset.aois:
        file.write(aoi[0] + "\t" + aoi[1]         + "," + aoi[3]                         + "\t" +
                   str(int(aoi[1]) + int(aoi[2])) + "," + aoi[3]                         + "\t" +
                   str(int(aoi[1]) + int(aoi[2])) + "," + str(int(aoi[3]) + int(aoi[4])) + "\t" +
                   aoi[1]                         + "," + str(int(aoi[3]) + int(aoi[4])) + "\n")
    file.close()

def prepareSegFile(dataset):
    outputFile = open("data/allData/TobiiV3_sample.seg", 'w')
    outputFile.write("problem1	S1	" + str(1) + "	" + str(99999999))
    outputFile.close()

def loadResults():
    try:
        fo = open(parser.get('run', 'outputFeatures'), "r")
    except:
        print("Failed to open output file")
        return
    actFileContent = fo.read()
    fo.close()
    actFileLines = actFileContent.split('\n')
    columnCaptions = actFileLines[0].split('\t')
    features = {}
    for i in range(0, len(actFileLines)):
        lineList = actFileLines[i].split('\t')
        if i > 0 and len(lineList) > 0 and "_allsc" in lineList[0]:
            participantName = lineList[0].split("_allsc")[0]
            features[participantName] = {}
            for j in range (1,len(lineList)):
                features[participantName][columnCaptions[j]] = lineList[j]
    return features

def extractBasicFeatures(dataset, taskID):
    prepareAOIFile(dataset)
    prepareSegFile(dataset)
    keys = list(dataset.participants.keys())
    args = ""
    for key in keys:
    # for key in keys:
        args += " " + key
    runEMDAT(args, taskID)
    loadResults()



