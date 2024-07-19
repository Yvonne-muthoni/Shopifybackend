import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_URI = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

class Config:
    SQLALCHEMY_DATABASE_URI = DB_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY", "your_default_secret_key")
    CORS_HEADERS = 'Content-Type'


