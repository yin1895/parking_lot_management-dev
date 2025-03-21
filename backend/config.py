import os

class Config:
    PORT = int(os.getenv('PORT', 5000))
    DEBUG = False
    TESTING = False
    DATABASE_URI = 'sqlite://:memory:'
