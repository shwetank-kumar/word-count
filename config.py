class DevelopmentConfig():
    HOST = '0.0.0.0'
    PORT = 5000
    DEBUG = True
    broker_url = 'redis://localhost:6379/0'
    result_backend = 'redis://localhost:6379/0'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost/wordcount_dev'

    @staticmethod
    def init_app(app):
        pass

class DockerConfig(DevelopmentConfig):
    broker_url = 'redis://wordcount_redis_1:6379/0'
    result_backend = 'redis://wordcount_redis_1:6379/0'
    val = 'see'

config = {
    'development': DevelopmentConfig,
    'docker': DockerConfig
}
