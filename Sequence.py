from math import *



def createSequences(my_dataset, errorRateArea, max_AOI = 10):
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
        aSequence: array representation of sequence

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
        aSequence: array representation of sequence
        threshold: default 80 ms

    Returns:
        Processed sequence in array representation
    """
    keys = aSequence.keys()
    for y in range(0, len(keys)):
        proessedArray = []
        for z in range(0, len(aSequence[keys[y]])):
            if int(aSequence[keys[y]][z][1]) > threshold:
                proessedArray.append(aSequence[keys[y]][z])
        aSequence[keys[y]] = proessedArray
    return aSequence








