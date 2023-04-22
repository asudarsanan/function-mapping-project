import pandas as pd
from sqlalchemy import create_engine


class CoreFunction:
    """
    A class to handle core functions.
    """

    def __init__(self, csv_path):
        """
        Constructs a CoreFunction object.

        Parameters:
            csv_path (str): The path to the input CSV file.
        """
        self.data_frames = []

        try:
            self.csv_data = pd.read_csv(csv_path)
        except FileNotFoundError:
            print(f"There is an issue while reading file {csv_path}")
            raise

        x_values = self.csv_data["x"]

        for name_of_column, data_of_column in self.csv_data.items():
            if "x" in name_of_column:
                continue
            subset = pd.concat([x_values, data_of_column], axis=1)
            function = Function.from_dataframe(name_of_column, subset)
            self.data_frames.append(function)

    def to_sql(self, file_name, suffix):
        """
        Converts the CSV data to SQL and saves it to disk.

        Parameters:
            file_name (str): The name of the output database file.
            suffix (str): The suffix to add to the column names in the database.
        """
        db_engine = create_engine('sqlite:///output-data/solution.db', echo=False)

        csv_data_copied = self.csv_data.copy()
        csv_data_copied.columns = [name.capitalize() + suffix for name in csv_data_copied.columns]
        csv_data_copied.set_index(csv_data_copied.columns[0], inplace=True)

        csv_data_copied.to_sql(
            file_name,
            db_engine,
            if_exists="replace",
            index=True,
        )

    @property
    def functions(self):
        """
        Returns the data frames.
        """
        return self.data_frames

    def __iter__(self):
        """
        Makes the object iterable.
        """
        return CoreFunctionIterator(self)

    def __repr__(self):
        """
        Returns a string representation of the object.
        """
        return f"Contains {len(self.functions)} number of functions"


class CoreFunctionIterator():
    """
    An iterator that iterates through the functions in a CoreFunctionObject.

    Attributes:
    -----------
    index : int
        The index of the current function in the iteration.
    coreFunctionObject : CoreFunctionObject
        The CoreFunctionObject containing the functions to iterate over.

    Methods:
    --------
    __next__() -> function:
        Returns the next function in the iteration.
    """

    def __init__(self, coreFunctionObj):
        """
        Initializes the iteration by setting the index to 0 and saving a reference to the
        CoreFunctionObject to iterate over.

        Parameters:
        -----------
        coreFunctionObj : CoreFunctionObject
            The CoreFunctionObject containing the functions to iterate over.
        """
        self.index = 0
        self.coreFunctionObject = coreFunctionObj

    def __next__(self):
        """
        Returns the next function in the iteration, and increments the index.

        Raises:
        -------
        StopIteration
            If there are no more functions in the iteration.

        Returns:
        --------
        function
            The next function in the iteration.
        """
        if self.index < len(self.coreFunctionObject.functions):
            valueRequested = self.coreFunctionObject.functions[self.index]
            self.index = self.index + 1
            return valueRequested
        raise StopIteration



class Function:

    """
        A class representing a mathematical function.

        Attributes:
        ----------
        _name : str
            The name of the function.
        dataframe : pandas.DataFrame
            A dataframe containing the function's X and Y values.

        Methods:
        -------
        locateYBasedOnX(x):
            Returns the Y value based on the given X value.
        name():
            Returns the name of the function.
        from_dataframe(name, dataframe):
            Creates a new Function object from a pandas DataFrame.
        __iter__():
            Returns an iterator that iterates over the function's Y values.
        __sub__(second):
            Subtracts the Y values of two functions and returns the result.
        __repr__():
            Returns a string representation of the Function object.
    """
    
    def __init__(self, name):
        """
        Initialize Function object with given name.
        :param name: Name of the function
        """
        self._name = name
        self.dataframe = pd.DataFrame()

    def locateYBasedOnX(self, x):
        """
        Returns the Y value based on X value from the data frame. If the value is not found, it raises an IndexError.
        :param x: X value
        :return: Y value
        """
        searchKey = self.dataframe["x"] == x
        try:
            return self.dataframe.loc[searchKey].iat[0, 1]
        except IndexError:
            raise IndexError("Y value not found for given X value.")

    @property
    def name(self):
        """
        Returns the name of the function.
        """
        return self._name

    def __iter__(self):
        """
        Returns FunctionIterator object for iteration.
        """
        return FunctionIterator(self)

    def __sub__(self, second):
        """
        Subtracts two data frames and returns the resulting data frame.
        :param second: Function object to subtract
        :return: Data frame resulting from subtraction
        """
        return self.dataframe - second.dataframe

    @classmethod
    def from_dataframe(cls, name, dataframe):
        """
        Returns a Function object from given data frame.
        :param name: Name of the function
        :param dataframe: Data frame
        :return: Function object
        """
        dataFunction = cls(name)
        dataFunction.dataframe = dataframe
        dataFunction.dataframe.columns = ["x", "y"]
        return dataFunction

    def __repr__(self):
        """
        Returns a string representation of the Function object.
        """
        return "This is Function for {}".format(self.name)


class IdealFunction(Function):
    """
    This class calculates the ideal function based on the passed function data
    and training function with a given error tolerance.

    Attributes:
        training_function (Function): The training function used to calculate the ideal function.
        error (float): The error tolerance for the ideal function.
        toleranceValue (float): The tolerance factor for the largest deviation of the ideal function.
        _tolerance (float): The current tolerance value for the ideal function.

    Methods:
        determineLargestDeviation: Calculates the largest deviation between the training function
        and the ideal function.
        tolerance: Property that returns the current tolerance value.
        tolerance.setter: Setter for the tolerance value.
        toleranceFactor: Property that returns the current tolerance factor.
        toleranceFactor.setter: Setter for the tolerance factor.
        largestDeviation: Property that returns the largest deviation between the training function
        and the ideal function.

    """

    def __init__(self, functionData, trainingFunction, error):
        """
        Initializes the IdealFunction instance.

        Args:
            functionData (Function): The function data used to create the ideal function.
            trainingFunction (Function): The training function used to calculate the ideal function.
            error (float): The error tolerance for the ideal function.
        """
        super().__init__(functionData.name)
        self.dataframe = functionData.dataframe
        self.training_function = trainingFunction
        self.error = error
        self.toleranceValue = 1
        self._tolerance = 1

    def determineLargestDeviation(self, idealFunction, trainFunction):
        """
        Calculates the largest deviation between the training function and the ideal function.

        Args:
            idealFunction (Function): The ideal function.
            trainFunction (Function): The training function.

        Returns:
            The largest deviation between the training function and the ideal function.
        """
        distance = trainFunction - idealFunction
        distance["y"] = distance["y"].abs()
        return max(distance["y"])

    @property
    def tolerance(self):
        """
        Returns the current tolerance value for the ideal function.

        Returns:
            The current tolerance value.
        """
        self._tolerance = self.toleranceFactor * self.largestDeviation
        return self._tolerance

    @tolerance.setter
    def tolerance(self, value):
        """
        Sets the tolerance value for the ideal function.

        Args:
            value (float): The new tolerance value.
        """
        self._tolerance = value

    @property
    def toleranceFactor(self):
        """
        Returns the current tolerance factor for the ideal function.

        Returns:
            The current tolerance factor.
        """
        return self.toleranceValue

    @toleranceFactor.setter
    def toleranceFactor(self, value):
        """
        Sets the tolerance factor for the ideal function.

        Args:
            value (float): The new tolerance factor.
        """
        self.toleranceValue = value

    @property
    def largestDeviation(self):
        """
        Calculates the largest deviation between the training function and the ideal function.

        Returns:
            The largest deviation between the training function and the ideal function.
        """
        return self.determineLargestDeviation(self, self.training_function)



class FunctionIterator:
    """
    Iterator class that returns a dictionary describing a point on a function.

    Args:
        function (Function): The function to iterate over.

    Yields:
        dict: A dictionary containing the x and y values of the point.

    Raises:
        StopIteration: When there are no more points to iterate over.
    """

    def __init__(self, function):
        """
        Initializes an instance of FunctionIterator.

        Args:
            function (Function): The function to iterate over.
        """
        self._function = function
        self._index = 0

    def __next__(self):
        """
        Returns the next point on the function.

        Yields:
            dict: A dictionary containing the x and y values of the point.

        Raises:
            StopIteration: When there are no more points to iterate over.
        """
        if self._index < len(self._function.dataframe):
            value_requested_series = (self._function.dataframe.iloc[self._index])
            point = {"x": value_requested_series.x, "y": value_requested_series.y}
            self._index += 1
            return point
        raise StopIteration
    