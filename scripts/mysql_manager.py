import mysql.connector
from mysql.connector import errorcode

class MySQLManager:
    def __init__(self, root_user: str, root_password: str, host: str = "localhost", port: int = 3306):
        self.config = {
            "user": root_user,
            "password": root_password,
            "host": host,
            "port": port
        }
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(**self.config)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("❌ Wrong username or password.")
            else:
                print(f"❌ Error: {err}")
            self.connection = None

    def execute_query(self, query: str):
        if not self.connection:
            self.connect()
        if not self.connection:
            return

        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            self.connection.commit()
            print(f"✅ Executed: {query}")
        except mysql.connector.Error as err:
            print(f"❌ MySQL error: {err}")
        finally:
            cursor.close()

    def create_database(self, db_name, user, host_ip, password):
        self.execute_query(f"CREATE DATABASE IF NOT EXISTS `{db_name}`")
        self.execute_query(f"CREATE USER IF NOT EXISTS '{user}'@'{host_ip}' IDENTIFIED BY '{password}'")
        self.execute_query(
            f"GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, ALTER, DROP, REFERENCES "
            f"ON `{db_name}`.* TO '{user}'@'{host_ip}'"
        )

    def delete_database(self, db_name, user, host_ip):
        self.execute_query(f"DROP DATABASE IF EXISTS `{db_name}`")
        self.execute_query(f"DROP USER IF EXISTS '{user}'@'{host_ip}'")
        self.execute_query("FLUSH PRIVILEGES")
