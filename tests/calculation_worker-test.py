import unittest
import pandas as pd
import logging

import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from calculations_worker import errorSquared
from function_model_worker import CoreFunction

logging.basicConfig(level=logging.DEBUG)

class MyUnitTest(unittest.TestCase):
    def setUp(self):
        """Sets up dummy data for testing."""
        # Generate dummy data
        data1 = {"x":[1.0,2.0,3.0],"y":[5.0,6.0,7.0]}
        data2 = {"x":[4.0,5.0,6.0], "y":[8.0,9.0,10.0]}

        # Create pandas dataframes from the data
        self.df1 = pd.DataFrame(data=data1)
        self.df2 = pd.DataFrame(data=data2)

        # Create instances of CoreFunction and assign the dataframes to them
        self.func1 = CoreFunction('input-data/test.csv')
        self.func1 = self.df1
        self.func2 = CoreFunction('input-data/test.csv')
        self.func2 = self.df2

    def tearDown(self):
        """Tears down any resources used for testing."""
        pass

    def testSquaredError(self):
        """Tests the errorSquared function."""
        # Test to ensure that the function returns the correct value when given two functions
        self.assertEqual(errorSquared(self.func1, self.func2), 27.0)

        # Test to ensure that the function is symmetric when given two functions
        self.assertEqual(errorSquared(self.func2, self.func1), 27.0)

        # Test to ensure that the function returns zero when given the same function twice
        self.assertEqual(errorSquared(self.func1, self.func1), 0.0)

if __name__ == '__main__':
    unittest.main()
