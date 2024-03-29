import json
import os
import uuid
import io
import time
import random

import psycopg2
from psycopg2 import sql
import sqlalchemy
from sqlalchemy import create_engine
import pandas as pd


class Database:
    """
    Defines PostgreSQL database schema.
    
    Attributes (preceding _ to indicate used by class internals)):
        _columns: dictionary - map table names to column names
        _schemas: dictionary - map table names to schema
        
    """
    _columns = {
        "fact_prices": [
            "timestamp", "price_in_usd", "checksum"
        ],
        "dim_coins": [
            "id", "abbr", "name", "checksum"
        ]
    }

    _schemas = {
        "fact_prices":
        """
        (
            timestamp FLOAT8, 
            price_in_usd FLOAT8,
            checksum TEXT
        )
        """,
        "dim_coins":
        """
        (
            id TEXT PRIMARY KEY, 
            abbr TEXT, 
            name TEXT, 
            checksum TEXT
        )
        """
    }

    @classmethod
    def get_columns(cls):
        """ 
        Getter method for columns
        """
        return cls._columns

    @classmethod
    def get_schemas(cls):
        """ 
        Getter method for schemas
        """
        return cls._schemas


class DBConnection:
    """
    Initiates connection with PostgreSQL database.
    Provides clean interface to perform database operations.
    
    Attributes:
        _engine: API object used to interact with db.
        _conn: handles connection (encapsulates DB session)
        _cur:  cursor object to execute PostgreSQl commands
    """

    def __init__(
            self,
            db_user=os.environ["POSTGRES_USER"],
            db_password=os.environ["POSTGRES_PASSWORD"],
            host_addr="database:5432",
            max_num_tries=20
        ):
        """
        Initiates connection with PostgreSQL database 
        as the given user on the given port.
        Try connect to db, on fail retry 
        with increasing waits in between.

        Args:
            - db_user: the name of the user connecting to the database.
            - db_password: the password of said user.
            - host_addr: (of the form <host>:<port>) the address where the
            database is hosted. For Postgres docker container, default port 
            is 5432 and host is "database". Docker resolves "database" to 
            the internal subnet URL of the database container.
            - max_num_tries: maximum number of tries __init__ method 
            should try to connect to the database for.
        Returns: None (since __init__)
        Raises:
            - IOError: An error occurred accessing the database. 
            Raised if after the max number of tries the connection still
            hasn't been established.
        """
        db_name = os.environ["POSTGRES_DB"]

        engine_params = (
            f"postgresql+psycopg2://{db_user}:{db_password}@"
            f"{host_addr}/{db_name}"
        )
        num_tries = 1

        while True:
            try:
                self._engine = create_engine(engine_params)
                self._conn = self._engine.raw_connection()
                self._cur = self._conn.cursor()
                break
            except (sqlalchemy.exc.OperationalError,
                    psycopg2.OperationalError):
                # Use binary exponential backoff
                #- i.e. sample a wait between [0..2^n]
                #when n = number of tries.
                time.sleep(random.randint(0, 2**num_tries))
                if num_tries > max_num_tries:
                    raise IOError("Database unavailable...")
                num_tries += 1

    def create_tables(self):
        """
        Creates database tables based on schema definition in Database 
        class.

        Args: None
           
        Returns: None (since commits execution result to database)
        """
        for table, schema in Database.get_schemas().items():
            self._cur.execute(
                sql.SQL("CREATE TABLE IF NOT EXISTS {} {}").format(
                    sql.Identifier(table), sql.SQL(schema)))
        self._conn.commit()

    def insert_backup_data(self, csv_file):
        """
        Inserts database backup CSV data. 
        If a unique uid for each measurement is not present, it generates one 
        and stores it in the CSV file.
        The rows in the CSV are then inserted as records in respective 
        tables.

        Args: 
            - csv_file: path of the CSV file
           
        Returns: None (since commits data to database)
        """
        data = pd.read_csv(csv_file)
        if "uuid" not in data.columns:
            data["uuid"] = [uuid.uuid4().hex for _ in range(data.shape[0])]
            data.to_csv(csv_file)

    # csv for each table converted to a string and copied across to database.
    # alternative could be to do Batch Insert
        for table in Database.get_columns():
            table_df = data[Database.get_columns()[table]]
            output = io.StringIO()
            table_df.to_csv(output, sep="\t", header=False, index=False)
            output.seek(0)
            self._cur.copy_from(output, table, null="")
        self._conn.commit()

    def insert_fact_prices_data(self, data):
        """
        Inserts prices data into database.

        Args: 
            - data: list of data values from the hardware (logically grouped 
            into groups of 4 values, each group is a measurement of 
            (timestamp, price_in_usd, checksum)
           
        Returns: None (since commits data to database)

        Raises:
            IOError: if data malformed (i.e. not a multiple of 4, so missing 
            values)
        """
        if len(data) % 4 != 0:
            raise IOError("Malformed packet data")

        for i in range(0, len(data), 4):
            self._cur.execute(
                """
                INSERT INTO fact_prices 
                (
                    timestamp, 
                    price_in_usd, 
                    checksum
                ) 
                VALUES 
                (
                    %s, 
                    %s, 
                    %s
                )
                ;
                 """,
                (
                    uuid.uuid4().hex, 
                    *list(data)[i: i + 4]
                )
            )
        
        self._conn.commit()

    def query_fact_prices_data(self):
        """
        Returns prices data from database for analytics.

        Args: None
           
        Returns: list of (lists of 3 values) - corresponds to records of 
        (timestamp, price_in_usd, checksum)'
        """
        self._cur.execute(
            """
            SELECT 
            timestamp, 
            price_in_usd, 
            checksum 
            FROM 
            fact_prices
            ;
            """
        )

        return json.dumps(self._cur.fetchall())

    def get_connection_stats(self):
        """
       Returns statistics for database connection (debugging). 

        Args: None
           
        Returns: JSON string consisting of connection statistics 
        e.g. 
        {4
            "user": "tester", 4
            "dbname": "testdatabase",
            "host": "database", 
            "port": "5432", 
            "tty": "", 
            "options": "", 
            "sslmode": "prefer", 
            "sslcompression": "0", 
            "krbsrvname": "postgres",
            "target_session_attrs": "any"
        }
        """

        return json.dumps(self._conn.get_dsn_parameters())

    def get_database_info(self):
        """
        Returns data stored in database, indexed by table.

        Args: None
           
        Returns: JSON string where keys are table names and values are lists 
        of lists, corresponds to list of records in that table.
        """
        tables = {}
        # returns iterable collection of public tables in the database
        self._cur.execute(
            """
            SELECT table_name 
            FROM information_schema.tables
            WHERE table_schema = 'public'
            """
        )  
        
        for table in self._cur.fetchall():
            cur2 = self._conn.cursor()
            # note sql module used for safe dynamic SQL queries
            cur2.execute(
                sql.SQL(
                    """
                    SELECT * FROM {} ;
                    """
                ).format(sql.Identifier(table[0]))
            )  
            
            tables[table[0]] = cur2.fetchall()

        return json.dumps(tables)

    def clear_data(self):
        """
        Clears data stored in database, useful for bootstrap and unit tests 
        that want to start with a fresh state.

        Args: None
           
        Returns: None
        """

        # returns an iterable collection of public tables in database
        self._cur.execute(
            """
            SELECT 
            table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            """
        )  

        for table in self._cur.fetchall():
            cur2 = self._conn.cursor()
            # note sql module used for safe dynamic SQL queries
            cur2.execute(
                sql.SQL(
                    """
                    DELETE 
                    FROM {} ;
                    """
                ).format(sql.Identifier(table[0]))
            )  
        self._conn.commit()
