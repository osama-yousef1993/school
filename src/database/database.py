import pymysql

from src.utils.config import DATABASE, DB_PORT, HOST_DB, PASSWORD, USERNAME


class DataBase:
    def __init__(
        self,
        host=HOST_DB,
        username=USERNAME,
        password=PASSWORD,
        database=DATABASE,
        port=int(DB_PORT),
    ):
        try:
            # Initial connection to check databases
            self.connection = pymysql.connect(
                host=host,
                user=username,
                password=password,
                port=port,
            )
            self.my_cursor = self.connection.cursor()

            if database:
                self.my_cursor.execute("SHOW DATABASES")
                databases = [db[0] for db in self.my_cursor.fetchall()]

                if database in databases:
                    # Reconnect to the specified database
                    self.connection = pymysql.connect(
                        host=host,
                        user=username,
                        password=password,
                        db=database,
                    )
                    self.my_cursor = self.connection.cursor()
                else:
                    print(f"Database '{database}' not found.")
        except pymysql.MySQLError as e:
            print(f"Error connecting to the database: {e}")

    def create_new_database(self, name: str):
        try:
            self.my_cursor.execute(f"CREATE DATABASE `{name}`;")
            self.connection.commit()
            print(f"Database '{name}' created successfully.")
        except pymysql.MySQLError as e:
            print(f"Error creating database '{name}': {e}")

    def create_new_table(self, name: str, columns: str):
        try:
            sql = f"CREATE TABLE `{name}` ({columns});"
            self.my_cursor.execute(sql)
            self.connection.commit()
            print(f"Table '{name}' created successfully.")
        except pymysql.MySQLError as e:
            print(f"Error creating table '{name}': {e}")

    def insert_data(self, table: str, **values):
        try:
            columns = ", ".join(f"`{col}`" for col in values.keys())
            placeholders = ", ".join(["%s"] * len(values))
            sql = f"INSERT INTO `{table}` ({columns}) VALUES ({placeholders});"
            self.my_cursor.execute(sql, tuple(values.values()))
            self.connection.commit()
            print(f"Data inserted into table '{table}' successfully.")
        except pymysql.MySQLError as e:
            print(f"Error inserting data into table '{table}': {e}")

    def select_one(self, sql: str):
        try:
            self.my_cursor.execute(sql)
            return self.my_cursor.fetchone()
        except pymysql.MySQLError as e:
            print(f"Error fetching data: {e}")
            return None

    def select_all(self, sql: str):
        try:
            self.my_cursor.execute(sql)
            return self.my_cursor.fetchall()
        except pymysql.MySQLError as e:
            print(f"Error fetching data: {e}")
            return []

    def update_data(self, table: str, id_: int, **values):
        try:
            set_clause = ", ".join(f"`{col}` = %s" for col in values.keys())
            sql = f"UPDATE `{table}` SET {set_clause} WHERE `Id` = %s;"
            self.my_cursor.execute(sql, tuple(values.values()) + (id_,))
            self.connection.commit()
            print(f"Data in table '{table}' updated successfully.")
        except pymysql.MySQLError as e:
            print(f"Error updating data in table '{table}': {e}")

    def delete_data(self, table: str, column: str, value):
        try:
            sql = f"DELETE FROM `{table}` WHERE `{column}` = %s;"
            self.my_cursor.execute(sql, (value,))
            self.connection.commit()
            print(f"Data deleted from table '{table}' where `{column}` = {value}.")
        except pymysql.MySQLError as e:
            print(f"Error deleting data from table '{table}': {e}")

    def upsert_data(self, table: str, **values):
        try:
            columns = ", ".join(f"`{col}`" for col in values.keys())
            # set_clause = ", ".join(f"`{col}` = %s" for col in values.keys())
            # Generate the SET clause for updating
            set_clause = ", ".join(
                f"`{col}` = VALUES(`{col}`)" for col in values.keys()
            )

            placeholders = ", ".join(["%s"] * len(values))
            sql = f"""INSERT INTO `{table}` ({columns}) VALUES ({placeholders}) ON DUPLICATE KEY UPDATE {set_clause};"""
            self.my_cursor.execute(sql, tuple(values.values()))
            self.connection.commit()
            print(f"Data in table '{table}' updated successfully.")
        except pymysql.MySQLError as e:
            print(f"Error updating data in table '{table}': {e}")

    def close_connection(self):
        try:
            if self.connection:
                self.connection.close()
                print("Database connection closed.")
        except pymysql.MySQLError as e:
            print(f"Error closing connection: {e}")
