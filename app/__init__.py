# import settings and flask package
from flask import Flask
from config.settings import Config
from config.database import close_db

# Initialise an instance of Flask
# __name__ helps flask locate resources templates and static files
app = Flask(__name__)

# Use the secret key -> Create sessions
app.secret_key = Config.SECRET_KEY

# Load configuration setting
app.config.from_object(Config)

# close the database automatically
@app.teardown_appcontext
def teardown_db(exception):
    """Closes trhe database connection when the application ends"""
    close_db()

#We must ensure "app" is fully initialized before the controller tries to use it
from app import controller

