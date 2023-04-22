import logging
from sqlalchemy import create_engine, Table, Column, String, Float, MetaData
import sqlalchemy as db

class DataSaveError(Exception):
    pass

def writeToSqlite(data):
    '''
    This function saves the mapped testdata to the database
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

    for singleRaw in data:
        point = singleRaw["point"]
        classification = singleRaw["classification"]
        yDelta = singleRaw["delta_y"]

        if classification is not None:
            classificationName = classification.name.replace("y", "N")
        else:
            # If there is no classification, there is also no distance. In that case I write a dash
            classificationName = "-"
            yDelta = -1

        try:
            insert_mapped_test_data(dbEngine, mappingTableSchema, point["x"], point["y"], yDelta, classificationName)
        except DataSaveError as e:
            logging.error(str(e))

def insert_mapped_test_data(dbEngine, mappingTableSchema, x_test, y_test, delta_y, ideal_n_y):
    '''
    This function inserts mapped testdata to the database

    Parameters:
    dbEngine: sqlalchemy.engine.Engine
    mappingTableSchema: sqlalchemy.schema.Table
    x_test: decimal
    y_test: decimal
    delta_y: decimal
    ideal_n_y: decimal
    '''

    try:
        with dbEngine.connect() as con:
            con.execute(mappingTableSchema.insert().values({"X (test function)": x_test, "Y (test function)": y_test, "Delta Y (test function)": delta_y,"Number of ideal function": ideal_n_y}))
            con.commit()
    except Exception as e:
        raise DataSaveError(f"Error saving data: {str(e)}")
