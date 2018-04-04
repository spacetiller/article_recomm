# -*- encoding: utf-8 -*- 编码

from flask import Flask
from flask_login import LoginManager

#from app.modules.users.models.users import User

from app.common.data import db

from app.common.log import logger

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


"""
初始化登录管理器
"""
login_manager = LoginManager()

"""
这里的参数格式是：蓝图名称.函数名
这里是指定了当用户未登录的时候，进入需要登录才能进入的页面时，会自动跳转到的页面。
"""
login_manager.login_view = "user.login"
login_manager.login_message = u"用户未登录"

def create_app(config_filename=None):
    app = Flask(__name__)
    login_manager.init_app(app)
    logger.debug("module login_manager.init_app() __init__")

    if config_filename is not None:
        # 注册数据访问信息
        app.config.from_pyfile(config_filename)
        logger.debug("app.config.from_pyfile __config__")

        # 初始化数据库
        configure_database(app)
    else:	#  后增，如果没有配置文件，就使用本地 sqlite3 数据库。 可能造成混乱
        SQLALCHEMY_DATABASE_URI = 'sqlite:///foo.db'
        SQLALCHEMY_TRACK_MODIFICATIONS = True  # FSADeprecationWarning: SQLALCHEMY_TRACK_MODIFICATIONS adds significant overhead and will be disabled by default in the future.  Set it to True or False to suppress this warning.
        app.config.from_object(__name__)
        logger.error("No config file found. app.config.from_object __config__")
    return app


def configure_database(app):
    """初始化数据库连接。
    Args:
        app:应用对象。
    Returns:
        该函数没有返回值。
    """
    db.init_app(app)
    logger.debug("module db __init__")
    
    app.app_context().push()
    db.create_all()		# 如果表不存在，则创建表
    logger.debug("db tables constructed if not exist __init__")
