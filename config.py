class Config:
    SECRET_KEY='mi_clave'

class DevelopmentConfig(Config):
    DEBUG=True
    MYSQL_HOTS = 'localhost'
    MYSQL_USERNAME = 'jerem'
    MYSQL_PASSWORD = 'jeremias166'
    MYSQL_DB = 'flask_login'

config={
    'development':DevelopmentConfig
}