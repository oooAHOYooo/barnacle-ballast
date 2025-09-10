# config.py - Flask Configuration
import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-for-development'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///barnacle_ballast.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Upload settings
    UPLOAD_FOLDER = 'static/uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mov'}
    
    # Session settings
    PERMANENT_SESSION_LIFETIME = timedelta(hours=8)
    
    # Crew authentication
    CREW_PASSWORD = os.environ.get('CREW_PASSWORD', 'STUDIO!@#')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'BARNACLE2025')

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///barnacle_ballast_dev.db'

class ProductionConfig(Config):
    DEBUG = False
    # Use PostgreSQL in production
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///barnacle_ballast_test.db'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

