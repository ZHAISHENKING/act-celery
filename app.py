import logging
from flask import Flask, jsonify, request
from flask_cors import CORS
from routes import docs
from config import config
from werkzeug.utils import import_string
from homework.models import *
from wechat.models import *
from flask_babelex import Babel
from admin import admin, MyModelView, AdminUser, login, limiter
from flask_admin.contrib.mongoengine import ModelView
from homework.view import ActModelView, StudentModelView
from wechat.view import OauthModelView
from production import *
from rsync_tasks import celery, redis
try:
    from local_settings import *
except Exception:
    pass

blueprints = ['routes:uploadApi']

admin.add_view(StudentModelView(name="APP合作"))
admin.add_view(ModelView(Consultation, name="官网首页"))
admin.add_view(ModelView(ClassInfo, name="学生预约课"))
admin.add_view(ActModelView(name="作业帮活动"))
admin.add_view(OauthModelView(name="微信多平台"))
admin.add_view(ModelView(Operation, name="访客记录"))


# 初始化app
def create_app(config_name):
    app = Flask(config_name)
    app.config.from_object(config[config_name])

    # 全局响应头
    @app.after_request
    def after_request(response):
        if "Access-Control-Allow-Origin" not in response.headers.keys():
            response.headers['Access-Control-Allow-Origin'] = '*'
        if request.method == 'OPTIONS':
            response.headers['Access-Control-Allow-Methods'] = 'DELETE, GET, POST, PUT'
            headers = request.headers.get('Access-Control-Request-Headers')
            if headers:
                response.headers['Access-Control-Allow-Headers'] = headers
        return response

    # 自定义错误日志
    handler = logging.FileHandler('app.log', encoding='UTF-8')
    logging_format = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
    handler.setFormatter(logging_format)
    app.logger.addHandler(handler)

    def init_login():
        login_manager = login.LoginManager()
        login_manager.setup_app(app)

        # Create user loader function
        @login_manager.user_loader
        def load_user(user_id):
            return AdminUser.objects(id=user_id).first()

    @app.errorhandler(404)
    def page_not_found(e):
        return jsonify(msg='404 page not found')

    # 注册所有蓝图
    for bp_name in blueprints:
        bp = import_string(bp_name)
        app.register_blueprint(bp)

    config[config_name].init_app(app)
    babel = Babel(app)
    db.init_app(app)
    docs.init_app(app)
    admin.init_app(app)
    init_login()
    limiter.init_app(app)
    celery.init_app(app)
    redis.init_app(app)
    celery.conf.update(app.config)

    db.register_connection(
        db='ultrabear_homework',
        alias="home",
        port=PORT,
        username=NAME,
        password=PWD
    )
    # 跨域
    CORS(app, supports_credentials=True)
    return app
