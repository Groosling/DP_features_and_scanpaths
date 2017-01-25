from structure import Sequence

from operator import itemgetter, attrgetter


class Dotplot:

    def __init__(self, my_dataset, my_env):
        self.my_dataset = my_dataset
        self.my_env = my_env

    def dotplotListofLists(self, sequenceX, sequenceY):
        # fill matrix with zeroes
        dotplotMatrix = [[0 for x in sequenceX] for y in sequenceY]
        # put 1 on matching positions
        for xIndex, valueX in enumerate(sequenceX):
            for yIndex, valueY in enumerate(sequenceY):
                if valueX == valueY:
                    dotplotMatrix[yIndex][xIndex] = 1
        return dotplotMatrix

    def findLongestCommonSequence(self, dotplotMatrix, sequenceX):

        commonSubSequence = ""
        lengthSubsequence = 0

        # right part of matrix
        for i in range(0, len(dotplotMatrix[0])):
            # reamining x length or height of matrix
            sum = 0
            for j in range(0, min(len(dotplotMatrix[0]) - i, len(dotplotMatrix))):
                sum = sum + dotplotMatrix[j][i + j]
                # print dotplotMatrix[j][i + j]
            if sum > lengthSubsequence:
                # sequence created by characters with value 1
                lengthSubsequence = sum
                commonSubSequence = ""
                for j in range(0, min(len(dotplotMatrix[0]) - i, len(dotplotMatrix))):
                    if dotplotMatrix[j][i + j] == 1:
                        commonSubSequence = commonSubSequence + sequenceX[i + j]


        # left part of the matrix
        for i in range(0, len(dotplotMatrix)):
            sum = 0
            for j in range(0, min(len(dotplotMatrix) - i, len(dotplotMatrix[0]))):
                sum = sum + dotplotMatrix[i + j][j]
                # print dotplotMatrix[i + j][j]

            if sum > lengthSubsequence:
                # sequence created by characters with value 1
                lengthSubsequence = sum
                commonSubSequence = ""
                for j in range(0, min(len(dotplotMatrix) - i, len(dotplotMatrix[0]))):
                    if dotplotMatrix[i + j][j] == 1:
                        commonSubSequence = commonSubSequence + sequenceX[j]

        return commonSubSequence

    def findCommonSequence(self, stringSequences):
        """
        Finds the most similar seuecnces in dictionary and determines their common scanpath
        Args:
            stringSequences: dictionary of sequences in string format

        Returns:

        """
        keys = stringSequences.keys()
        while len(keys) > 1:
            commonSequences = []
            for y in range(0, len(keys)):
                sequence = ""
                for z in range(y + 1, len(keys)):
                    #  create matrix
                    matrix = self.dotplotListofLists(stringSequences[keys[y]], stringSequences[keys[z]])
                    # for row in matrix:
                    #     for column in row:
                    #         print column,
                    #     print

                    # find longest common subsequence
                    subSequence = self.findLongestCommonSequence(matrix, stringSequences[keys[y]])
                    commonSequences.append([keys[y], keys[z], subSequence, len(subSequence)])

            # replace 2 most similar sequences with their common sequence
            commonSequences = sorted(commonSequences, reverse=True, key=itemgetter(3))
            if commonSequences[0][2] == "":
                return "Dotplot common scanpath doesn't exist."

            del stringSequences[commonSequences[0][0]]
            del stringSequences[commonSequences[0][1]]
            stringSequences[commonSequences[0][0] + commonSequences[0][1]] = commonSequences[0][2]
            keys = stringSequences.keys()
        return stringSequences[keys[0]]



    def runDotplot(self, simplify = False, fixDurThreshold = None, mod = 1):
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

        # mySequences = Sequence.createSequences(self.my_dataset, errorRateArea)
        for keys, values in mySequences.items():
            print(keys)
            print(values)
        mySequences = Sequence.getArrayRepresentationOfSequence(mySequences)

        if fixDurThreshold is not None:
            mySequences = Sequence.applyFixDurationThreshold(mySequences, fixDurThreshold)

        if simplify:
            mySequences = Sequence.simplifySequence(mySequences)

        stringSequences = Sequence.getStringRepresentation(mySequences)
        return self.findCommonSequence(stringSequences)
