import numpy as np

from configparser import ConfigParser
import codecs

parser = ConfigParser()
with codecs.open('config.ini', 'r', encoding='utf-8') as f:
    parser.readfp(f)

def compareDatasets(basicFeatures):
    participantsGroups = []
    counter = 1
    while counter:
        try:
            participantsGroups.append(parser.get('participants', 'group' + str(counter)).split('\n'))
            counter += 1
        except:
            break
    comparisionResults = {}
    comparisionResults["fixationDuration"] = compareFeature(participantsGroups, basicFeatures, "fixationDuration")
    comparisionResults["saccadeLength"] = compareFeature(participantsGroups, basicFeatures, "saccadeLength")
    return comparisionResults


def compareFeature(participantsGroups, basicFeatures, featureName):
    averageFixationDurationPerGroup  = []
    for participantsGroup in participantsGroups:
        keys = list(participantsGroup)
        listOfAll = np.array([])
        for key in keys:
            listOfAll = np.append(listOfAll, basicFeatures[key][featureName])
        averageFixationDurationPerGroup.append(np.mean(listOfAll))
    return averageFixationDurationPerGroup

