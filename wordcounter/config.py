class DevelopmentConfig():
    HOST = '0.0.0.0'
    PORT = 5000
    DEBUG = True
    broker_url = 'redis://redis-server:6379/0'
    result_backend = 'redis://redis-server:6379/0'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@db:5432/wordcount_dev'
    # User for migrations
    # SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost:5432/wordcount_dev'

    # TODO fix url for migrations and persistence of docker postgres

    # broker_url = 'redis://localhost:6379/0'
    # result_backend = 'redis://localhost:6379/0'
    # SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@10.200.10.1:5432/wordcount_dev'

    @staticmethod
    def init_app(app):
        pass

config = {
    'development': DevelopmentConfig
}
