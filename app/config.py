DEBUG = True
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = True
#SQLALCHEMY_DATABASE_URI = 'mysql://weibospider:wangjipeng@192.168.1.124/flask?charset=utf8'
#SQLALCHEMY_BINDS = {
#		'p4lab':        'mysql+pymysql://pk4yo:pk4yo@2017@172.16.9.69/ailab?charset=utf8',
#		'articles':      'mysql+pymysql://pk4yo:pk4yo@2017@172.16.9.69/webspider?charset=utf8'
#		}
SQLALCHEMY_BINDS = {
		'meiyo':        'mysql+pymysql://juncheng:qwer1234@192.168.8.215/meiyo?charset=utf8'
		}
#SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://juncheng:qwer1234@192.168.1.110/p4lab?charset=utf8'
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SECRET_KEY = '*\xff\x93\xc8w\x13\x0e@3\xd6\x82\x0f\x84\x18\xe7\xd9\\|\x04e\xb9(\xfd\xc3'
