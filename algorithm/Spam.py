import os
from subprocess import check_output
from structure.Sequence import *
from algorithm.StringEditAlgs import *


from configparser import ConfigParser
import codecs



class Spam:
    def __init__(self, my_dataset, my_env):
        parser = ConfigParser()
        # Open the file with the correct encoding
        with codecs.open('config.ini', 'r', encoding='utf-8') as f:
            parser.readfp(f)
        self.my_dataset = my_dataset
        self.my_env = my_env

    def runSPAM(self, inputFilePath, outputFilePath):
        check_output("java -jar " + parser.get('spam', 'lib') + " run SPAM " + inputFilePath + " " + outputFilePath + " 0.5 2 6 1 true", shell=True).decode()

    def spamRun(self, simplify=False, fixDurThreshold=None, mod=1):
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

        for keys,values in mySequences.items():
            print(keys)
            print(values)

        mySequences = getArrayRepresentationOfSequence(mySequences)

        if fixDurThreshold is not None:
            mySequences = applyFixDurationThreshold(mySequences, fixDurThreshold)

        if simplify:
            mySequences = simplifySequence(mySequences)
        participantsList, mapOfAois = self.codeAoiInNumbers(mySequences)

        INPUT_FILE = parser.get('spam', 'inputFilepath')
        OUTPUT_FILE = parser.get('spam', 'outputFilepath')

        # ---------- Writing to FILE START------------------
        try:
            file = open(INPUT_FILE, 'w+')
        except IOError:
            print ("File can not be open")
            return

        for participant in participantsList:
            line  = self.encodeParticipant(participant, mapOfAois )
            file.write(line)
        file.close()

        # ---------- Writing to FILE END------------------

        self.runSPAM(INPUT_FILE, OUTPUT_FILE)
        try:
            os.remove(INPUT_FILE)
        except OSError:
            pass

    # ---------- Read FILE START------------------
        try:
            file = open(OUTPUT_FILE, 'r')
        except IOError:
            print("File can not be open")
            return
        common_scanpaths = []
        for line in file:
        # line = file.readline()
            common_scanpaths.append(self.decodeParticipant(line, mapOfAois))

        file.close()
        try:
            os.remove(OUTPUT_FILE)
        except OSError:
            pass

    # ---------- Read FILE END------------------


        aoisPositionsDict = {}
        for scanpath  in common_scanpaths:
            scanpath["similarity"] = calcSimilarityForDataset(mySequences, scanpath["scanpath"], self.my_dataset.aois)

        maxSimilarityItem = max(common_scanpaths, key=lambda x: x['similarity']['OverAllSimilarity'])

        for keys,values in maxSimilarityItem['similarity'].items():
            print(keys)
            print(values)
        return maxSimilarityItem['similarity']


    def encodeParticipant(self, paticitpant, mapOfAois ):
        line = ""
        for item in paticitpant:
            line = line + str(mapOfAois[item]) + " -1 "
        return line + "-2\n"

    def decodeParticipant(self, line, mapOfAois):
        mapOfAoisReverted = {v: k for k, v in mapOfAois.items()}
        participant = {}
        start = "#SUP: "
        end = " #SID:"
        if line != "":
            splitLine = line.split(' -1 ')
            splitLine = splitLine[:-1]
            participant["scanpath"] = [mapOfAoisReverted[int(item)] for item in splitLine]
            participant["support"] = int((line.split(start))[1].split(end)[0])
            return participant
        else:
            return []

    def codeAoiInNumbers(self, sequence):
        mapOfAois = {}
        participantsList = []
        for participant in sequence:
            aoiList = []
            for aoi in sequence[participant]:
                if aoi[0] not in mapOfAois.keys():
                    mapOfAois[aoi[0]] = len(mapOfAois.keys())
                aoiList.append(aoi[0])
            participantsList.append(aoiList)

        return participantsList, mapOfAois


