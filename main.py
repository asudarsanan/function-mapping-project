import logging
import math
import pandas as pd
import sys

from function_model_worker import CoreFunction
from mapping_best_functions import writeToSqlite
from calculations_worker import minimiseLoss, findClassification, errorSquared
from visualisation_worker import plotIdealFunctions, createPlottingPointBasedOnIdealFunction


"""
This script provides the following functionalities:
1. Convert csv data to SQLite
2. Find ideal function based on data
3. Visualize logical graphs
"""

class CsvConversionException(Exception):
    pass

class IdealFunctionException(Exception):
    pass

if __name__ == '__main__':
    # Configure logging
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler = logging.FileHandler('log.txt')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    # Input data declaration
    ideal_csv_path = "input-data/ideal.csv"
    train_csv_path = "input-data/train.csv"
    test_csv_path = "input-data/test.csv"

    try:
        # Read csv files and convert them to dataset using CoreFunction class
        logging.info("Converting CSV files to dataset using CoreFunction class")
        try:
            ideal_csv_dataset = CoreFunction(csv_path=ideal_csv_path)
            train_csv_dataset = CoreFunction(csv_path=train_csv_path)
            test_csv_dataset = CoreFunction(csv_path=test_csv_path)
        except Exception as e:
            raise CsvConversionException("Error occurred while converting CSV to dataset using CoreFunction class") from e

        # Convert the csv files to SQLite using pandas
        logging.info("Converting CSV files to SQLite using pandas")
        try:
            ideal_csv_dataset.to_sql(file_name="ideal", suffix=" (ideal function)")
            train_csv_dataset.to_sql(file_name="training", suffix=" (training function)")
        except Exception as e:
            raise CsvConversionException("Error occurred while converting CSV to SQLite using pandas") from e

        # Compute the ideal functions for the provided data and store them in a list
        ideal_functions = []
        for train_function in train_csv_dataset:
            # Find the best fitting function
            logging.info("Finding the best fitting function")
            try:
                ideal_function = minimiseLoss(trainFunction=train_function,
                                              listOfCandidateFunctions=ideal_csv_dataset.functions,
                                              lossFunction=errorSquared)
                # Set the tolerance factor to the square root of 2
                ideal_function.toleranceFactor = math.sqrt(2)
                # Add the ideal function to the list of ideal functions
                ideal_functions.append(ideal_function)
            except Exception as e:
                raise IdealFunctionException("Error occurred while finding the best fitting function") from e


        # Plot the ideal functions on the graph and save to an HTML file
        logging.info("Plotting the ideal functions on the graph and saving to an HTML file")
        plotIdealFunctions(ideal_functions, "ideal-functions-vs-training-data")

        # Fetch the test CSV datasets and plot
        logging.info("Fetching the test CSV datasets and plotting")
        test_dataset_points = test_csv_dataset.functions[0]

        test_dataset_ideal_function_points = []
        for point in test_dataset_points:
            # Find the best classification function and the delta y for each point in the test dataset
            ideal_function, y_delta = findClassification(point=point, idealFunctions=ideal_functions)
            
            # Create a dictionary containing the point, the classification function and the delta y
            result = {"point": point, "classification": ideal_function, "delta_y": y_delta}
            # Add the dictionary to the list of ideal function points
            test_dataset_ideal_function_points.append(result)

        # Plot the test data into the Bokeh graph
        logging.info("Plotting the test data into the Bokeh graph")
        createPlottingPointBasedOnIdealFunction(test_dataset_ideal_function_points, "test-functions-vs-ideal-functions")

        # Write the mapping to SQLite to export as a .db file
        logging.info("Writing the mapping to SQLite to export as a .db file")
        writeToSqlite(test_dataset_ideal_function_points)

    except Exception as e:
        logging.error(str(e))
        raise CustomException("Error occurred while executing the script. Check the log file for details.") from e

