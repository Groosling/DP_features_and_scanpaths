from structure import Sequence

from ConfigParser import SafeConfigParser
import codecs
from operations.Operations import *

import numpy as np

parser = SafeConfigParser()
# Open the file with the correct encoding
with codecs.open('config.ini', 'r', encoding='utf-8') as f:
    parser.readfp(f)

class AoiFeatures:

    def __init__(self):
        self.aois = []


    def createParitcipantsWithAois(self,my_dataset):
        """
        Transform Participants representation the way, that each participant contain histogram of AOI
        which contain fixation respresented as [time, fixation_duration]
        Args:
            my_dataset:

        Returns:
         participants containing histogram of Aois
        """
        errorRateArea = int(parser.get('sequence', 'errorRateArea'))
        paritcipantsWithAois = {}
        participants = my_dataset.participants
        myAoIs = my_dataset.aois
        keys = participants.keys()
        for y in range(0, len(keys)):
            paritcipantsWithAois[keys[y]] = {}
            paritcipantsWithAois[keys[y]]["first_fixation"] = participants[keys[y]][0]
            # create list for each aoi for particulat participant
            if y == 0:
                self.aois = []
            for z in range(0, len(myAoIs)):
                paritcipantsWithAois[keys[y]][myAoIs[z][5]] = []
                if y == 0:
                    self.aois.append(myAoIs[z][5])

            for z in range(0, len(participants[keys[y]])):
                tempAoI = ""
                tempDuration = 0

                for k in range(0, len(myAoIs)):
                    if float(participants[keys[y]][z][3]) >= (float(myAoIs[k][1]) - errorRateArea) and float(
                            participants[keys[y]][z][3]) < (
                    ((float(myAoIs[k][1]) - errorRateArea) + (float(myAoIs[k][2]) + 2 * errorRateArea))) and float(
                            participants[keys[y]][z][4]) >= (float(myAoIs[k][3]) - errorRateArea) and float(
                            participants[keys[y]][z][4]) < (
                    ((float(myAoIs[k][3]) - errorRateArea) + (float(myAoIs[k][4]) + 2 * errorRateArea))):
                        tempAoI = tempAoI + myAoIs[k][5]
                        tempDuration = int(participants[keys[y]][z][2])
                # my solution compare sum of distances to four corners
                if len(tempAoI) > 1:
                    tempAoI = Sequence.getCloserAOI(participants[keys[y]][z],myAoIs, tempAoI)

                if len(tempAoI) != 0:
                    # add time and duraton of fixation
                    paritcipantsWithAois[keys[y]][tempAoI].append([int(participants[keys[y]][z][1]), int(participants[keys[y]][z][2])])
        return paritcipantsWithAois

    def getTotalNumberOfFixationOnAOi(self, paritcipantsWithAois):
        result = {}
        keys = paritcipantsWithAois.keys()
        for y in range(0, len(keys)):
            list = []
            for z in range(0, len(self.aois)):
                list.append(len(paritcipantsWithAois[keys[y]][self.aois[z]]))
            result[keys[y]] = list
        return result

    def getSumFixDuration(self, paritcipantsWithAois):
        result = {}
        keys = paritcipantsWithAois.keys()
        for y in range(0, len(keys)):
            list = []
            for z in range(0, len(self.aois)):
                sum = 0
                for k in range(0, len(paritcipantsWithAois[keys[y]][self.aois[z]])):
                    sum = sum + int(paritcipantsWithAois[keys[y]][self.aois[z]][k][1])
                list.append(sum)
            result[keys[y]] = list
        return result

    def getMeanFixDuration(self, paritcipantsWithAois):
        result = {}
        keys = paritcipantsWithAois.keys()
        for y in range(0, len(keys)):
            list = []
            for z in range(0, len(self.aois)):
                sum = 0
                for k in range(0, len(paritcipantsWithAois[keys[y]][self.aois[z]])):
                    sum = sum + int(paritcipantsWithAois[keys[y]][self.aois[z]][k][1])
                if len(paritcipantsWithAois[keys[y]][self.aois[z]]) != 0:
                    list.append(sum / len(paritcipantsWithAois[keys[y]][self.aois[z]]))
                else:
                    list.append(0)
            result[keys[y]] = list
        return result

    def getLongestFixDuration(self, paritcipantsWithAois):
        result = {}
        keys = paritcipantsWithAois.keys()
        for y in range(0, len(keys)):
            list = []
            for z in range(0, len(self.aois)):
                max = 0
                for k in range(0, len(paritcipantsWithAois[keys[y]][self.aois[z]])):
                    if int(paritcipantsWithAois[keys[y]][self.aois[z]][k][1]) > max:
                        max = int(paritcipantsWithAois[keys[y]][self.aois[z]][k][1])
                list.append(max)
            result[keys[y]] = list
        return result

    def getTimeToFirstFixation(self, paritcipantsWithAois):
       print "aaa"
       # TODO ... discutable

    def getAoiFeatures(self, paritcipantsWithAois):
        # result = self.getTotalNumberOfFixationOnAOi(paritcipantsWithAois)
        # result = self.getSumFixDuration(paritcipantsWithAois)
        # result = self.getMeanFixDuration(paritcipantsWithAois)
        result = self.getLongestFixDuration(paritcipantsWithAois)
