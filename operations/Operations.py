from math import *

AOIS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

def calculateDistance(xStart, yStart, xEnd, yEnd):
    """
    Calculate distance of 2D coordinates.
    """
    return sqrt(pow(xEnd - xStart, 2) + pow(yEnd - yStart, 2))

def calculateVector(xStart, yStart, xEnd, yEnd):
    """
    Calculate vector between two 2D coordinates.
    """
    return [xEnd - xStart, yEnd - yStart]

def calculateAngle(vect1, vect2):
    """
    Calculates angle between 2 vector in 2D space
    Args:
        vect1: vector represented as list
        vect2: vector represented as list

    Returns:

    """
    vect1Size = calculateDistance(0, 0, vect1[0], vect1[1])
    vect2Size = calculateDistance(0, 0, vect2[0], vect2[1])
    dotProduct = (vect1[0] * vect2[0]) + (vect1[1] * vect2[1])

    try:
        return degrees(acos(dotProduct / (vect1Size * vect2Size)))
    except:
        return 0

def getAOIBasedOnRange(value, aoiRange):
    """
    Determine AOI based on range
    Args:
        value: distance between fixations
        range: range of distance for single AOI

    Returns: character representation of AOI
    """
    return AOIS[int(value / aoiRange)]