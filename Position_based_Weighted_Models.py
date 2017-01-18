import Sequence
import operator


class Position_based_Weighted_Models:
    def __init__(self, my_dataset):
        self.my_dataset = my_dataset

    def run_PBWM(self, simplify = False, fixDurThreshold = None):
        errorRateArea = 0
        mySequences = Sequence.createSequences(self.my_dataset, errorRateArea)
        for keys, values in mySequences.items():
            print(keys)
            print(values)

        mySequences = Sequence.getArrayRepresentationOfSequence(mySequences)

        if fixDurThreshold is not None:
            mySequences = Sequence.applyFixDurationThreshold(mySequences, fixDurThreshold)

        if simplify:
            mySequences = Sequence.simplifySequence(mySequences)

        keys = mySequences.keys()
        # creating dictionary of AOIS
        aois = {}
        for item in self.my_dataset.aois:
            aois[item[5]] = 0.0

        # vytvorenie histogramu
        for y in range(0, len(keys)):
             aois[mySequences[keys[y]][0][0]] = aois[mySequences[keys[y]][0][0]] + 1
             aois[mySequences[keys[y]][1][0]] = aois[mySequences[keys[y]][1][0]] + 0.5
             aois[mySequences[keys[y]][2][0]] = aois[mySequences[keys[y]][2][0]] + 0.2

        # zoradi dictionary do pola
        sorted_d = sorted(aois.items(), reverse=True, key=operator.itemgetter(1))

        # create printable result
        result = ""
        for i in range (0, 3):
            result =  result + sorted_d[i][0] +","

        return result[:len(result)-1]
