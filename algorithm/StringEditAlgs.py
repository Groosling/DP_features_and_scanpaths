from __future__ import division
from structure.Sequence import *
import numpy as np
from configparser import ConfigParser
import codecs

parser = ConfigParser()
# Open the file with the correct encoding
with codecs.open('config.ini', 'r', encoding='utf-8') as f:
    parser.readfp(f)


def convert_to_strs(scanpaths):
    scanpath_strs = []
    # Extract scanpaths as raw string sequences with identifiers
    for act_scanpath in scanpaths:
        act_scanpath_str = ''
        for fixation in act_scanpath['fixations']:
            act_scanpath_str += fixation[0]
        # Store the identifier and extracted string sequence in an object
        temp_scanpath = {
            'identifier': act_scanpath['identifier'],
            'raw_str': act_scanpath_str
        }
        # Push the object to the array
        scanpath_strs.append(temp_scanpath)

    return scanpath_strs


def calc_similarity(scanpath_strs):
    for i_first in range(0, len(scanpath_strs)):
        # Each scanpath has a similarity object - similarity[id] represents
        # the level of similarity to the scanpath identified by id

        # If the similarity object of first scanpath does not exist yet - create it
        if not scanpath_strs[i_first].get('similarity'):
            scanpath_strs[i_first]['similarity'] = {}
        for i_second in range(i_first + 1, len(scanpath_strs)):
            # Calculate the edit (Levenshtein) distance of first and second string sequence
            edit_distance = levenshtein(scanpath_strs[i_first]['raw_str'], scanpath_strs[i_second]['raw_str'])

            # Calculate similarity as edit 1 - distance/length(longer string)
            # Non-integer division (python future import)
            len_first = len(scanpath_strs[i_first]['raw_str'])
            len_second = len(scanpath_strs[i_second]['raw_str'])
            similarity = 1 - (edit_distance / (len_first if len_first > len_second else len_second))
            # Set similarity as percentage
            similarity *= 100

            identifier_first = scanpath_strs[i_first]['identifier']
            identifier_second = scanpath_strs[i_second]['identifier']

            # Set the similarity for the first scanpath
            scanpath_strs[i_first]['similarity'][identifier_second] = similarity

            # If the similarity object of second scanpath does not exist yet - create it
            if not scanpath_strs[i_second].get('similarity'):
                scanpath_strs[i_second]['similarity'] = {}

            # Set the same similarity as above for the second scanpath
            scanpath_strs[i_second]['similarity'][identifier_first] = similarity


def calc_similarity_to_common(scanpath_strs, scanpath_common, substitution_Matrix, aoisPositionsDict):
    # Object storing similarities of each individual scanpath to the common one
    similarity_obj = {}
    # Calculate similarity of each scanpath to the common (trending) scanpath
    common = ''.join(str(ch) for ch in scanpath_common)
    for scanpath_str in scanpath_strs:
        similarity_obj[scanpath_str['identifier']] = calcSimilarityBetweenTwoScanpaths(scanpath_str["raw_str"], common, substitution_Matrix, aoisPositionsDict)

    return similarity_obj

def calcSimilarityBetweenTwoScanpaths(scanpath1, scanpath2, substitution_Matrix, aoisPositionsDict):
    len_common = len(scanpath2)
    edit_distance = levenshtein(scanpath1, scanpath2, substitution_Matrix, aoisPositionsDict)
    len_act = len(scanpath1)
    # Calculate similarity as edit 1 - distance/length(longer string)
    # Non-integer division (python future import)
    similarity = 1 - (edit_distance / (len_act if len_act > len_common else len_common))
    # Set similarity as percentage
    return similarity * 100


def levenshtein(s1, s2, substitution_Matrix, aoisPositionsDict):

    if len(s1) < len(s2):
        return levenshtein(s2, s1, substitution_Matrix, aoisPositionsDict)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[
                             j + 1] + 1  # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1  # than s2
            # use this line if you want to take in to account substitution matrix
            # substitutions = previous_row[j] + (c1 != c2) * substitution_Matrix [aoisPositionsDict[c1]][aoisPositionsDict[c2]]
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


def calcSimilarityForDataset(mySequence, common_scanpath, aois):
    """
    Calculates similarity between scanpaths of participants in dataset and common scanpath
    Args:
        mySequence:
        common_scanpath:

    Returns:

    """
    aoisPositionsDict = {}
    for i in range(0, len(aois)):
        aoisPositionsDict[aois[i][5]] = i

    substitution_Matrix = calcSubstitutionMatrix(aois)
    formatted_sequences = get_formatted_sequences(mySequence)

    # Store scanpaths as an array of string-converted original scanpaths
    scanpath_strs = convert_to_strs(formatted_sequences)


    result =  {
        'fixations': common_scanpath,
        'similarity': calc_similarity_to_common(scanpath_strs, common_scanpath, substitution_Matrix, aoisPositionsDict)
    }
    result['OverAllSimilarity'] = np.mean(list(result['similarity'].values()))
    result['interParticipantsSimilarities'] = calculateInterParticipantsScanpathSimilarities(scanpath_strs, substitution_Matrix, aoisPositionsDict)
    return result

def calculateInterParticipantsScanpathSimilarities(scanpathStrs, substitution_Matrix, aoisPositionsDict):
    listOfSimilarities = {}
    listOfSimilarities["all"] = []
    for actualParticipantIndex in range(0, len(scanpathStrs)):
        for i in range(0, len(scanpathStrs)):
            if i > actualParticipantIndex:
                listOfSimilarities["all"].append(calcSimilarityBetweenTwoScanpaths(scanpathStrs[actualParticipantIndex]['raw_str'],
                                                                                 scanpathStrs[i]['raw_str'],
                                                                                 substitution_Matrix,
                                                                                 aoisPositionsDict))

    listOfSimilarities["min"] =  np.min(listOfSimilarities["all"])
    listOfSimilarities["max"] =  np.max(listOfSimilarities["all"])
    listOfSimilarities["avg"] =  np.average(listOfSimilarities["all"])
    listOfSimilarities["std"] =  np.std(listOfSimilarities["all"])
    return listOfSimilarities

def calcSubstitutionMatrix(aois):
    matrix = []
    # calculateDistance(aois[0], aois[1])
    for i in range(0, len(aois)):
        row = []
        for j in range(0, len(aois)):
            row.append(calculateDistance(aois[i], aois[j]))
        matrix.append(row)
    return matrix

def calculateDistance(aoi1, aoi2):
    # TODO predelit sirkou a vyskou
    coeffSubstitutionMatrix = int(parser.get('evaluation', 'coeffSubstitutionMatrix'))
    x_aoi1_mid = int((int(aoi1[1]) + int(aoi1[2])) /2)
    y_aoi1_mid = int((int(aoi1[3]) + int(aoi1[4])) /2)
    x_aoi2_mid = int((int(aoi2[1]) + int(aoi2[2])) /2)
    y_aoi2_mid = int((int(aoi2[3]) + int(aoi2[4])) /2)
    return (sqrt(pow(x_aoi1_mid - x_aoi2_mid,2)) + sqrt(pow(y_aoi1_mid - y_aoi2_mid,2))) / int(coeffSubstitutionMatrix)

