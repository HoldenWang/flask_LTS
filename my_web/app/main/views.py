#coding=utf-8

from flask import render_template, session,redirect, url_for, flash,abort
from datetime import datetime

from . import main
from .forms import LoginForm,MessageForm,RegisterForm,MessageForm_single
from .. import db
from ..models import User,Role,Content

#路由和视图函数
@main.route('/',methods=['GET','POST'])
def index():
	name = None
	login = LoginForm()
	register = RegisterForm()

	if login.validate_on_submit():
		user = User.query.filter_by(username=login.name.data).first()
		# 此处执行查询操作的如果不是fisrt而是all，则返回的是一个list，len(user)返回长度
		# 意味着不能用user.password这种方式而是user[0].password
		if user is None:
			#user = User(username=login.name.data)
			#db.session.add(user)
			session['known'] = False
			session['name'] = login.name.data
			return redirect(url_for('.index'))
		else:
			session['known'] = True
			if login.password.data == user.password:
				print "nice try"
				session['passed_user']=login.name.data
				return redirect(url_for('.create_content',name=user.username))

		session['name'] = login.name.data
		session['password'] = login.password.data
		
		login.name.data = ''
		login.password.data = ''	

	return render_template('index.html',\
		form_login=login, name=session.get('name'), \
		known = session.get('known',False),current_time=datetime.utcnow())

@main.route('/register',methods=['GET','POST'])
def register():
	form = RegisterForm()
	if form.validate_on_submit():
		print 'registering'
		#flash('make sure input the same password or the name has been registered by others:)')
		reged=User.query.filter_by(username=form.name.data).first()
		if form.password_re.data == form.password.data and reged is None:
			new_user=User(username=form.name.data,password=form.password.data,role_id=2)
			db.session.add(new_user)
			db.session.commit()
			return redirect(url_for('.index'))
		else:
			flash('make sure input the same password or the name has been registered by others:)')
	return render_template('register.html',form_reg=form,current_time=datetime.utcnow())

@main.route('/user/<id>')
def get_id(id):
	return '<h1> Hello, %s!</h1>' % id

@main.route('/user/<name>/content/create',methods=['GET','POST'])
def create_content(name):
	msg = None
	form = MessageForm()
	if form.validate_on_submit():
		content = Content(passage_name=form.title.data,author=name,\
			edit_time=datetime.utcnow(),passage=form.body.data )
		
		db.session.add(content)
		db.session.commit()
		passage_id = content.id
		print content.id
		print 'debug1'
		return redirect(url_for('.show_all_content',passage_id=passage_id))
    	form.title.data=''
        form.body.data=''

	return render_template('create_content.html',form=form),520

@main.route('/post/<int:passage_id>',methods=['GET','POST'])
def show_content(passage_id):
	cont=Content.query.get_or_404(passage_id)
	# form = MessageForm_single()
	#num = len(content)
	#print "the num of content:"num
	content=cont.passage
	return render_template('post_content.html',post=cont) 

@main.route('/edit/<passage_id>',methods=['GET','POST'])
def edit_content(passage_id):
	cont=Content.query.filter_by(id=passage_id).first()
	form = MessageForm_single()
	if session['passed_user']!=cont.author:
		abort(403)
	if form.validate_on_submit() and session['passed_user']==cont.author:
		cont.title=form.title.data
		cont.passage=form.body.data
		cont.edit_time=datetime.utcnow()
		db.session.add(cont)
		flash("the message has be update.")
		return redirect(url_for('.show_content',passage_id=cont.id))
	#num = len(content)
	#print "the num of content:"num
	form.title.data=cont.passage_name
	form.body.data=cont.passage
	return render_template('edit_content.html',form=form) 

@main.route('/message/all',methods=['GET','POST'])
def show_all_content():
	posts=Content.query.order_by(Content.edit_time.desc()).all()
	return render_template('content_show.html',posts=posts)
