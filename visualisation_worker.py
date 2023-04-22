from bokeh.plotting import figure, output_file, show
from bokeh.layouts import gridplot
from bokeh.models import Band, ColumnDataSource
from bokeh.palettes import Category10_5, Colorblind5

def plotIdealFunctions(idealFunctions, fileName):
    """
    Generates and displays two graphs per row based on the provided `idealFunctions`.

    Args:
        idealFunctions (list): A list of `IdealFunction` objects.
        fileName (str): The name of the output HTML file to generate.

    Returns:
        None.
    """
    idealFunctions.sort(key=lambda ideal_function: ideal_function.training_function.name, reverse=False)
    graphPlots = []
    for idealFunction in idealFunctions:
        graphData = createGraphFromTwoFunctions(lineFunction=idealFunction, scatterFunction=idealFunction.training_function,
                                                squaredError=idealFunction.error)
        graphPlots.append(graphData)
    output_file("{}.html".format(fileName), title="Training functions VS Best ideal functions")
    n = len(graphPlots)
    plots = []
    row = []
    for i in range(n):
        if i > 0 and i % 2 == 0:
            plots.append(row)
            row = []
        row.append(graphPlots[i])
    plots.append(row)
    gridLayout = gridplot(plots, toolbar_location=None, sizing_mode='stretch_width')
    show(gridLayout)



def createPlottingPointBasedOnIdealFunction(classificationPoints, fileName):
    """
    Creates plotting points based on ideal functions and saves in an HTML file.

    Parameters:
    classificationPoints (list): A list of dictionaries containing the points and their classifications.
    fileName (str): The name of the output file.

    Returns:
    None
    """
    graphPlots = []
    for index, item in enumerate(classificationPoints):
        if item["classification"] is not None:
            p = classificationGraphPlot(item["point"], item["classification"])
            graphPlots.append(p)

    # Create grid layout with four columns
    plotsPerRow = 4
    numRows = len(graphPlots) // plotsPerRow + (len(graphPlots) % plotsPerRow > 0)
    grid = []
    for i in range(numRows):
        row = []
        for j in range(plotsPerRow):
            idx = i * plotsPerRow + j
            if idx < len(graphPlots):
                row.append(graphPlots[idx])
        grid.append(row)

    # Create output file and show grid of plots with updated title
    output_file(f"{fileName}.html", title='Test points VS Ideal functions')
    show(gridplot(grid))

def createGraphFromTwoFunctions(scatterFunction, lineFunction, squaredError):
    """
    Creates a graph based on two functions.

    Parameters:
    scatterFunction (IdealFunction): An IdealFunction object representing the scatter plot data.
    lineFunction (IdealFunction): An IdealFunction object representing the ideal line data.
    squaredError (float): The calculated squared error between the two functions.

    Returns:
    A Bokeh figure object.
    """
    # First function dataframes and names
    functionOneDataframe = scatterFunction.dataframe
    functionOneName = scatterFunction.name

    # Second function dataframes and names
    functionTwoDataframe = lineFunction.dataframe
    functionTwoName = lineFunction.name

    # Get squared error rounded to two
    squaredError = round(squaredError, 2)

    # Set up figure
    graphPlot = figure(title="Graph for train model {} vs ideal {}. Calculated Squared error = {}".format(functionOneName, functionTwoName, squaredError),
                       x_axis_label='x', y_axis_label='y')

    # Set up data sources
    dataSources = {
        'train': ColumnDataSource(functionOneDataframe),
        'ideal': ColumnDataSource(functionTwoDataframe)
    }

    # Set up plot glyphs
    graphPlot.scatter('x', 'y', fill_color=Category10_5[0], legend_label='Train', size=8, source=dataSources['train'])
    graphPlot.line('x', 'y', line_width=3, legend_label='Ideal', line_color=Colorblind5[3], source=dataSources['ideal'])

    return graphPlot


def classificationGraphPlot(point, idealFunction):
    """
    Plots the classification based on points.

    Parameters:
    point (dict): A dictionary containing the x and y coordinates of the point.
    idealFunction (IdealFunction): An object representing the ideal classification function.

    Returns:
    graphPlot (figure): A Bokeh figure object with the plotted graph.
    """
    if idealFunction is not None:
        # Get data from ideal function
        functionClassificationDataframe = idealFunction.dataframe

        # Get string representation of point
        pointString = f"({point['x']}, {round(point['y'], 2)})"

        # Create figure with title and axis labels
        title = f"Point: {pointString} with Best Ideal Function: {idealFunction.name}"
        graphPlot = figure(title=title, x_axis_label="x", y_axis_label="y")

        # Plot ideal function as a line
        graphPlot.line(functionClassificationDataframe["x"], functionClassificationDataframe["y"],
                       legend_label="Best Ideal function", line_width=2, line_color=Colorblind5[0])

        # Plot ideal function tolerance as a band
        idealFunctionTolerance = idealFunction.tolerance
        functionClassificationDataframe["upper"] = functionClassificationDataframe["y"] + idealFunctionTolerance
        functionClassificationDataframe["lower"] = functionClassificationDataframe["y"] - idealFunctionTolerance
        dataSrc = ColumnDataSource(functionClassificationDataframe.reset_index())
        band = Band(base="x", lower="lower", upper="upper", source=dataSrc, level="underlay",
                    fill_alpha=0.5, line_width=4, line_color=Colorblind5[2], fill_color=Colorblind5[2])
        graphPlot.add_layout(band)

        # Plot test point as a red dot
        graphPlot.scatter([point["x"]], [round(point["y"], 4)], fill_color=Category10_5[3],
                          legend_label="Test data point", size=8)

        # Set the background color and grid lines
        graphPlot.background_fill_color = "#f9f9f9"
        graphPlot.grid.grid_line_color = "#e4e4e4"

        return graphPlot
