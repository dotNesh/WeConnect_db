import os
from app import app

#Debug should be false in production
app.DEBUG = True
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')