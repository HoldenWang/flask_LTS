# coding=utf-8

from flask import Flask 
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy 
from config import config
#此处的config来自上一级目录，跟启动脚本同级，所以可能允许这种方法导入？？？？

bootstrap = Bootstrap()
moment = Moment()
db = SQLAlchemy()

def create_app(config_name):
	app=Flask(__name__)
	app.config.from_object(config[config_name])
	config[config_name].init_app(app)

	bootstrap.init_app(app)
	moment.init_app(app)
	db.init_app(app)

	from .main import main as main_blueprint
	app.register_blueprint(main_blueprint)

	return app

