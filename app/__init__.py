from flask import Flask, render_template,session
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import datetime
from flask_mail import Mail, Message
from flask_restful import Api

def create_app():
    app = Flask(__name__)   
    return app


app = create_app()
app.config.from_pyfile('../config-extended.py')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///internetshop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECURITY_PASSWORD_SALT'] = '12Serg0591'
app.secret_key = '12Serg0591'
app.permanent_session_lifetime = datetime.timedelta(days=365)
api = Api(app)



db = SQLAlchemy(app)
migrate = Migrate(app, db)
db.create_all()


# Ставим редирект, если пользователь не авторизован, для страниц где обязательна авторизация
login_manager = LoginManager(app)
login_manager.login_view = 'admin_blueprint.login'

# Регистрация путей Blueprint
from app.admin.routes import admin_bp
from app.main_page.main_page import main_page_bp
from app.card.card import card_page_bp


app.register_blueprint(card_page_bp)
app.register_blueprint(admin_bp, url_prefix="/admin")
app.register_blueprint(main_page_bp)




       


