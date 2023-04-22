# **Function Mapping Project**

This project involves writing a Python program that uses training data to choose the four ideal functions which are the best fit out of the fifty provided. The program must then use the test data provided to determine for each and every x-y-pair of values whether or not they can be assigned to the four chosen ideal functions. If so, the program also needs to execute the mapping and save it together with the deviation at hand. All data must be visualized logically, and where possible, suitable unit tests should be created/compiled.

The structure of all CSV files provided will be as follows:

* X
* Y
* x1
* y1
* ...
* ...
* xn
* yn

The criterion for choosing the ideal functions for the training function is how they minimize the sum of all y-deviations squared (Least-Square). The criterion for mapping the individual test case to the four ideal functions is that the existing maximum deviation of the calculated regression does not exceed the largest deviation between the training dataset and the ideal function chosen by more than a factor sqrt(2).

In order to complete this project, you will need to have knowledge of Python programming and data analysis techniques. Additionally, you must be familiar with handling CSV files and visualizing data. This project will be a good opportunity to practice these skills and apply them to real-world problems.

## **Table of Contents**

* **__[Installation](https://github.com/asudarsanan/function-mapping-project/tree/devlop#installation)__**
* **__[Usage](https://github.com/asudarsanan/function-mapping-project/tree/devlop#usage)__**
* **__[Contributing](https://github.com/asudarsanan/function-mapping-project/tree/devlop#contributing)__**
* **__[License](https://github.com/asudarsanan/function-mapping-project/tree/devlop#license)__**

## Installation

To install this project, follow these steps:


1. Clone the repository to your local machine using the following command:

   ```python
   git clone https://github.com/<username>/<repository-name>.git
   ```

   Note: Replace `<username>` and `<repository-name>` with your GitHub username and the name of the repository.
2. Navigate to the project directory:

   ```
   cd <repository-name>
   ```

   Note: Replace `<repository-name>` with the name of the repository.
3. Install Python 3 if it is not already installed on your machine.
4. Install the required modules by running the following command:

   ```python
   pip3 install -r requirements.txt
   ```

   This will install all the modules listed in the `requirements.txt` file.

   Note: If you are using a virtual environment, activate it before running the above command.
5. You can now use the project by running the `main.py` file.
6. To test the unit test cases, run the following command:

```python
python3 -m unittest discover tests
```

This will run all the test cases in the **tests** directory and show you the results. If any test case fails, you'll see an error message explaining what went wrong. You can modify the test cases or add new ones as needed to make sure your code is working correctly.

## **Usage**

To use this program, follow these steps:


1. Install the project by following the instructions in the Installation section.
2. Open the **main.py** file in your preferred Python IDE or text editor.
3. Modify the code to specify the path to the training datasets, test dataset, and ideal functions dataset. By default, the program expects the input datasets to be located in the **input-data** directory with the following file names:
   * **train.csv**
   * **test.csv**
   * **ideal.csv**
4. Enable INFO level logs by uncommenting the following lines in the **main.py** file:

   ```python
   bashCopy code#INFO level logs can be enabled, when needed. {INFO}
   logger.setLevel(logging.INFO)
   
   ```

   This will enable the program to output INFO-level logs, which can be useful for debugging.
5. Run the **main.py** file using the following command:

   ```python
   cssCopy codepython3 main.py
   
   ```

   This will execute the program. The program will read in the input datasets, choose the four ideal functions with the least-square deviation, and map the x-y pairs in the test dataset to the chosen functions. The output will be saved in the **output-data** directory.
6. Once the program has finished running, you can find the output database in the **output-data** directory. You can also view the HTML outputs in your preferred web browser.
7. If you want to update the input datasets, simply replace the old files in the **input-data** directory with the new ones. Then, re-run the **main.py** file to analyze the new data.

   ```bash
   bashCopy codecp /path/to/new/train/dataset.csv <repository-name>/input-data/train.csv
   cp /path/to/new/test/dataset.csv <repository-name>/input-data/test.csv
   cp /path/to/new/ideal/functions.csv <repository-name>/input-data/ideal.csv
   
   ```

   Note: Replace **<repository-name>** with the name of the repository, and **/path/to/new/train/dataset.csv**, **/path/to/new/test/dataset.csv**, and **/path/to/new/ideal/functions.csv** with the paths to the new datasets.

   Note: Before updating the input datasets, make sure they have the same structure as the original datasets.

## **Contributing**

Thank you for your interest in contributing to this project! Contributions are welcome and appreciated. To contribute, please follow these steps:


1. Fork the repository.
2. Create a new branch for your changes.
3. Make your changes and commit them with descriptive commit messages.
4. Push your changes to your fork.
5. Submit a pull request to the original repository.

Before submitting a pull request, please make sure that your changes are well-tested and do not break any existing functionality. Also, make sure to follow the code style guidelines used in the project.

## **License**

This project is licensed under the MIT License. See the **__[**LICENSE**](https://github.com/asudarsanan/function-mapping-project/blob/main/LICENSE)__** file for more information.