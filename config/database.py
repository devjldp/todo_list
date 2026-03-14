# import psycopg package
import psycopg

# Import the class Config that containst the credentials to connect with the database.
from config.settings import Config

class Database:
    """
    Use singleton pattern to manage the PostgreSQL connection.

    Attributes:
        _instance: singleton instance of the class
    """

    _instance = None
    
    #constructor
    def __init__(self):
        try:
            self._instance = psycopg.connect(
                user = Config.DB_USER,
                password = Config.DB_PASSWORD,
                host = Config.DB_HOST,
                port = Config.DB_PORT,
                dbname = Config.DB_NAME
            )

            # Display message -> debug purpose
            print("Database connection stablished")
        except psycopg.OperationalError as e:
            print(f"Error: {e}")

    # apply singleton design patter

    @classmethod
    def _get_instance(cls):
        """
        Priavte method that manages the singleton instance -> internally

        Return:
            Database coneection: singleton instance
        """
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def _close_connection(self):
        if self._instance:
            self._instance.close()
            print("Connection closed")


# To imporve the security we are going to create two more methods:

def get_db():
    return Database._get_instance()._instance

def close_db():
    if Database._instance:
        Database._instance._close_connection()
        Database._instance = None # Reset the instance