import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv("../.env")


class DB:

    def __init__(self):
        try:
            self.connection = mysql.connector.connect(
                host="e150497-mysql.services.easyname.eu",
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                database=os.getenv("DB_NAME"),
            )
            self.cursor = self.connection.cursor()
        except mysql.connector.Error as err:
            raise Exception(
                "An error occurred while trying to connect to the database: {}".format(
                    err
                )
            )
