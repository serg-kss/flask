from flask import render_template, session,Blueprint,request
from app.models import Goods, Img
from app import app


tyres_bp = Blueprint('tyres',__name__)
category = 1
template_road = 'goods/tyres.html'

@app.route('/tyres', methods=['GET','POST'])
def tyres():
   goods = Goods.query.filter_by(category=category) 
   image = Img.query.order_by(Img.id).all() 
   
   if request.method == 'POST':
      filterPrice = request.form['filterPrice'] 
      
      if filterPrice == 'cheep':
         goods = Goods.query.filter_by(category=category).order_by(Goods.price).all()
         return render_template(template_road, data=[goods,image,session])
      elif filterPrice == 'expensive':
         goods = Goods.query.filter_by(category=category).order_by(Goods.price.desc()).all()
         return render_template(template_road, data=[goods,image,session])
   
   
                       
   return render_template(template_road, data=[goods,image,session])


