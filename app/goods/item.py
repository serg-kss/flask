from flask import render_template, session, Blueprint, request
from app.models import Goods, Img
from app import app

item_bp = Blueprint('item',__name__)
template_road = 'goods/item.html'

@app.route('/item/<pk>')
def item(pk):
   item = Goods.query.filter(Goods.code_of_item == pk).first() 
   image_item = Img.query.filter(Img.code_of_pic == pk).first()                     
   return render_template(template_road, data=[item,image_item,session])


