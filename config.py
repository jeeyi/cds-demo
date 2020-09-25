import os

JSONIFY_PRETTYPRINT_REGULAR = False
WTF_CSRF_CHECK_DEFAULT = False

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
CDS_KEY = "OkeM2gDF.vCKtaxobPWCeiWRJHcehrouTb3QQDHfw"
ROOT_FOLDER_ID = "ab383f88-8c7e-46eb-ad5d-877d46d83e0c"
CARTA_USER_ID = 1
