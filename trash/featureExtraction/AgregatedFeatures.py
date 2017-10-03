# TODO add fixaton count and fixation rate...
# TODO allow cuting down length of the sequences .. to enable proper using of sum function
import numpy as np
from configparser import ConfigParser
import codecs

config = ConfigParser()
# Open the file with the correct encoding
with codecs.open('config.ini', 'r', encoding='utf-8') as f:
    config.readfp(f)

def calculateAgregatedFeatures(basicFeatures):
    """
    calculate sum, mean and stdev of basic features
    Args:
        basicFeatures: basic features extracted from dataset

    Returns:

    """
    listOfFeatures = config.get('aggregFeatures', 'appliedFeatures').split('\n')
    sumBool = bool(int(config.get('aggregFeatures', 'sum')))
    meanBool = bool(int(config.get('aggregFeatures', 'mean')))
    stdBool = bool(int(config.get('aggregFeatures', 'std')))

    participants = {}
    keys = list(basicFeatures)
    for y in range(0, len(keys)):
        features = {}
        for z in range(0, len(listOfFeatures)):

            #  if given basic featue doesn't exists, ignore it
            if listOfFeatures[z] not in basicFeatures[keys[y]]:
                continue
            features[listOfFeatures[z]] = {}
            if sumBool:
                features[listOfFeatures[z]]["sum"] = np.sum(basicFeatures[keys[y]][listOfFeatures[z]])
            if meanBool:
                features[listOfFeatures[z]]["mean"] = np.mean(basicFeatures[keys[y]][listOfFeatures[z]])
            if stdBool:
                features[listOfFeatures[z]]["stdev"] = np.std(basicFeatures[keys[y]][listOfFeatures[z]])
        participants[keys[y]] = features
    return participants





