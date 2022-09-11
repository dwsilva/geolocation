import psycopg2


class Database:
    def __init__(self, user: str, password: str, host: str) -> None:
        self.user_db = user
        self.password_db = password
        self.host_db = host

    @property
    def _connection_database(self):
        connection = psycopg2.connect(
            host=self.host_db,
            database='geolocation',
            user=self.user_db,
            password=self.password_db,
            port='5432'
        )
        return connection

    @property
    def _sql_select_all(self):
        return '''
                SELECT device.device_id, location.latitude, location.longitude FROM device
                JOIN location ON device.id = location.id;
            '''

    @property
    def _sql_increment(self):
        return '''SELECT NEXTVAL('code_sequence');'''

    def _sql_insert(self, increment, device_id, lat, long):
        return f'''
        INSERT INTO device ("id", "device_id") VALUES({increment}, {device_id});
        INSERT INTO location ("id", "latitude", "longitude") VALUES({increment}, {lat}, {long});
        '''

    def _sql_select_id(self, device_id):
        return f'''
        SELECT device.device_id, location.latitude, location.longitude FROM device
        JOIN location ON device.id = location.id
        WHERE device.device_id = {device_id};
        '''

    def _execute_sql(self, sql):
        connection = self._connection_database
        try:
            cursor = connection.cursor()
            query = cursor.execute(sql)
            connection.commit()
            return query
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if connection is not None:
                connection.close()

    def increment_number(self):
        connection = self._connection_database
        try:
            cursor = connection.cursor()
            cursor.execute(self._sql_increment)
            increment = cursor.fetchall()
            return increment
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            connection.close()
        finally:
            if connection is not None:
                connection.close()

    def insert_db(self, id, lat, long):
        connection = self._connection_database
        cursor = connection.cursor()
        increment = self.increment_number()[0]
        sql = self._sql_insert(increment[0], id, lat, long)
        try:
            cursor.execute(sql)
            connection.commit()
            return connection.status
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error: %s" % error)
            connection.rollback()
            cursor.close()
            return error
        finally:
            if connection is not None:
                connection.close()

    def select_all_devices(self):
        connection = self._connection_database
        cursor = connection.cursor()
        cursor.execute(self._sql_select_all)

        recset = cursor.fetchall()
        registros = []
        for rec in recset:
            dic = {'id': rec[0], 'lat': rec[1], 'long': rec[2]}
            registros.append(dic)
        connection.close()

        return registros

    def select_id_device(self, id_device):
        connection = self._connection_database
        cursor = connection.cursor()
        cursor.execute(self._sql_select_id(id_device))

        recset = cursor.fetchall()
        registros = []
        for rec in recset:
            dic = {'id': rec[0], 'lat': rec[1], 'long': rec[2]}
            registros.append(dic)
        connection.close()

        return registros
