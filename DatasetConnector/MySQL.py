import mysql.connector
import pandas as pd
from CustomException import CustomException as CE


class MySQL(object):
    connection = None

    def __init__(self):
        pass

    def connect(self, host, username, password, db):
            try:
                MySQL.connection = mysql.connector.connect(host=host, database=db, user=username, password=password)
            except mysql.connector.Error as err:
                raise CE.DatasetConnectionFailed("Failed to establish connection with dataset connector: %s"
                                                 % "SQL", 403)

    def dataset(self, db_param):
        """ Read from SQL and Store into DataFrame """

        if not MySQL.connection:
            MySQL.connect(self, host=db_param["host"], username=db_param["username"],
                          password=db_param["password"], db=db_param["db"])
        cursor = MySQL.connection.cursor()
        cursor.execute('SELECT * FROM ' + db_param["db"] + '.' + db_param['table'] + ';')
        dataframe = pd.DataFrame(cursor.fetchall())
        dataframe.columns = cursor.column_names
        return dataframe

    def get_columns(self, db_param):
        if not MySQL.connection:
            MySQL.connect(self, host=db_param["host"], username=db_param["username"],
                          password=db_param["password"], db=db_param["db"])
        cursor = MySQL.connection.cursor()
        column_list = cursor.column_names
        return column_list

    def check_connection(self, db_param):
        try:
            if not MySQL.connection:
                MySQL.connect(self, host=db_param["host"], username=db_param["username"],
                              password=db_param["password"], db=db_param["db"])
            #  checkTableExists
            cursor = MySQL.connection.cursor()
            cursor.execute("""
                    SELECT COUNT(*)
                    FROM information_schema.tables
                    WHERE table_name = '{0}'
                    """.format(db_param['table'].replace('\'', '\'\'')))
            if cursor.fetchone()[0] == 1:
                cursor.close()
                return True
            cursor.close()
            return False
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            return False


