#coding=utf-8

from flask_wtf import Form
from wtforms import StringField, SubmitField, TextAreaField, PasswordField
from wtforms.validators import Required
from flask_pagedown.fields import PageDownField

#表单
class LoginForm(Form):
	name = StringField('What is your name?',validators=[Required()])
	password = PasswordField('What is your password?',validators=[Required()])
	submit = SubmitField('Login')
	
class RegisterForm(Form):
	name = StringField('input your name?',validators=[Required()])
	password = PasswordField('input your password',validators=[Required()])
	password_re = PasswordField('reform your password',validators=[Required()])
	submit = SubmitField('Register')

class MessageForm(Form):
	title = TextAreaField(u"Title", render_kw={"rows": 1, "cols": 11})
	#author = TextAreaField(u"Author", render_kw={"rows": 1, "cols": 11})
	body = PageDownField("What's on your mind ?",validators=[Required()])
	#message = TextAreaField("Content",default="please add sth",render_kw={"rows": 20, "cols": 11})
	submit = SubmitField('submit')

class MessageForm_single(Form):
	title = TextAreaField(u"Title", render_kw={"rows": 1, "cols": 11})
	body = PageDownField("What's on your mind ?",validators=[Required()])
	submit = SubmitField('submit')