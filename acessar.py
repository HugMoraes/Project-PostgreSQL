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

def load_config(filename='database.ini', section='postgresql'):
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

config = load_config()

print(config)

conn = connect(config)

conn.autocommit = True
cursor = conn.cursor()

cursor.execute(f"CREATE TABLE funcionario(nome VARCHAR(20), idade INT, salario DECIMAL(10,2))")

cursor.execute("INSERT INTO funcionario VALUES ('Paula', 2904.57, 26)")
cursor.execute("INSERT INTO funcionario VALUES ('Jose', 1893.88, 22)")

cursor.execute(f"SELECT * FROM funcionario")

rows = cursor.fetchall()

print(rows)