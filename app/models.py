from datetime import datetime
from itertools import count
from flask_login import UserMixin
from flask_security import RoleMixin
from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash


roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('roles.id'))
)


class Role(db.Model, RoleMixin):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String)
    username = db.Column(db.String, unique=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    # Нужен для security!
    active = db.Column(db.Boolean())
    # Для получения доступа к связанным объектам
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))

    # Flask - Login
    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    # Flask-Security
    def has_role(self, *args):
        return set(args).issubset({role.name for role in self.roles})

    def get_id(self):
        return self.id

    # Required for administrative interface
    def __unicode__(self):
        return self.username

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


# Отвечает за сессию пользователей. Запрещает доступ к роутам, перед которыми указано @login_required
@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)


class Img(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.Text, unique=True, nullable=False)
    name = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)
    code_of_pic = db.Column(db.String(20),nullable = False, unique=True)

class Goods(db.Model):
    __tablename__ = 'товары'
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    code_of_item = db.Column(db.String(20),nullable = False, unique=True)
    name = db.Column(db.String(200), nullable = False)
    price = db.Column(db.Float, nullable = False)
    price_fondy = db.Column(db.Integer, nullable = False)
    amount = db.Column(db.Integer, nullable = False)  
    text = db.Column(db.Text, nullable = True)
    
 
   
    def __repr__(self) -> str:
       return self.name
   
   
class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(30), nullable = False,unique=True)
    date = db.Column(db.String(30), nullable = False)
    code_of_item = db.Column(db.String(200),nullable = False)
    buyer_data = db.Column(db.String(200),nullable = False)
    email = db.Column(db.String, nullable = True)
    buyer_tel = db.Column(db.String(200),nullable = False)    
    name = db.Column(db.String(800), nullable = False)
    count = db.Column(db.String(200),nullable = False)
    price = db.Column(db.String(800), nullable = False)
    amount = db.Column(db.Integer, nullable = False)
    delivery = db.Column(db.String(30), nullable = False)
    payment = db.Column(db.String(30), nullable = False)