import os
"""
    This will be the base setting of the entire 
    application. They are the default configs
"""

class Config(object):
    """
        Parent configuration class.
    """
    DEBUG = False
    TESTING = False
    # # Database
    # DB_HOST = os.getenv('DB_HOST')
    # DB_USER = os.getenv('DB_USER')
    # DB_PASSWORD = os.getenv('DB_PASSWORD')
    
    SEED_ADMIN_EMAIL = os.getenv('SEED_ADMIN_EMAIL')
    SEED_ADMIN_PASSWORD = os.getenv('SEED_ADMIN_PASSWORD')
    SEED_ADMIN_USERNAME = os.getenv('SEED_ADMIN_USERNAME')



class DevelopmentConfig(Config):
    """
        Configurations for Development.
    """
    DEVELOPMENT = True
    DEBUG = True
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))  

    # Define the database - we are working with
    # SQLite for this example
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'EESBS.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DATABASE_CONNECT_OPTIONS = {}

    # Application threads. A common general assumption is
    # using 2 per available processor cores - to handle
    # incoming requests using one and performing background
    # operations using the other.
    THREADS_PER_PAGE = 2



class TestingConfig(Config):
    """
        Configurations for Testing
    """
    TESTING = True
    DEBUG = True
    # DB_NAME = os.getenv('TEST_DB_NAME')


class ProductionConfig(Config):
    """configuration for the production environment"""
    # DB_NAME = os.getenv('DB_NAME')
    DEBUG = True


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}