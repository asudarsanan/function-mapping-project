from function_model_worker import CoreFunction
from mapping_best_functions import writeToSqlite
from calculations_worker import minimiseLoss, findClassification, errorSquared
from visualisation_worker import plotIdealFunctions, createPlottingPointBasedOnIdealFunction
import math
import pandas as pd


"""
This script provides the following functionalities:
1. Convert csv data to SQLite
2. Find ideal function based on data
3. Visualize logical graphs
"""


if __name__ == '__main__':
    # Input data declaration
    ideal_csv_path = "input-data/ideal.csv"
    train_csv_path = "input-data/train.csv"
    test_csv_path = "input-data/test.csv"

    # Read csv files and convert them to dataset using CoreFunction class
    ideal_csv_dataset = CoreFunction(csv_path=ideal_csv_path)
    train_csv_dataset = CoreFunction(csv_path=train_csv_path)
    test_csv_dataset = CoreFunction(csv_path=test_csv_path)

    # Convert the csv files to SQLite using pandas
    ideal_csv_dataset.to_sql(file_name="ideal", suffix=" (ideal function)")
    train_csv_dataset.to_sql(file_name="training", suffix=" (training function)")

    # Compute the ideal functions for the provided data and store them in a list
    ideal_functions = []
    for train_function in train_csv_dataset:
        # Find the best fitting function
        ideal_function = minimiseLoss(trainFunction=train_function,
                                      listOfCandidateFunctions=ideal_csv_dataset.functions,
                                      lossFunction=errorSquared)
        # Set the tolerance factor to the square root of 2
        ideal_function.toleranceFactor = math.sqrt(2)
        # Add the ideal function to the list of ideal functions
        ideal_functions.append(ideal_function)

    # Plot the ideal functions on the graph and save to an HTML file
    plotIdealFunctions(ideal_functions, "ideal-functions-vs-training-data")

    # Fetch the test CSV datasets and plot
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
    createPlottingPointBasedOnIdealFunction(test_dataset_ideal_function_points, "test-functions-vs-ideal-functions")

    # Write the mapping to SQLite to export as a .db file
    writeToSqlite(test_dataset_ideal_function_points)
