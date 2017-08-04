# -*- coding: utf-8 -*-  
#coding=utf-8
# import os
# from flask import Flask , render_template,session,redirect, url_for
# from flask_script import Manager, Shell
# from flask_bootstrap import Bootstrap
# from flask_moment import Moment
# from datetime import datetime
# from flask_wtf import Form
# from wtforms import StringField, SubmitField, TextAreaField, PasswordField
# from wtforms.validators import Required
# from flask_sqlalchemy import SQLAlchemy 
# from flask_migrate import Migrate, MigrateCommand

# #配置数据库路径
# basedir = os.path.abspath(os.path.dirname(__file__))

#app = Flask(__name__)
# manager = Manager(app)
# bootstrap = Bootstrap(app)
# moment = Moment(app)
# db = SQLAlchemy(app)
# migrate = Migrate(app, db)

#数据库相关配置
app.config['SQLALCHEMY_DATABASE_URI']=\
'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

# #注册回调函数，方便导入数据库
# def make_shell_context():
# 	return dict(app=app, db=db, User=User, Role=Role, Content=Content )
# manager.add_command("shell", Shell(make_context=make_shell_context))
# manager.add_command('db', MigrateCommand)

# #定义数据库模型
# class Role(db.Model):
# 	__tablename__ = 'roles'
# 	id = db.Column(db.Integer, primary_key=True)
# 	name = db.Column(db.String(64), unique=True)
# 	# backref 相当于在users表中增加了一列属性role,默认情况下自动匹配外键foreignkey
# 	users = db.relationship('User', backref='role', lazy='dynamic')

# 	def __repr__(self):
# 		return '<Role %r>' % self.name

# class User(db.Model):
# 	__tablename__ = 'users'
# 	id = db.Column(db.Integer, primary_key=True)
# 	username = db.Column(db.String(64), unique=True, index=True)
# 	password = db.Column(db.String(64))
# 	role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

# 	def __repr__(self):
# 		return '<User %r>' % self.username

# class Content(db.Model):
# 	__tablename__ = 'contents'
# 	id = db.Column(db.Integer, primary_key=True)
# 	passage_name = db.Column(db.String(32))
# 	author = db.Column(db.String(64))
# 	edit_time = db.Column(db.DateTime)
# 	passage = db.Column(db.Text)

# 	def __repr__(self):
# 		return '<Content %r>' % self.passage_name

#防止CSRF，使用wtf必须
app.config['SECRET_KEY']="are you kiding"

#####################################################################
# #表单
# class NameForm(Form):
# 	name = StringField('What is your name?',validators=[Required()])
# 	password = PasswordField('What is your password?',validators=[Required()])
# 	submit = SubmitField('Submit')

# class MessageForm(Form):
# 	title = TextAreaField(u"Title", render_kw={"rows": 1, "cols": 11})
# 	#author = TextAreaField(u"Author", render_kw={"rows": 1, "cols": 11})
# 	message = TextAreaField("Content",default="please add sth",render_kw={"rows": 20, "cols": 11})
# 	submit = SubmitField('submit')

######################################################################
# #路由和视图函数
# @app.route('/',methods=['GET','POST'])
# def index():
# 	name = None
# 	form = NameForm()
# 	if form.validate_on_submit():
# 		user = User.query.filter_by(username=form.name.data).first()
# 		# 此处执行查询操作的如果不是fisrt而是all，则返回的是一个list，len(user)返回长度
# 		# 意味着不能用user.password这种方式而是user[0].password
# 		if user is None:
# 			user = User(username=form.name.data)
# 			db.session.add(user)
# 			session['known'] = False
# 			return redirect(url_for('index'))
# 		else:
# 			session['known'] = True
# 			if form.password.data == user.password:
# 				print "nice try"
# 				return redirect(url_for('edit_content',name=user.username))

# 		session['name'] = form.name.data
# 		session['password'] = form.password.data
		
# 		form.name.data = ''
# 		form.password.data = ''
# 	return render_template('index.html',\
# 		form=form, name=session.get('name'), \
# 		known = session.get('known',False),current_time=datetime.utcnow())

# @app.route('/user/<id>')
# def get_id(id):
# 	return '<h1> Hello, %s!</h1>' % id

# @app.route('/user/<name>/content/edit',methods=['GET','POST'])
# def edit_content(name):
# 	msg = None
# 	form = MessageForm()
# 	if form.validate_on_submit():
# 		content = Content(passage_name=form.title.data,author=name,\
# 			edit_time=datetime.utcnow(),passage=form.message.data )
		
# 		db.session.add(content)
# 		db.session.commit()
# 		passage_id = content.id
# 		print content.id
# 		print 'debug1'
# 		return redirect(url_for('show_all_content',passage_id=passage_id))
#     	form.title.data=''
#         form.message.data=''

# 	return render_template('content.html',form=form),520

# @app.route('/message/<passage_id>',methods=['GET','POST'])
# def show_content(passage_id):
# 	#content = Content.query.all()
# 	cont=Content.query.filter_by(id=passage_id).first()
# 	#num = len(content)
# 	#print "the num of content:"num
# 	title=cont.passage_name
# 	author=cont.author
# 	time=cont.edit_time
# 	content=cont.passage
# 	return render_template('content_show.html',\
# 		title=title,author=author,time=time,content=content) 

# @app.route('/message/all',methods=['GET','POST'])
# def show_all_content():
# 	posts=Content.query.order_by(Content.edit_time.desc()).all()
# 	return render_template('content_show.html',posts=posts)


# @app.errorhandler(404)
# def page_not_found(e):
# 	return render_template('404.html'),404

# @app.errorhandler(500)
# def page_not_found(e):
# 	return render_template('500.html'),500

# if __name__ == '__main__':
# 	#app.run(debug=True)
# 	manager.run()
# 	