from sqlalchemy import create_engine, Table, Column, String, Float, MetaData
import sqlalchemy as db

def writeToSqlite(data):
    ###
    # Here, we are using default engine of sqline and creating tables in the sqlife for the mapping part
    ###

    for singleRaw in data:
        point = singleRaw["point"]
        classification = singleRaw["classification"]
        yDelta = singleRaw["delta_y"]

        if classification is not None:
            classificationName = classification.name.replace("y", "N")
            insert_mapped_test_data(point["x"],point["y"],yDelta,classificationName)
        else:
            # If there is no classification, there is also no distance. In that case I write a dash
            classificationName = "-"
            yDelta = -1

            insert_mapped_test_data(point["x"],point["y"],yDelta,classificationName)
            # query=mappingTableSchema.insert().values({"X (test function)": point["x"], "Y (test function)": point["y"], "Delta Y (test function)": yDelta,"Number of ideal function": classificationName})

    #     # Make sure the column name should be same as table schema, otherwise it will thorw an error
    # #     tableData.append(
    # #         {"X (test function)": point["x"], "Y (test function)": point["y"], "Delta Y (test function)": yDelta,
    # #          "Number of ideal function": classificationName})

    # # # here we are inserting data and executing the query
    # # query = mappingTableSchema.insert()
    # # query.execute(tableData)
        


    # try:
    #     with dbEngine.connect() as con:

    #         print (classificationName)
    #         con.execute(query)
    #         return True
    # except Exception as e:
    #     raise Exception(f"Error saving data: {str(e)}")

def insert_mapped_test_data(x_test, y_test, delta_y, ideal_n_y):
    
    '''

    This function saves the mapped testdata to the database

    Raises:
    A custom exception if there is an error saving the data

    Returns:
    Boolean: success or failure
    
    Parameters:
    x_test: decimal
    y_test: decimal
    delta_y: decimal
    ideal_n_y: decimal
    
    '''
    dbEngine = create_engine('sqlite:///output-data/solution.db', echo=False)
    metadata = db.MetaData()

    mappingTableSchema = Table('mappingData', metadata,
                    Column('X (test function)', Float, primary_key=False),
                    Column('Y (test function)', Float),
                    Column('Delta Y (test function)', Float),
                    Column('Number of ideal function', String(50))
                    )

    metadata.create_all(dbEngine)

    try:
        with dbEngine.connect() as con:
            con.execute(mappingTableSchema.insert().values({"X (test function)": x_test, "Y (test function)": y_test, "Delta Y (test function)": delta_y,"Number of ideal function": ideal_n_y}))
            con.commit()
            return True
    except Exception as e:
        raise Exception(f"Error saving data: {str(e)}")