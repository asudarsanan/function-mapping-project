import unittest
from unittest.mock import MagicMock
import pandas as pd

from calculations_worker import errorSquared
from function_model_worker import CoreFunction
from main import minimiseLoss


class UnitTest(unittest.TestCase):
    """
    Unit tests for errorSquared function.
    """
    def setUp(self):
        """
        Setting up dummy data and CoreFunction instances.
        """
        first_data_set = {"x": [5.0, 7.0, 9.0], "y": [10.0, 11.0, 12.0]}
        second_data_set = {"x": [1.0, 2.0, 3.0], "y": [7.0, 8.0, 9.0]}

        self.first_dataframe = pd.DataFrame(data=first_data_set)
        self.second_dataframe = pd.DataFrame(data=second_data_set)

        self.first_function = CoreFunction('')
        self.first_function.dataframe = self.first_dataframe
        self.second_function = CoreFunction('')
        self.second_function.dataframe = self.second_dataframe

    def tearDown(self):
        """
        Clean up after each test.
        """
        pass

    def test_error_squared(self):
        """
        Test errorSquared function with different CoreFunction instances.
        """
        # Check to see the correct value for the first function
        self.assertEqual(errorSquared(self.first_function, self.second_function), 15.0)

        # Check to test the loss function value
        self.assertEqual(errorSquared(self.second_function, self.first_function), 14.0)

        # Test to check that regression is zero or not
        self.assertEqual(errorSquared(self.first_function, self.first_function), 0.0)
