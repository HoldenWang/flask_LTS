#coding=utf-8

from flask import render_template, session,redirect, url_for
from datetime import datetime

from . import main
from .forms import NameForm,MessageForm
from .. import db
from ..models import User,Role,Content

#路由和视图函数
@main.route('/',methods=['GET','POST'])
def index():
	name = None
	form = NameForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.name.data).first()
		# 此处执行查询操作的如果不是fisrt而是all，则返回的是一个list，len(user)返回长度
		# 意味着不能用user.password这种方式而是user[0].password
		if user is None:
			user = User(username=form.name.data)
			db.session.add(user)
			session['known'] = False
			return redirect(url_for('.index'))
		else:
			session['known'] = True
			if form.password.data == user.password:
				print "nice try"
				return redirect(url_for('.edit_content',name=user.username))

		session['name'] = form.name.data
		session['password'] = form.password.data
		
		form.name.data = ''
		form.password.data = ''
	return render_template('index.html',\
		form=form, name=session.get('name'), \
		known = session.get('known',False),current_time=datetime.utcnow())

@main.route('/user/<id>')
def get_id(id):
	return '<h1> Hello, %s!</h1>' % id

@main.route('/user/<name>/content/edit',methods=['GET','POST'])
def edit_content(name):
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

	return render_template('content.html',form=form),520

@main.route('/message/<passage_id>',methods=['GET','POST'])
def show_content(passage_id):
	#content = Content.query.all()
	cont=Content.query.filter_by(id=passage_id).first()
	#num = len(content)
	#print "the num of content:"num
	title=cont.passage_name
	author=cont.author
	time=cont.edit_time
	content=cont.passage
	return render_template('content_show.html',\
		title=title,author=author,time=time,content=content) 

@main.route('/message/all',methods=['GET','POST'])
def show_all_content():
	posts=Content.query.order_by(Content.edit_time.desc()).all()
	return render_template('content_show.html',posts=posts)
