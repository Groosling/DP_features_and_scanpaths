import operator

from structure import Sequence


class Position_based_Weighted_Models:
    def __init__(self, my_dataset):
        self.my_dataset = my_dataset

    def run_PBWM(self, simplify = False, fixDurThreshold = None, mod = 1):
        """
        Args:
            simplify: urcuje ci redukovat opakujuce sa fixacie za sebou na jednu
            fixDurThreshold: minimalna dlzka trvania fixacie
            mod: 1 vytvori standardny scanpath z AOI
                 2 vytvori scanpah na zaklade dlzky sakad
                 3 vytvori scanpath na zaklade dlzky trvania fixacii
                 4 vytvori scanpath na zaklade relativnych uhlov sakad
                 5 vytvori scanpath na zaklade absolutnych uhlov sakad

        Returns:

        """
        errorRateArea = 0
        mySequences = {
              1: Sequence.createSequences(self.my_dataset, errorRateArea),
              2: Sequence.createSequencesBasedOnDistances(self.my_dataset),
              3: Sequence.createSequencesBasedOnFixatonDurations(self.my_dataset),
              4: Sequence.createSequencesBasedOnRelativeAngle(self.my_dataset),
              5: Sequence.createSequencesBasedOnAbsoluteAngle(self.my_dataset),
            }[mod]
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
