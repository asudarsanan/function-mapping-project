import logging
from function_model_worker import IdealFunction


def minimiseLoss(trainFunction, listOfCandidateFunctions, lossFunction):
    """
    This function finds the function with the minimum loss based on a training function and a list of candidate functions.
    It returns an IdealFunction object with the data of the function with the smallest error.
    """
    logging.info(f"Invoking minimiseLoss with trainFunction={trainFunction}, listOfCandidateFunctions={listOfCandidateFunctions}, lossFunction={lossFunction}")
    
    functionWithSmallestError = None
    smallestError = None

    for candidateFunction in listOfCandidateFunctions:
        error = lossFunction(trainFunction, candidateFunction)

        if smallestError is None or error < smallestError:
            smallestError = error
            functionWithSmallestError = candidateFunction

    return IdealFunction(functionData=functionWithSmallestError,
                          trainingFunction=trainFunction,
                          error=smallestError)


def findClassification(point, idealFunctions):
    """
    This function finds the classification of a point with respect to a list of ideal functions.
    It returns a tuple containing the ideal function with the lowest distance and the distance itself.
    """
    logging.info(f"Invoking findClassification with point={point}, idealFunctions={idealFunctions}")
    
    lowestClassification = None
    lowestDistance = None

    for idealFunction in idealFunctions:
        try:
            yLocation = idealFunction.locateYBasedOnX(point["x"])
        except IndexError as e:
            logging.error(f"IndexError occurred while locating y for point {point}: {e}")
            raise

        # finds the absolute distance
        absoluteDistance = abs(yLocation - point["y"])

        if abs(absoluteDistance) < idealFunction.tolerance:
            # returns the lowest distance
            if lowestClassification is None or absoluteDistance < lowestDistance:
                lowestClassification = idealFunction
                lowestDistance = absoluteDistance

    return lowestClassification, lowestDistance


def errorSquared(firstFunction, secondFunction):
    """
    This function calculates the squared error based on the distance between two functions.
    It returns the sum of squared distances.
    """
    logging.info(f"Invoking errorSquared with firstFunction={firstFunction}, secondFunction={secondFunction}")
    
    distances = secondFunction - firstFunction
    distances["y"] = distances["y"] ** 2
    return sum(distances["y"])
