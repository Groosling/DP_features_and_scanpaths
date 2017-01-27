from math import *
from ConfigParser import SafeConfigParser
import codecs
from operations.Operations import *

AOIS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
parser = SafeConfigParser()
# Open the file with the correct encoding
with codecs.open('config.ini', 'r', encoding='utf-8') as f:
    parser.readfp(f)

def createSequencesBasedOnVisualElements(my_dataset):
    max_AOI = int(parser.get('sequence', 'maxAoi'))
    errorRateArea = int(parser.get('sequence', 'errorRateArea'))
    Sequences = {}
    Participants = my_dataset.participants
    myAoIs = my_dataset.aois
    keys = Participants.keys()
    for y in range(0, len(keys)):
        sequence = ""
        counter = 0
        for z in range(0, len(Participants[keys[y]])):
            if counter == max_AOI:
                break
            tempAoI = ""
            tempDuration = 0

            for k in range(0, len(myAoIs)):
                if float(Participants[keys[y]][z][3]) >= (float(myAoIs[k][1]) - errorRateArea) and float(
                        Participants[keys[y]][z][3]) < (
                ((float(myAoIs[k][1]) - errorRateArea) + (float(myAoIs[k][2]) + 2 * errorRateArea))) and float(
                        Participants[keys[y]][z][4]) >= (float(myAoIs[k][3]) - errorRateArea) and float(
                        Participants[keys[y]][z][4]) < (
                ((float(myAoIs[k][3]) - errorRateArea) + (float(myAoIs[k][4]) + 2 * errorRateArea))):
                    tempAoI = tempAoI + myAoIs[k][5]
                    tempDuration = int(Participants[keys[y]][z][2])


            # my solution compare sum of distances to four corners
            if len(tempAoI) > 1:
                tempAoI = getCloserAOI(Participants[keys[y]][z],myAoIs, tempAoI)

            if len(tempAoI) != 0:
                counter = counter + 1
                sequence = sequence + tempAoI + "-" + str(tempDuration) + "."
                if counter == max_AOI:
                    break

        Sequences[keys[y]] = sequence
    return Sequences

def getCloserAOI(Participants_pos, myAoIs, tempAoI):
    min_distamce =9999
    closest_AOI = ""
    temp_distannce = []
    sums_of_distances = {}
    for m in range(0, len(tempAoI)):
        for n in range(0, len(myAoIs)):
            if tempAoI[m] == myAoIs[n][5]:
                temp_distannce = []
                # sum distance of all 4 corners
                # up, left
                temp_distannce.append(sqrt(pow(float(Participants_pos[3]) - float(myAoIs[n][1]), 2) +
                                           pow(float(Participants_pos[4]) - float(myAoIs[n][3]), 2)))
                # up right
                temp_distannce.append(sqrt(pow(float(Participants_pos[3]) - (float(myAoIs[n][1]) + float(myAoIs[n][2])), 2) +
                                           pow(float(Participants_pos[4]) - float(myAoIs[n][3]), 2)))
                # down left
                temp_distannce.append(sqrt(pow(float(Participants_pos[3]) - (float(myAoIs[n][1])), 2) +
                                           pow(float(Participants_pos[4]) - (float(myAoIs[n][3]) + float(myAoIs[n][4])), 2)))
                # down, right
                temp_distannce.append(sqrt(pow(float(Participants_pos[3]) - (float(myAoIs[n][1]) + float(myAoIs[n][2])), 2) +
                                           pow(float(Participants_pos[4]) - (float(myAoIs[n][3]) + float(myAoIs[n][4])), 2)))
                sums_of_distances[tempAoI[m]] = sum(temp_distannce)
                break
    # print "ss"
    # return key of minimal value in dictionary
    return min(sums_of_distances, key=sums_of_distances.get)

def getArrayRepresentationOfSequence(mySequences):
    """

    Args:
        sequence: String format of sequence

    Returns: array representation of sequence

    """
    keys = mySequences.keys()
    # odstranenie bodky na konci
    for y in range(0, len(keys)):
        mySequences[keys[y]] = mySequences[keys[y]].split('.')
        del mySequences[keys[y]][len(mySequences[keys[y]]) - 1]
    #  rozdeli D-100 na pole z dvomi prvkami D a 100
    for y in range(0, len(keys)):
        for z in range(0, len(mySequences[keys[y]])):
            mySequences[keys[y]][z] = mySequences[keys[y]][z].split('-')
    return mySequences

def simplifySequence(aSequence):
    """
    Groups same fixation in a row AAABBB ->  AB and sums up the fixDur
    Args:
        aSequence: dictionary of array representation of sequences

    Returns:
        Processed sequence in array representation
    """
    keys = aSequence.keys()
    for y in range(0, len(keys)):
        simpleSequence = []
        lastAOI = "0"
        for z in range(0, len(aSequence[keys[y]])):
            if aSequence[keys[y]][z][0] == lastAOI:
                simpleSequence[len(simpleSequence) - 1][1] = str(int(simpleSequence[len(simpleSequence) - 1][1]) + int(aSequence[keys[y]][z][1]))
            else:
                simpleSequence.append([aSequence[keys[y]][z][0], aSequence[keys[y]][z][1]])
                lastAOI = aSequence[keys[y]][z][0]
        aSequence[keys[y]] = simpleSequence
    return aSequence


def applyFixDurationThreshold(aSequence, threshold = 80):
    """
    Delete fixations shorter than defined threshold
    Args:
        aSequence: dictionary of array representation of sequences
        threshold: default 80 ms

    Returns:
        Processed sequence in array representation
    """
    keys = aSequence.keys()
    for y in range(0, len(keys)):
        processedArray = []
        for z in range(0, len(aSequence[keys[y]])):
            if int(aSequence[keys[y]][z][1]) > threshold:
                processedArray.append(aSequence[keys[y]][z])
        aSequence[keys[y]] = processedArray
    return aSequence

def getStringRepresentation(aSequence):
    """
    Returns string representation without duration of fixations
    Args:
        aSequence: dictionary of array representation of sequeces

    Returns:

    """
    newDict  = {}
    keys = aSequence.keys()
    for y in range(0, len(keys)):
        sequence = ""
        for z in range(0, len(aSequence[keys[y]])):
            sequence = sequence + aSequence[keys[y]][z][0]
        newDict[keys[y]] = sequence
    return newDict

def createSequencesBasedOnDistances(my_dataset):
    """
    Create Scanpath from sacade lengths(distances between fixations)
    Args:
        my_dataset: dataset

    Returns:

    """
    aoiRange = int(parser.get('aoiRange', 'saccadeLength'))
    max_AOI = int(parser.get('sequence', 'maxAoi'))
    sequences = {}
    participants = my_dataset.participants
    myAoIs = my_dataset.aois
    keys = participants.keys()
    for y in range(0, len(keys)):
        sequence = ""
        for z in range(0, min(len(participants[keys[y]]) - 1, max_AOI)):
           tempdist = calculateDistance(int(participants[keys[y]][z][3]), int(participants[keys[y]][z][4]),
                                        int(participants[keys[y]][z + 1][3]), int(participants[keys[y]][z + 1][4]))
           sequence = sequence + getAOIBasedOnRange(tempdist, aoiRange) + "-" + str(int(participants[keys[y]][z + 1][1]) - int(participants[keys[y]][z][1])) + "."
        sequences[keys[y]] = sequence
    return sequences


def getAOIBasedOnRange(value, aoiRange):
    """
    Determine AOI based on range
    Args:
        value: distance between fixations
        range: range of distance for single AOI

    Returns: character representation of AOI
    """
    return AOIS[int(value / aoiRange)]

def createSequencesBasedOnFixatonDurations(my_dataset):
    """
    Create Scanpath from fixations duration
    Args:
        my_dataset: dataset
    Returns:

    """
    aoiRange = int(parser.get('aoiRange', 'fixationDuration'))
    max_AOI = int(parser.get('sequence', 'maxAoi'))
    sequences = {}
    participants = my_dataset.participants
    myAoIs = my_dataset.aois
    keys = participants.keys()
    for y in range(0, len(keys)):
        sequence = ""
        for z in range(0, min(len(participants[keys[y]]) - 1, max_AOI)):
           sequence = sequence + getAOIBasedOnRange(int(participants[keys[y]][z][2]), aoiRange) +\
                      "-" + participants[keys[y]][z][2] + "."
        sequences[keys[y]] = sequence
    return sequences



def createSequencesBasedOnRelativeAngle(my_dataset):
    """
    Create Scanpath from absolute angles of saccades
    Args:
        my_dataset: dataset
    Returns:

    """
    aoiRange = int(parser.get('aoiRange', 'relativeAngle'))
    max_AOI = int(parser.get('sequence', 'maxAoi'))
    sequences = {}
    participants = my_dataset.participants
    myAoIs = my_dataset.aois
    keys = participants.keys()
    for y in range(0, len(keys)):
        # TODO vec1 = vec2 at the beginning of the cycle ... better time complexity
        # TODO add condition if sequence has two elements or so.. return empty sequence.. depends ond cycle
        sequence = ""
        for z in range(0, min(len(participants[keys[y]]) - 2, max_AOI)):
            # calculates vector between curent point and next one
            vec1 = calculateVector(int(participants[keys[y]][z][3]), int(participants[keys[y]][z][4]),
                                   int(participants[keys[y]][z + 1][3]), int(participants[keys[y]][z + 1][4]))
            # calculates vector between next point and next next one
            vec2 = calculateVector(int(participants[keys[y]][z + 1][3]), int(participants[keys[y]][z + 1][4]),
                                   int(participants[keys[y]][z + 2][3]), int(participants[keys[y]][z + 2][4]))
            angle = calculateAngle(vec1, vec2)
            # duration is calculated as sum of both sacades durations
            sequence = sequence + getAOIBasedOnRange(angle, aoiRange) + "-" + str(int(participants[keys[y]][z + 2][1]) - int(participants[keys[y]][z][1])) + "."
        sequences[keys[y]] = sequence
    return sequences


def createSequencesBasedOnAbsoluteAngle(my_dataset):
    """
    Create Scanpath from absolute angles of saccades
    Args:
        my_dataset: dataset

    Returns:

    """
    aoiRange = int(parser.get('aoiRange', 'absoluteAngle'))
    max_AOI = int(parser.get('sequence', 'maxAoi'))
    sequences = {}
    participants = my_dataset.participants
    myAoIs = my_dataset.aois
    keys = participants.keys()
    for y in range(0, len(keys)):
        sequence = ""
        for z in range(0, min(len(participants[keys[y]]) - 1, max_AOI)):
            # calculates vector between curent point and next one
            vec1 = calculateVector(int(participants[keys[y]][z][3]), int(participants[keys[y]][z][4]),
                                   int(participants[keys[y]][z + 1][3]), int(participants[keys[y]][z + 1][4]))
            # default vector (right direction)
            vec2 = calculateVector(0, 0, 1, 0)
            angle = calculateAngle(vec1, vec2)
            # duration is calculated as sum of both sacades durations
            sequence = sequence + getAOIBasedOnRange(angle, aoiRange) + "-" + str(int(participants[keys[y]][z + 1][1]) - int(participants[keys[y]][z][1])) + "."
        sequences[keys[y]] = sequence
    return sequences

def createSequences(my_dataset, mod):
    """
    Based on mod creates sequences from dataset
    Args:
        my_dataset: dataset
        mod:     1 vytvori standardny scanpath z AOI
                 2 vytvori scanpah na zaklade dlzky sakad
                 3 vytvori scanpath na zaklade dlzky trvania fixacii
                 4 vytvori scanpath na zaklade relativnych uhlov sakad0
                 5 vytvori scanpath na zaklade absolutnych uhlov sakad

    Returns:

    """
    case = {
      1: createSequencesBasedOnVisualElements,
      2: createSequencesBasedOnDistances,
      3: createSequencesBasedOnFixatonDurations,
      4: createSequencesBasedOnRelativeAngle,
      5: createSequencesBasedOnAbsoluteAngle,
    }
    myFunc = case[mod]
    return myFunc(my_dataset)