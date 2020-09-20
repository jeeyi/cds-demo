import os

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Secret key for session management. You can generate random strings here:
# https://randomkeygen.com/
SECRET_KEY = "my precious"

# Connect to the database
SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "database.db")

CDS_URL = "http://localhost:8002/api/v1"
CDS_KEY = "hjn8SPZZ.ishYcNORLMzqBlAdbdkFIxHiiZ2LD80Y"
ROOT_FOLDER_ID = "d2eba7d2-da53-45f3-b1d6-1a1a9c1e4234"
CARTA_USER_ID = 1
