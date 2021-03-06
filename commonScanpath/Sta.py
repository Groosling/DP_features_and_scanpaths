from __future__ import division

import json

from commonScanpath.StringEditAlgs import *
from structure.Dataset import *
from structure.Environment import *
from structure.Sequence import *


class Sta:
    def __init__(self, my_dataset, my_env):
        self.my_dataset = my_dataset
        self.my_env = my_env
        self.parser = ConfigParser()
        # Open the file with the correct encoding
        with codecs.open('config.ini', 'r', encoding='utf-8') as f:
            self.parser.readfp(f)



    def getNumberedSequence(self, Sequence):
        numberedSequence = []
        numberedSequence.append([Sequence[0][0], 1, Sequence[0][1]])

        for y in range(1, len(Sequence)):
            if Sequence[y][0] == Sequence[y - 1][0]:
                numberedSequence.append([Sequence[y][0], numberedSequence[len(numberedSequence) - 1][1], Sequence[y][1]])
            else:
                numberedSequence.append([Sequence[y][0],self.getSequenceNumber(Sequence[0:y], Sequence[y][0]), Sequence[y][1]])

        AoIList = self.getExistingAoIListForSequence(numberedSequence)
        AoINames = self.my_dataset.aois
        AoINames = [w[5] for w in AoINames]
        newSequence = []

        myList = []
        myDictionary = {}
        replacementList = []

        for x in range(0, len(AoIList)):
            totalDuration = 0
            for y in range(0, len(numberedSequence)):
                if numberedSequence[y][0:2] == AoIList[x]:
                    totalDuration = totalDuration + int(numberedSequence[y][2])
            myList.append([AoIList[x], totalDuration])

        for x in range(0, len(AoINames)):
            myAoIList = [w for w in myList if w[0][0] == AoINames[x]]
            myAoIList.sort(key=lambda x: x[1])
            myAoIList.reverse()
            if len(myAoIList) > 0:
                myDictionary[AoINames[x]] = myAoIList

        for AoI in AoIList:
            index = [w[0] for w in myDictionary[AoI[0]]].index(AoI)
            replacementList.append([AoI, [AoI[0], (index + 1)]])

        for x in range(0, len(numberedSequence)):
            myReplacementList = [w[0] for w in replacementList]
            index = myReplacementList.index(numberedSequence[x][0:2])
            newSequence.append([replacementList[index][1][0]] + [replacementList[index][1][1]] + [numberedSequence[x][2]])

        return newSequence


    def getSequenceNumber(self, Sequence, Item):
        abstractedSequence = self.getAbstractedSequence(Sequence)
        return abstractedSequence.count(Item) + 1


    def getAbstractedSequence(self, Sequence):
        myAbstractedSequence = [Sequence[0][0]]
        for y in range(1, len(Sequence)):
            if myAbstractedSequence[len(myAbstractedSequence) - 1] != Sequence[y][0]:
                myAbstractedSequence.append(Sequence[y][0])
        return myAbstractedSequence


    def getExistingAoIListForSequence(self, Sequence):
        AoIlist = []
        for x in range(0, len(Sequence)):
            try:
                AoIlist.index(Sequence[x][0:2])
            except:
                AoIlist.append(Sequence[x][0:2])
        return AoIlist


    def calculateImportanceThreshold(self, mySequences):
        myAoICounter = self.getNumberDurationOfAoIs(mySequences)
        commonAoIs = []
        for myAoIdetail in myAoICounter:
            if myAoIdetail[3] == True:
                commonAoIs.append(myAoIdetail)

        if len(commonAoIs) == 0:
            print ("No shared instances!")
            return None

        minValueCounter = commonAoIs[0][1]
        for AoIdetails in commonAoIs:
            # TODO zmenit threshold na pocet vyskytov
            if minValueCounter > AoIdetails[1]:
                minValueCounter = AoIdetails[1]

        minValueDuration = commonAoIs[0][2]
        for AoIdetails in commonAoIs:
            if minValueDuration > AoIdetails[2]:
                minValueDuration = AoIdetails[2]

        return [minValueCounter, minValueDuration]


    def getNumberDurationOfAoIs(self, Sequences):
        AoIs = self.getExistingAoIList(Sequences)
        AoIcount = []
        for x in range(0, len(AoIs)):
            counter = 0
            duration = 0
            flagCounter = 0
            keys = list(Sequences)
            for y in range(0, len(keys)):
                if [s[0:2] for s in Sequences[keys[y]]].count(AoIs[x]) > 0:
                    counter = counter + [s[0:2] for s in Sequences[keys[y]]].count(AoIs[x])
                    duration = duration + sum([int(w[2]) for w in Sequences[keys[y]] if w[0:2] == AoIs[x]])
                    flagCounter = flagCounter + 1
            # TODO maybe change for: if flagCounter > len(keys)/2:
            # if flagCounter > len(keys)/2:
            if flagCounter == len(keys):
                AoIcount.append([AoIs[x], counter, duration, True])
            else:
                AoIcount.append([AoIs[x], counter, duration, False])
        return AoIcount


    def updateAoIsFlag(self, AoIs, threshold):
        for AoI in AoIs:
            if AoI[1] >= threshold[0] and AoI[2] >= threshold[1]:
                AoI[3] = True
        return AoIs


    def removeInsignificantAoIs(self, Sequences, AoIList):
        significantAoIs = []
        for AoI in AoIList:
            if AoI[3] == True:
                significantAoIs.append(AoI[0])

        keys = list(Sequences)
        for y in range(0, len(keys)):
            temp = []
            for k in range(0, len(Sequences[keys[y]])):
                try:
                    significantAoIs.index(Sequences[keys[y]][k][0:2])
                    temp.append(Sequences[keys[y]][k])
                except:
                    continue
            Sequences[keys[y]] = temp
        return Sequences


    def getExistingAoIList(self, Sequences):
        AoIlist = []
        keys = list(Sequences)
        for y in range(0, len(keys)):
            for x in range(0, len(Sequences[keys[y]])):
                try:
                    AoIlist.index(Sequences[keys[y]][x][0:2])
                except:
                    AoIlist.append(Sequences[keys[y]][x][0:2])
        return AoIlist


    def calculateNumberDurationOfFixationsAndNSV(self, Sequences):
        keys = list(Sequences)
        for x in range(0, len(keys)):
            myAbstractedSequence = []
            myAbstractedSequence = [Sequences[keys[x]][0][0:2] + [1] + [int(Sequences[keys[x]][0][2])]]
            for y in range(1, len(Sequences[keys[x]])):
                if myAbstractedSequence[len(myAbstractedSequence) - 1][0:2] != Sequences[keys[x]][y][0:2]:
                    myAbstractedSequence.append(Sequences[keys[x]][y][0:2] + [1] + [int(Sequences[keys[x]][y][2])])
                else:
                    myAbstractedSequence[len(myAbstractedSequence) - 1][2] = \
                    myAbstractedSequence[len(myAbstractedSequence) - 1][2] + 1
                    myAbstractedSequence[len(myAbstractedSequence) - 1][3] = \
                    myAbstractedSequence[len(myAbstractedSequence) - 1][3] + int(Sequences[keys[x]][y][2])

            Sequences[keys[x]] = myAbstractedSequence

        keys = list(Sequences)

        for x in range(0, len(keys)):
            for y in range(0, len(Sequences[keys[x]])):
                if len(Sequences[keys[x]]) < 2:
                    value = 0
                else:
                    value = 0.9 / (len(Sequences[keys[x]]) - 1)
                NSV = 1 - round(y, 2) * value
                Sequences[keys[x]][y] = Sequences[keys[x]][y] + [NSV]
        return Sequences


    def calculateTotalNumberDurationofFixationsandNSV(self, AoIList, Sequences):
        for x in range(0, len(AoIList)):
            duration = 0
            counter = 0
            totalNSV = 0

            flag = 0
            keys = list(Sequences)
            for y in range(0, len(keys)):
                for k in range(0, len(Sequences[keys[y]])):
                    if Sequences[keys[y]][k][0:2] == AoIList[x]:
                        counter += Sequences[keys[y]][k][2]
                        duration += Sequences[keys[y]][k][3]
                        totalNSV += Sequences[keys[y]][k][4]
                        flag += 1
            if flag == len(Sequences):
                AoIList[x] = AoIList[x] + [counter] + [duration] + [totalNSV] + [True]
            else:
                AoIList[x] = AoIList[x] + [counter] + [duration] + [totalNSV] + [False]

        return AoIList


    def getValueableAoIs(self, AoIList):
        commonAoIs = []
        valuableAoIs = []
        for myAoIdetail in AoIList:
            if myAoIdetail[5] == True:
                commonAoIs.append(myAoIdetail)

        minValue = commonAoIs[0][4]
        for AoIdetails in commonAoIs:
            if minValue > AoIdetails[4]:
                minValue = AoIdetails[4]

        for myAoIdetail in AoIList:
            if myAoIdetail[4] >= minValue:
                valuableAoIs.append(myAoIdetail)

        return valuableAoIs



    def get_edit_distances(self, scanpaths):
        # Store scanpaths as an array of string-converted original scanpaths
        scanpath_strs = convert_to_strs(scanpaths)

        # Calculate the edit distances
        # The order of records in scanpaths and scanpath_strs must be the same!
        calc_similarity(scanpath_strs)

        for i_first in range(0, len(scanpath_strs)):
            # Save the calculations to the original scanpaths object
            scanpaths[i_first]['similarity'] = scanpath_strs[i_first]['similarity']



    def get_scanpaths_json(self):
        myErrorRateArea = self.my_env.get_error_rate_area()
        mySequences = self.createSequences( myErrorRateArea)

        keys = list(mySequences)
        for y in range(0, len(keys)):
            mySequences[keys[y]] = mySequences[keys[y]].split('.')
            del mySequences[keys[y]][len(mySequences[keys[y]]) - 1]
        for y in range(0, len(keys)):
            for z in range(0, len(mySequences[keys[y]])):
                mySequences[keys[y]][z] = mySequences[keys[y]][z].split('-')

        formatted_sequences = self.my_dataset.get_formatted_sequences(mySequences)

        self.get_edit_distances(formatted_sequences)
        self.my_dataset.get_max_similarity(formatted_sequences)
        self.my_dataset.get_min_similarity(formatted_sequences)

        ret_dataset = {
            'userScanpaths': formatted_sequences,
            'visualMain': self.my_dataset.file_path_visual,
        }

        return json.dumps(ret_dataset)

    # STA Algorithm
    def sta_run(self, simplify=False, fixDurThreshold=None, mod=1):
        """
        Args:
            simplify: reduction of repeated characters
            fixDurThreshold: miniimal length of fixation
            mod: 1 create scanpath from AOI
                 2 create scanpath based on length of fixation
                 3 create scanpath based on duration of fixation
                 4 create scanpath based on relative angles
                 5 create scanpath based on absolute angles

        Returns:

        """
        mySequences = createSequences(self.my_dataset, mod)
        temp = dict(mySequences)
        for k, v in temp.items():
            if v == "":
                del mySequences[k]
        """ Write Sequences of participants to console"""
        # for keys,values in mySequences.items():
        #     print(keys)
        #     print(values)

        mySequences = getArrayRepresentationOfSequence(mySequences)

        if fixDurThreshold is not None:
            mySequences = applyFixDurationThreshold(mySequences, fixDurThreshold)

        if simplify:
            mySequences = simplifySequence(mySequences)

        maxFinalScanpathLength = int(parser.get('sequence', 'maxFinalScanpathLength'))
        #shorten the sequnces
        for key, value in mySequences.items():
            if len(value) > 10:
                mySequences[key] = value[:maxFinalScanpathLength]
        filteredSequences = filterOutParticipantsWithLowSimilarityToOthers(mySequences, self.my_dataset.aois)

        # First-Pass
        mySequences_num = {}
        keys = list(filteredSequences)
        for y in range(0, len(keys)):
            mySequences_num[keys[y]] = self.getNumberedSequence(filteredSequences[keys[y]])

        myImportanceThreshold = self.calculateImportanceThreshold(mySequences_num)
        if myImportanceThreshold == None:
            res_data = calcSimilarityForDataset(mySequences, "", self.my_dataset.aois)
            self.printResults(res_data)
            res_data["sequences"] = mySequences
            return res_data

        myImportantAoIs = self.updateAoIsFlag(self.getNumberDurationOfAoIs(mySequences_num), myImportanceThreshold)
        myNewSequences = self.removeInsignificantAoIs(mySequences_num, myImportantAoIs)

        # Second-Pass
        myNewAoIList = self.getExistingAoIList(myNewSequences)

        # B gets flagged as false
        myNewAoIList = self.calculateTotalNumberDurationofFixationsandNSV(myNewAoIList,
                                                                     self.calculateNumberDurationOfFixationsAndNSV(myNewSequences))
        # B gets removed
        myFinalList = self.getValueableAoIs(myNewAoIList)

        myFinalList.sort(key=lambda x: (x[4], x[3], x[2]))
        myFinalList.reverse()

        commonSequence = []
        for y in range(0, len(myFinalList)):
            commonSequence.append(myFinalList[y][0])

        common_scanpath = self.getAbstractedSequence(commonSequence)


        res_data = calcSimilarityForDataset(mySequences, common_scanpath, self.my_dataset.aois)

        self.printResults(res_data)
        # to get JSON use return str(sta_run()) when calling this alg
        # return json.dumps(res_data)
        res_data["sequences"] = mySequences
        return res_data

    def printResults(self, results):
        print("STA")
        print("-----------------------------------------------")
        # print(results["fixations"])
        for keys,values in results.items():
            print(keys)
            print(values)

