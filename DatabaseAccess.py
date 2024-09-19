import psycopg2
from configparser import ConfigParser

class DatabaseController:
    @classmethod
    def getConnection(cls, config):
        # Connect to the PostgreSQL database server
        try:
            with psycopg2.connect(**config) as conn:
                print('Connected to the PostgreSQL server.')
                return conn
        except (psycopg2.DatabaseError, Exception) as error:
            print(error)
    
    @classmethod
    def getConfiguration(cls, filename, section):
        parser = ConfigParser()
        parser.read(filename)
        config = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                config[param[0]] = param[1]
        else:
            raise Exception('Section {0} not found in the {1} file'.format(section, filename))
        return config
    
    @classmethod
    def createDatabase(cls):
        init_config = DatabaseController.getConfiguration("database.ini", "postgresql")
        conn = DatabaseController.getConnection(init_config)
        conn.autocommit = True
        cursor = conn.cursor()
        try:
            cursor.execute(f"CREATE DATABASE amazondb")
            print("Database was created!")
        except Exception as error:
            print("amazondb already exists!")
        cursor.close()
        conn.close()
    
    @classmethod
    def createTables(cls, sqlTablesFileName):
        with open(sqlTablesFileName, "r") as f:
            sqlTables = f.readlines()
            sqlTables = ''.join(sqlTables)
        try:
            DatabaseController.executeQuery(sqlTables)
            print("Tables succesfully created!")
        except Exception as error:
            print("Tables already exist!")
        f.close()
    
    @classmethod
    def getRows(cls, query):
        amazondb_config = DatabaseController.getConfiguration("amazondb.ini", "amazondb")
        conn = DatabaseController.getConnection(amazondb_config)
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows
    
    @classmethod
    def executeQuery(cls, query):
        amazondb_config = DatabaseController.getConfiguration("amazondb.ini", "amazondb")
        conn = DatabaseController.getConnection(amazondb_config)
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(query)
        cursor.close()
        conn.close()