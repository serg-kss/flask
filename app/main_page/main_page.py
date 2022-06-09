from flask import Blueprint, render_template, request, session
from app.models import Goods, Img
from app import app
main_page_bp = Blueprint('main_page',__name__)


category = 1
template_road = 'main_page/main_page.html'
template_road_about = 'main_page/about.html'
POSTS_PER_PAGE = 3


@app.route('/', methods = ['GET', 'POST'])
def index():
   page = request.args.get('page', 1, type=int)
   goods = Goods.query.filter_by(category=category).paginate(page=page, per_page=POSTS_PER_PAGE)
   image = Img.query.all()      
   
   if request.method == 'POST':
      filterPrice = request.form['filterPrice'] 
      
      if filterPrice == 'cheep':
         goods = Goods.query.order_by(Goods.price).filter_by(category=category).paginate(page=page, per_page=POSTS_PER_PAGE)
         return render_template(template_road, data=[goods,image,session])
      elif filterPrice == 'expensive':
         goods = Goods.query.order_by(Goods.price.desc()).filter_by(category=category).paginate(page=page, per_page=POSTS_PER_PAGE)
         return render_template(template_road, data=[goods,image,session]) 
                      
   return render_template(template_road, data=[goods,image,session])


@app.route('/about')
def about():   
   return render_template(template_road_about, data=session)