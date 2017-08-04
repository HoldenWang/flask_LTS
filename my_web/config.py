#coding=utf-8

import os

#配置数据库路径
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
	SECRET_KEY=os.environ.get('SECRET_KEY') or 'hard to guess string'
	SQLALCHEMY_COMMIT_ON_TEARDOWN=True

	@staticmethod
	def init_app(app):
		pass

class ProductionConfig(Config):
	SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL') or \
	'sqlite:///' + os.path.join(basedir, 'data.sqlite')

config={
	'production':ProductionConfig,
	'default':ProductionConfig
}