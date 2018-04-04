# -*- encoding: utf-8 -*-
from app import create_app
from app.modules.home.views import homeRoute
from app.modules.user.views import userRoute
from app.modules.article.views import articleRoute
from flask_cors import *

DEFAULT_MODULES = [homeRoute,
                   userRoute,
                   articleRoute]

def create_aapp():
    app = create_app('config.py')
    CORS(app, supports_credentials=True)
    return app

#app = create_app('config.py')
#CORS(app, supports_credentials=True)

application = create_aapp()

for module in DEFAULT_MODULES:
    application.register_blueprint(module)


#@app.before_request
@application.before_request
def before_request():
    """
    这里是全局的方法，在请求开始之前调用。
    其中 flask 有个全局的变量 g，它是和 session 一样的用途，可以使用它来保存当前用户的数据
    Returns:

    """
    pass


if __name__ == '__main__':
    application.run()
    #app.run(host="::",port=8080)
