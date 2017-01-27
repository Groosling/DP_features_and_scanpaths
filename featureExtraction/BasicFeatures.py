from operations import Operations
def calculateBasicFeatures(participants):
    """
    Calculates basiv feature
    Args:
        participatns: dictionary od participants

    Returns:
    Dictionary of participants containing dictionary of no agregated basic features
    """
    result = {}
    keys = participants.keys()
    for y in range(0, len(keys)):
        result[keys[y]] = {}
        result[keys[y]]['fixationCount'] = len(participants[keys[y]])
        result[keys[y]]['fixationDuration'] = getFixationDuration(participants[keys[y]])
        result[keys[y]]['saccadeLength'] = getSaccadeLength(participants[keys[y]])
        result[keys[y]]['relSaccadeAngle'] = getRelativeSaccadeAngle(participants[keys[y]])
        result[keys[y]]['absSaccadeAngle'] = getAbsoluteSaccadeAngle(participants[keys[y]])

    return result


def getFixationDuration(participant):
    """
    Extract fixation durations from participant data
    Args:
        participant: array of single participant fixations

    Returns:
        array of fixation durations of single participant
    """
    result = []
    for z in range(0, len(participant)):
        result.append(float(participant[z][2]))
    return result


def getSaccadeLength(participant):
    """
    Extract saccade length from participant data
    Args:
        participant: array of single participant fixations

    Returns:
        array of saccade lengths of single participant
    """
    result = []
    for z in range(0, len(participant) - 1):
          result.append(Operations.calculateDistance(int(participant[z][3]), int(participant[z][4]),
                                                     int(participant[z + 1][3]), int(participant[z + 1][4])))
    return result

def getRelativeSaccadeAngle(participant):
    """
    Extract relative angle from participant saccades
    Args:
        participant: array of single participant fixations

    Returns:
        array of relative angles of single participant saccades
    """
    result = []
    for z in range(0, len(participant) - 2):
        # TODO vec2= vec1
        vec1 = Operations.calculateVector(int(participant[z][3]), int(participant[z][4]),
                               int(participant[z + 1][3]), int(participant[z + 1][4]))
        # calculates vector between next point and next next one
        vec2 = Operations.calculateVector(int(participant[z + 1][3]), int(participant[z + 1][4]),
                               int(participant[z + 2][3]), int(participant[z + 2][4]))
        result.append(Operations.calculateAngle(vec1, vec2))
    return result

def getAbsoluteSaccadeAngle(participant):
    """
    Extract absolute angle from participant saccades
    Args:
        participant: array of single participant fixations

    Returns:
        array of absolute angles of single participant saccades
    """
    result = []
    for z in range(0, len(participant) - 1):
        vec1 = Operations.calculateVector(int(participant[z][3]), int(participant[z][4]),
                               int(participant[z + 1][3]), int(participant[z + 1][4]))
        # calculates vector between next point and next next one
        vec2 = Operations.calculateVector(0, 0, 1, 0)
        result.append(Operations.calculateAngle(vec1, vec2))
    return result
