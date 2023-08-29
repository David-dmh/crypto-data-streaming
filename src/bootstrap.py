import glob
import db_connection
import endpoint
from pyflink.table.types import DataType
from pyflink.table import TableSink


def bootstrap():
    """
    Setup database with clean, consistent state. 
    Create tables, clear existing data, restore data from backup csvs.
    Args: None
    Returns: None
    """
    print("Bootstrap start...") 
    db = db_connection.DBConnection()
    print("Established connection to db...")

    db.create_tables()
    print("Created database tables")

    # clear existing data (refresh)
    db.clear_data()

    # iterate through backup csv folder and add backup csvs to db
    for csv_file in glob.glob("/usr/backups/*.csv"):
        db.insert_backup_data(csv_file)

    print("Bootstrap end...") 

def flink():
    """
    ?
    Args: None
    Returns: None
    """
    print("Flink start...") 

    t_sql_source = """
    CREATE TABLE flink_fact_prices (
        timestamp DOUBLE
        ,price_in_usd DOUBLE
        ,checksum TEXT
    )
    """

    # pg_flink_fact_prices = table_environment.execute_sql(t_sql_source)

    # my_sink = TableSink(
    #     field_names=["timestamp", "price_in_usd", "checksum"], 
    #     field_types=[DataType.String(), DataType.Float(), DataType.String()], 
    #     path, 
    #     field_delimiter=',', 
    #     num_files=-1,
    #     write_mode=None
    # )

    print("Flink end...") 

# set up db and endpoint
if __name__ == "__main__":  
    bootstrap()
    flink()
    endpoint.run()
