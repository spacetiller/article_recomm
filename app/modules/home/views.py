# -*- encoding: utf-8 -*- 编码

from flask import Blueprint
from flask import render_template, flash, session, g

homeRoute = Blueprint('home', __name__, url_prefix='/', template_folder='templates')


@homeRoute.route('/')
def index():
    if session.get('username') and session.get('password') :
        flash("你已经登陆" + session.get('username'))
    else:
        flash("未登陆")
    return render_template('index.html')
