import psycopg2
from configparser import ConfigParser

def connect(config):
    """ Connect to the PostgreSQL database server """
    try:
        # connecting to the PostgreSQL server
        with psycopg2.connect(**config) as conn:
            print('Connected to the PostgreSQL server.')
            return conn
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


def load_config(filename, section):
    parser = ConfigParser()
    parser.read(filename)

    # get section, default to postgresql
    config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            config[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
        
    return config

#connects to postgresql and creates amazondb database
init_config = load_config("database.ini", "postgresql")
conn = connect(init_config)
conn.autocommit = True
cursor = conn.cursor()
cursor.execute(f"CREATE DATABASE amazondb")
conn.close()

#connects to postgresql and to amazondb database to create tables, values, etc
amazondb_config = load_config("amazondb.ini", "amazondb")
conn = connect(amazondb_config)
conn.autocommit = True
cursor = conn.cursor()

cursor.execute(f"CREATE TABLE funcionario(nome VARCHAR(20), idade INT, salario DECIMAL(10,2))")

cursor.execute("INSERT INTO funcionario VALUES ('Paula', 26, 2348.94)")
cursor.execute("INSERT INTO funcionario VALUES ('Jose', 22, 1231.39)")
cursor.execute("INSERT INTO funcionario VALUES ('Rodrigo', 19, 1943.29)")
cursor.execute("INSERT INTO funcionario VALUES ('Amanda', 26, 3119.22)")
cursor.execute("INSERT INTO funcionario VALUES ('Joao', 43, 9983.64)")
cursor.execute("INSERT INTO funcionario VALUES ('Carolina', 31, 7855.33)")

cursor.execute(f"SELECT * FROM funcionario")

rows = cursor.fetchall()
print(rows)

conn.close()
