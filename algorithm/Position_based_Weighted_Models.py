import operator

from structure import Sequence
from algorithm.StringEditAlgs import *

class Position_based_Weighted_Models:
    def __init__(self, my_dataset):
        parser = ConfigParser()
        # Open the file with the correct encoding
        with codecs.open('config.ini', 'r', encoding='utf-8') as f:
            parser.readfp(f)
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
        mySequences = Sequence.createSequences(self.my_dataset, mod)
        temp = dict(mySequences)
        for k, v in temp.items():
            if v == "":
                del mySequences[k]
        """ Write Sequences of participants to console"""
        # for keys, values in mySequences.items():
        #     print(keys)
        #     print(values)

        mySequences = Sequence.getArrayRepresentationOfSequence(mySequences)

        if fixDurThreshold is not None:
            mySequences = Sequence.applyFixDurationThreshold(mySequences, fixDurThreshold)

        if simplify:
            mySequences = simplifySequence(mySequences)

        maxFinalScanpathLength = int(parser.get('sequence', 'maxFinalScanpathLength'))
        #shorten the sequnces
        for key, value in mySequences.items():
            if len(value) > 10:
                mySequences[key] = value[:maxFinalScanpathLength]
        filteredSequences = filterOutParticipantsWithLowSimilarityToOthers(mySequences, self.my_dataset.aois)

        keys = list(filteredSequences)
        # creating dictionary of AOIS
        aois = {}
        for item in self.my_dataset.aois:
            aois[item[5]] = 0.0

        # vytvorenie histogramu
        for y in range(0, len(keys)):
             if len(filteredSequences[keys[y]]) > 2:
                 aois[filteredSequences[keys[y]][0][0]] = aois[filteredSequences[keys[y]][0][0]] + 1
                 aois[filteredSequences[keys[y]][1][0]] = aois[filteredSequences[keys[y]][1][0]] + 0.5
                 aois[filteredSequences[keys[y]][2][0]] = aois[filteredSequences[keys[y]][2][0]] + 0.2

        # zoradi dictionary do pola
        sorted_d = sorted(aois.items(), reverse=True, key=operator.itemgetter(1))

        # create printable result
        result = ""
        for i in range (0, 3):
            result =  result + sorted_d[i][0]

        res_data = calcSimilarityForDataset(mySequences, list(result),self.my_dataset.aois)
        print("PBWM")
        print("-----------------------------------------------")
        print(res_data["fixations"])
        # for keys,values in res_data.items():
        #     print(keys)
        #     print(values)
        res_data["sequences"] = mySequences
        return res_data
        # return result[:len(result)-1]
