#coding=utf-8

from flask import Blueprint

main=Blueprint('main',__name__)

#放在最后导入，是为了避免循环导入，views.py和errors.py中同样要导入main
from . import views, errors