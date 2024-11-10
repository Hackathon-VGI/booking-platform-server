import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://user:password@db:5432/booking_db')
    QLALCHEMY_TRACK_MODIFICATIONS = False