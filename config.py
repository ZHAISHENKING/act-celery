import os, datetime
from production import *
try:
    from local_settings import *
except Exception:
    pass


class Config(object):
    DEBUG = False
    TESTING = False

    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    SECRET_KEY = 'FDANFSDAO32NE1-013UR12y4ibksd13B2KJ;SC0231'
    REMEMBER_COOKIE_DURATION = datetime.timedelta(hours=3)
    BABEL_DEFAULT_LOCALE = 'zh_CN'

    # 可上传的文件类型
    ALLOWED_EXTENSIONS = dict([
        ("3gp", "video/3gpp"),
        ("gif", "image/gif"),
        ("jpeg", "image/jpeg"),
        ("jpg", "image/jpeg"),
        ("m4u", "video/vndmpegurl"),
        ("m4v", "video/x-m4v"),
        ("mov", "video/quicktime"),
        ("mp4", "video/mp4"),
        ("mpe", "video/mpeg"),
        ("mpeg", "video/mpeg"),
        ("mpg", "video/mpeg"),
        ("mpg4", "video/mp4"),
        ("png", "image/png"),
        ("flv", "flv-application/octet-stream")
    ])

    # Flask-Security config
    SECURITY_URL_PREFIX = "/docs/admin/"
    SECURITY_PASSWORD_HASH = "pbkdf2_sha512"
    SECURITY_PASSWORD_SALT = "ATGUOHAELKiubahiughaerGOJAEGj"

    # Flask-Security URLs
    SECURITY_LOGIN_URL = "/docs/login/"
    SECURITY_LOGOUT_URL = "/docs/logout/"
    SECURITY_REGISTER_URL = "/docs/reg/"

    SECURITY_POST_LOGIN_VIEW = "/docs/admin/"
    SECURITY_POST_LOGOUT_VIEW = "/docs/admin/"
    SECURITY_POST_REGISTER_VIEW = "/docs/admin/"

    # Flask-Security features
    SECURITY_REGISTERABLE = True
    SECURITY_SEND_REGISTER_EMAIL = False

    CELERY_ACCEPT_CONTENT = ['pickle', 'json', 'msgpack', 'yaml']
    CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/5'
    CELERY_BROKER_URL = 'redis://127.0.0.1:6379/6'
    REDIS_URL = 'redis://localhost'

    @staticmethod
    def init_app(app):
        pass


class DevConfig(Config):
    DEBUG = True
    MONGODB_SETTINGS = {
        'db': 'ultrabear_homework',
        'host': 'localhost'
    }


class PrdConfig(Config):
    DEBUG = False
    MONGODB_SETTINGS = {
        'db': 'ultrabear_homework',
        'host': 'localhost',
        'port': PORT,
        "username": NAME,
        "password": PWD
    }


class TestingConfig(Config):
    TESTING = True
    DEBUG = True

    WTF_CSRF_ENABLED = False
    MONGODB_SETTINGS = {
        'db': 'Courses_test',
        'is_mock': True
    }


config = {
    'dev': DevConfig,
    'prd': PrdConfig,
    'testing': TestingConfig,
    'default': DevConfig,
}


