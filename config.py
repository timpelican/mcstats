import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'do-you-want-to-know-a-secret'