import psycopg2


def create_database():
    sql_create_database = '''
        -- Database: geolocation
        -- DROP DATABASE IF EXISTS geolocation;
        CREATE DATABASE geolocation
            WITH
            OWNER = root
            ENCODING = 'UTF8'
            LC_COLLATE = 'en_US.utf8'
            LC_CTYPE = 'en_US.utf8'
            CONNECTION LIMIT = -1;
    '''

    connection = psycopg2.connect(
        database="postgres",
        user='root',
        password='root',
        host='localhost',
        port='5432'
    )

    connection.autocommit = True
    cursor = connection.cursor()
    cursor.execute(sql_create_database)
    print("Database has been created successfully !!")
    connection.close()


def create_tables():
    sql_create_device = '''
        CREATE TABLE IF NOT EXISTS device(
            id SERIAL NOT NULL PRIMARY KEY,
            device_id integer NOT NULL
        );
    '''
    sql_create_location = '''
        CREATE TABLE IF NOT EXISTS location(
            id SERIAL NOT NULL PRIMARY KEY,
            latitude decimal NOT NULL,
            longitude decimal NOT NULL,
            FOREIGN KEY (id) REFERENCES device (id)
        );
    '''
    sql_create_sequence = '''
        CREATE SEQUENCE code_sequence
        INCREMENT 1
        MINVALUE 1
        MAXVALUE 99999
        START 1
        CACHE 1;
    '''
    connection = psycopg2.connect(
        database="geolocation",
        user='root',
        password='root',
        host='localhost',
        port='5432'
    )
    connection.autocommit = True
    cursor = connection.cursor()
    cursor.execute(sql_create_device)
    print("Device table has been created successfully !!")
    cursor.execute(sql_create_location)
    print("Location table has been created successfully !!")
    cursor.execute(sql_create_sequence)
    print("Sequence has been created successfully !!")

    connection.close()


if __name__ == "__main__":
    create_database()

    create_tables()
