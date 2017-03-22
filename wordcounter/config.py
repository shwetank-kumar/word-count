class DevelopmentConfig():
    HOST = '0.0.0.0'
    PORT = 5000
    DEBUG = True
    broker_url = 'redis://redis-server:6379/0'
    result_backend = 'redis://redis-server:6379/0'
    # SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost/wordcount_dev'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@192.168.1.34/wordcount_dev'


    @staticmethod
    def init_app(app):
        pass

config = {
    'development': DevelopmentConfig
}
