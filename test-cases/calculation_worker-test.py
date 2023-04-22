import unittest
from unittest.mock import MagicMock
from function_model_worker import IdealFunction, CoreFunction
from calculations_worker import * 
from main import minimiseLoss, errorSquared
import pandas as pd

class UnitTest(unittest.TestCase):
    def setUp(self):
        # Setting up dummy data
        firstDataSet = {"x":[5.0,7.0,9.0],"y":[10.0,11.0,12.0]}
        secondDataSet = {"x":[1.0,2.0,3.0], "y":[7.0,8.0,9.0]}

        self.firstDataFrame = pd.DataFrame(data=firstDataSet)
        self.secondDataframe = pd.DataFrame(data=secondDataSet)

        self.firstFunction = CoreFunction('')
        self.firstFunction.dataframe = self.firstDataFrame
        self.secondFunction = CoreFunction('')
        self.secondFunction.dataframe = self.secondDataframe


    def tearDown(self):
        pass

    def testErrorSquared(self):
        # check to see first function correct value
        self.assertEqual(errorSquared(self.firstFunction, self.secondFunction), 15.0)
        # check to test the loss function value
        self.assertEqual(errorSquared(self.secondFunction, self.firstFunction), 14.0)
        # test to check that regression is zero or not
        self.assertEqual(errorSquared(self.firstFunction, self.firstFunction), 0.0)
