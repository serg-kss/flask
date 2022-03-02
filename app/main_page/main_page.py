from flask import Blueprint, render_template, session
from app.models import Goods, Img
from app import app
main_page_bp = Blueprint('main_page',__name__)


@app.route('/')
def main_page():
   goods = Goods.query.order_by(Goods.price).all() 
   image = Img.query.order_by(Img.id).all()                     
   return render_template('main_page/main_page.html', data=[goods,image,session])


@app.route('/about')
def about():   
   return render_template('main_page/about.html',data=session)