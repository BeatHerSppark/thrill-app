import os

from flask import Flask

UPLOAD_FOLDER = 'C:\\Users\\Peter\\Desktop\\realbeginnings\\thrill-app\\website\\static\\images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev'
    app.config['DATABASE'] = os.path.join(app.instance_path, 'website.sqlite')
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    
    from .views import views
    from .auth import auth
    from .api import api

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(api, url_prefix='/api')

    app.add_url_rule('/', endpoint='home')

    from . import db
    db.init_app(app)
    
    return app