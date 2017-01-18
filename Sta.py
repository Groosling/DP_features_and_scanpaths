from __future__ import division
from stringEditAlgs import *
from Dataset import *
from Environment import *
import json
from Sequence import *


class Sta:
    def __init__(self, my_dataset, my_env):
        self.my_dataset = my_dataset
        self.my_env = my_env



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
            print "No shared instances!"
            exit(1)

        minValueCounter = commonAoIs[0][1]
        for AoIdetails in commonAoIs:
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
            keys = Sequences.keys()
            for y in range(0, len(keys)):
                if [s[0:2] for s in Sequences[keys[y]]].count(AoIs[x]) > 0:
                    counter = counter + [s[0:2] for s in Sequences[keys[y]]].count(AoIs[x])
                    duration = duration + sum([int(w[2]) for w in Sequences[keys[y]] if w[0:2] == AoIs[x]])
                    flagCounter = flagCounter + 1

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

        keys = Sequences.keys()
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
        keys = Sequences.keys()
        for y in range(0, len(keys)):
            for x in range(0, len(Sequences[keys[y]])):
                try:
                    AoIlist.index(Sequences[keys[y]][x][0:2])
                except:
                    AoIlist.append(Sequences[keys[y]][x][0:2])
        return AoIlist


    def calculateNumberDurationOfFixationsAndNSV(self, Sequences):
        keys = Sequences.keys()
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

        keys = Sequences.keys()

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
            keys = Sequences.keys()
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


    # TODO presunut do dataset classy
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

        keys = mySequences.keys()
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
    def sta_run(self, simplify = False, fixDurThreshold = None):
        # myErrorRateArea = my_env.get_error_rate_area()
        myErrorRateArea = 0
        mySequences = createSequences(self.my_dataset, myErrorRateArea)

        print "povodne sekvencie"
        for keys,values in mySequences.items():
            print(keys)
            print(values)

        mySequences = getArrayRepresentationOfSequence(mySequences)

        if fixDurThreshold is not None:
            mySequences = applyFixDurationThreshold(mySequences, fixDurThreshold)

        if simplify:
            mySequences = simplifySequence(mySequences)

        # First-Pass
        mySequences_num = {}
        keys = mySequences.keys()
        for y in range(0, len(keys)):
            mySequences_num[keys[y]] = self.getNumberedSequence(mySequences[keys[y]])

        myImportanceThreshold = self.calculateImportanceThreshold(mySequences_num)
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

        formatted_sequences = self.my_dataset.get_formatted_sequences(mySequences)

        # Store scanpaths as an array of string-converted original scanpaths
        scanpath_strs = convert_to_strs(formatted_sequences)

        common_scanpath = self.getAbstractedSequence(commonSequence)
        res_data = {
            'fixations': common_scanpath,
            'similarity': calc_similarity_to_common(scanpath_strs, common_scanpath)
        }

        # to get JSON use return str(sta_run()) when calling this alg
        # return json.dumps(res_data)
        for keys,values in res_data.items():
            print(keys)
            print(values)
    """  ked uz mas custom scanpath """
    def custom_run(self, custom_scanpath):
        myErrorRateArea = self.my_env.get_error_rate_area()
        mySequences = createSequences(self.my_dataset,myErrorRateArea)

        keys = mySequences.keys()
        for y in range(0, len(keys)):
            mySequences[keys[y]] = mySequences[keys[y]].split('.')
            del mySequences[keys[y]][len(mySequences[keys[y]]) - 1]
        for y in range(0, len(keys)):
            for z in range(0, len(mySequences[keys[y]])):
                mySequences[keys[y]][z] = mySequences[keys[y]][z].split('-')

        formatted_sequences = self.my_dataset.get_formatted_sequences(mySequences)

        # Store scanpaths as an array of string-converted original scanpaths
        scanpath_strs = convert_to_strs(formatted_sequences)

        custom_scanpath_arr = []
        for i in range (0, len(custom_scanpath)):
            custom_scanpath_arr.append(custom_scanpath[i])

        res_data = {
            'fixations': custom_scanpath_arr,
            'similarity': calc_similarity_to_common(scanpath_strs, custom_scanpath_arr)
        }

        # to get JSON use return str(sta_run()) when calling this alg
        return json.dumps(res_data)

if __name__ == "__main__":
    # Storage for all loaded data
    my_dataset = Dataset('data/template_sta/scanpaths/DOD2016_fixations_2_participants.tsv',
                         'data/template_sta/regions/seg_FIIT_page.txt',
                         'static/images/datasets/template_sta/placeholder.png',
                         'http://www.fiit.stuba.sk/')
    # Environment in which the eye tracking experiment was performed
    my_env = Environment(0.5, 60, 1920, 1200, 17)
    # sta_run(my_env, my_dataset)
    # custom_run()