from configparser import ConfigParser
import codecs
from operations.Operations import *

import numpy as np

parser = ConfigParser()
# Open the file with the correct encoding
with codecs.open('config.ini', 'r', encoding='utf-8') as f:
    parser.readfp(f)
class AngleFeatures:
    def __init__(self):
        self.aois =[]
        aoiRange = int(parser.get('aoiRange', 'absoluteAngle'))
        self.aoiCount = int(ceil(360.0 / aoiRange))
        for z in range(0, self.aoiCount):
            self.aois.append(getAOIBasedOnRange(z*aoiRange, aoiRange))

    def getAbsoluteAngleHistogram(self, my_dataset):
        """
        For each participant create dictionary with aois based on absolute angles, which contain
        lengths of sacade
        Args:
            my_dataset: dataset

        Returns:

        """
        max_AOI = int(parser.get('sequence', 'maxAoi'))
        aoiRange = int(parser.get('aoiRange', 'absoluteAngle'))

        angleParticipants = {}
        participants = my_dataset.participants
        myAoIs = my_dataset.aois
        keys = list(participants)
        for y in range(0, len(keys)):
            aois = {}
            for z in range(0, self.aoiCount):
                aois[getAOIBasedOnRange(z*aoiRange, aoiRange)] = []

            for z in range(0, min(len(participants[keys[y]]) - 1, max_AOI)):
                # default vector (right direction)
                vec1 = calculateVector(0, 0, 1, 0)
                # calculates vector between curent point and next one
                vec2 = calculateVector(int(participants[keys[y]][z][3]), int(participants[keys[y]][z][4]),
                                       int(participants[keys[y]][z + 1][3]), int(participants[keys[y]][z + 1][4]))
                tempdist = calculateDistance(int(participants[keys[y]][z][3]), int(participants[keys[y]][z][4]),
                                            int(participants[keys[y]][z + 1][3]), int(participants[keys[y]][z + 1][4]))

                angle = calculateAngle(vec1, vec2)
                # duration is calculated as sum of both sacades durations
                aois[getAOIBasedOnRange(angle, aoiRange)].append(tempdist)
            angleParticipants[keys[y]] = aois
        return angleParticipants

    def getRelativeAngleHistogram(self, my_dataset):
        """
        For each participant create dictionary with aois based on relative angles, which contain
        lengths of sacade
        Args:
            my_dataset: dataset

        Returns:

        """
        aoiRange = int(parser.get('aoiRange', 'absoluteAngle'))
        max_AOI = int(parser.get('sequence', 'maxAoi'))

        angleParticipants = {}
        participants = my_dataset.participants
        myAoIs = my_dataset.aois
        keys = list(participants)
        for y in range(0, len(keys)):
            aois = {}
            for z in range(0, self.aoiCount):
                aois[getAOIBasedOnRange(z*aoiRange, aoiRange)] = []

            for z in range(0, min(len(participants[keys[y]]) - 2, max_AOI)):
                # default vector (right direction)
                vec1 = calculateVector(int(participants[keys[y]][z][3]), int(participants[keys[y]][z][4]),
                                       int(participants[keys[y]][z + 1][3]), int(participants[keys[y]][z + 1][4]))
                # calculates vector between next point and next next one
                vec2 = calculateVector(int(participants[keys[y]][z + 1][3]), int(participants[keys[y]][z + 1][4]),
                                       int(participants[keys[y]][z + 2][3]), int(participants[keys[y]][z + 2][4]))
                tempdist = calculateDistance(int(participants[keys[y]][z + 1][3]), int(participants[keys[y]][z + 1][4]),
                                            int(participants[keys[y]][z + 2][3]), int(participants[keys[y]][z + 2][4]))

                angle = calculateAngle(vec1, vec2)
                # duration is calculated as sum of both sacades durations
                aois[getAOIBasedOnRange(angle, aoiRange)].append(tempdist)
            angleParticipants[keys[y]] = aois
        return angleParticipants

    def getSumFixDuration(self, angleParticipants):
        """
        Sum fixation lengths in each bin.
        Args:
            angleParticipants:

        Returns:

        """
        result = {}
        keys = list(angleParticipants)
        for y in range(0, len(keys)):
            tempList = []
            for z in range(0, len(self.aois)):
                sum = 0
                for k in range(0, len(angleParticipants[keys[y]][self.aois[z]])):
                    sum = sum + int(angleParticipants[keys[y]][self.aois[z]][k])
                tempList.append(sum)
            result[keys[y]] = tempList
        return result

    def getFixationsCount(self, angleParticipants):
        """
        Counts number of fixation in each bin.
        Args:
            angleParticipants:

        Returns:

        """
        result = {}
        keys = list(angleParticipants)
        for y in range(0, len(keys)):
            tempList = []
            for z in range(0, len(self.aois)):
                count = 0
                for k in range(0, len(angleParticipants[keys[y]][self.aois[z]])):
                    count = count + 1
                tempList.append(count)
            result[keys[y]] = tempList
        return result

    def getMaxFixLength(self, angleParticipants):
        """
        Get maximal fixation length for each bin
        Args:
            self:
            angleParticipants:

        Returns:

        """
        result = {}
        keys = list(angleParticipants)
        for y in range(0, len(keys)):
            tempList = []
            for z in range(0, len(self.aois)):
                maxVal = max(angleParticipants[keys[y]][self.aois[z]] or [0])
                tempList.append(maxVal)
            result[keys[y]] = tempList
        return result
    def getMinFixLength(self, angleParticipants):
        """
        Get minimal fixation length for each bin
        Args:
            self:
            angleParticipants:

        Returns:

        """
        result = {}
        keys = list(angleParticipants)
        for y in range(0, len(keys)):
            tempList = []
            for z in range(0, len(self.aois)):
                minVal = min(angleParticipants[keys[y]][self.aois[z]] or [0])
                tempList.append(minVal)
            result[keys[y]] = tempList
        return result

    def getAvgFixLength(self, angleParticipants):
        """
        Get average fixation length for each bin
        Args:
            self:
            angleParticipants:

        Returns:

        """
        result = {}
        keys = list(angleParticipants)
        for y in range(0, len(keys)):
            tempList = []
            for z in range(0, len(self.aois)):
                meanVal = np.mean(angleParticipants[keys[y]][self.aois[z]] or [0])
                tempList.append(meanVal)
            result[keys[y]] = tempList
        return result

    def getAngleFeatures(self, my_dataset):
        absAngleParticipants = self.getAbsoluteAngleHistogram(my_dataset)
        angleFeatures = []
        angleFeatures.append(self.getSumFixDuration(absAngleParticipants))
        angleFeatures.append(self.getFixationsCount(absAngleParticipants))
        angleFeatures.append(self.getMaxFixLength(absAngleParticipants))
        angleFeatures.append(self.getMinFixLength(absAngleParticipants))
        angleFeatures.append(self.getAvgFixLength(absAngleParticipants))
        keys = list(absAngleParticipants)
        allFeatures = {}
        for y in range(0, len(keys)):
            allFeatures[keys[y]] = []
        for k in range(0, len(angleFeatures)):
            for y in range(0, len(keys)):

                allFeatures[keys[y]].extend(angleFeatures[k][keys[y]])

        relAbsAngleParticipants = self.getRelativeAngleHistogram(my_dataset)
        # TODO same for relAbsAngleParticipants