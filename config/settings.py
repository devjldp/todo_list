import os
from dotenv import load_dotenv, find_dotenv

# Find the .env file if it is in the same directory or level up directories
load_dotenv(find_dotenv())

class Config:
    # Create variables in the class that will hold the values got form the .env file
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    SECRET_KEY = os.getenv("SECRET_KEY")

    