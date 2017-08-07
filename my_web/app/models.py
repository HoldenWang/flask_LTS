# -*- coding: utf-8 -*-  
#coding=utf-8

from . import db
from markdown import markdown
import bleach

class Role(db.Model):
	__tablename__ = 'roles'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), unique=True)
	# backref 相当于在users表中增加了一列属性role,默认情况下自动匹配外键foreignkey
	users = db.relationship('User', backref='role', lazy='dynamic')

	def __repr__(self):
		return '<Role %r>' % self.name

class User(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), unique=True, index=True)
	password = db.Column(db.String(64))
	role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

	def __repr__(self):
		return '<User %r>' % self.username

class Content(db.Model):
	__tablename__ = 'contents'
	id = db.Column(db.Integer, primary_key=True)
	passage_name = db.Column(db.String(32))
	author = db.Column(db.String(64))
	edit_time = db.Column(db.DateTime)
	passage = db.Column(db.Text)
	body_html = db.Column(db.Text)
	@staticmethod
	def on_change_body(target, value, oldvalue, initiator):
		allowed_tags = ['a', 'abbr', 'code', 'ul', 'strong', 'pre' ]
		target.body_html = bleach.linkify(bleach.clean(markdown(value,output_format='html'),\
			tags=allowed_tags))

	def __repr__(self):
		return '<Content %r>' % self.passage_name
