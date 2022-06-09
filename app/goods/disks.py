from flask import render_template, session, Blueprint, request
from app.models import Goods, Img
from app import app

disks_bp = Blueprint('disks',__name__)
category = 2
template_road = 'goods/disks.html'

@app.route('/disks', methods=['GET','POST'])
def disks():
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


