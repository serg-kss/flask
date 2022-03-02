import json
import telebot
import requests
import datetime
import smtplib
from flask import Blueprint, flash, redirect, render_template, request, session
from app import app
from app import db
from app.models import Goods, Orders
from cloudipsp import Api, Checkout
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart




card_page_bp = Blueprint('card',__name__)
bot = telebot.TeleBot('5181107571:AAEw0wmrv8sFq4EgLOn1c9myHCOsgP_14LM')






@app.route('/card/<pk>',  methods =['POST', 'GET'])
def card(pk): 
       
    item = Goods.query.filter_by(code_of_item=pk).first()
       
    cart_item = {
      'name_of_item': item.name,
      'code': pk, 
      'price': item.price, 
      'amount': item.amount,
      'counter': 1
      }
       
    if 'card' in session:
       pass
    else:
       session['card'] = {}  
               
    if pk in session['card']:
       pass
    else:
       session['card'][pk] =cart_item
       session.modified = True
             
    if request.method == 'POST':
       payment = request.form['sum']
       session['payment']=payment
       session.modified = True
       return redirect('/check_out')
                                          
    return render_template('card/card.html', data=session)


@app.route('/delete_items')
def delete_items():
    if 'card' in session:
       session.pop('card')
      
    if 'payment' in session:
       session.pop('payment')  
    return redirect('/')


@app.route('/delete_one_item/<pk>')
def delete_one_items(pk):
    if pk in session['card']:    
      session['card'].pop(pk)
      session.modified = True
                          
    return redirect('/card') 


@app.route('/plus_one_item/<pk>')
def plus_one_item(pk):
               
   if pk in session['card']:
      if session['card'][pk]['amount'] >= session['card'][pk]['counter']:
         session['card'][pk]['counter']=session['card'][pk].get('counter')+1
         session.modified = True
         return redirect('/card')
      else:
         flash("Выбрано максимальное колличество доступного товара. Извините за неудобство!")
         return redirect('/card')
   return redirect('/card')


@app.route('/minus_one_item/<pk>')
def minus_one_item(pk):      
       
   if pk in session['card']:
            
      if session['card'][pk]['counter']==1:
         session['card'].pop(pk)
         session.modified = True
         return redirect('/card')
           
      if session['card'][pk]['counter']>1:
         session['card'][pk]['counter']=session['card'][pk].get('counter')-1
         session.modified = True
         return redirect('/card')
             
   return redirect('/card')   
 
 
@app.route('/card', methods =['POST', 'GET'])
def card_main():
   
   if request.method == 'POST':
       payment = request.form['sum']
       session['payment']=payment
       session.modified = True
       return redirect('/check_out')                            
   return render_template('card/card.html', data=session)
 
      
@app.route('/check_out', methods =['POST', 'GET'])
def check_out():
   if request.method == 'POST':
      x = Orders.query.count()
      if Orders.query.count() == 0:
         order_number = f"IHR{x}"
      elif Orders.query.count() > 0:
         order_number = f"IHR{x+1}"
         
      now = datetime.datetime.now()   
      date = now.strftime("%d-%m-%Y %H:%M")
      
      code_of_item = ""
      for key in session['card']:
         code_of_item = code_of_item + session['card'][key]['code']+ ", " 
                  
      buyer_data = f"{request.form['firstName']} {request.form['lastName']}"
      email = request.form['email']
      buyer_tel = request.form['phone']
      
      name = ""
      count = ""
      price = ""
      counter = 0
      for key in session['card']:
         counter = counter + 1          
         name = name + str(counter) + "| " + session['card'][key]['name_of_item']+ "; "
         count = count + str(counter) + "| " + str(session['card'][key]['counter'])+ " " +"шт. "
         price = price + str(counter) + "| " + str(session['card'][key]['price']) + " грн. "
            
      amount = session['payment']      
      delivery = request.form['delivery']         
      payment = request.form['paymentMethod']
      
      if delivery == "Самовывоз" and payment == "Оплата в точке самовывоза":
         order = Orders(order_number=order_number,
                     date=date,
                     code_of_item=code_of_item,
                     buyer_data=buyer_data,
                     email=email,
                     buyer_tel=buyer_tel,
                     name=name,
                     count=count,
                     price=price,
                     amount=amount,
                     delivery=delivery,
                     payment=payment                    
                     )
         db.session.add(order)
         db.session.commit()

         for el in session['card']:            
            try:
               c_amount = Goods.query.filter_by(code_of_item = str(el)).first()              
               new_amount = int(c_amount.amount - session['card'][el]['counter'])                            
               c_amount.amount = new_amount             
               db.session.commit()
            except:
               print('hren tam bil')
         
         # create message object instance
         msg = MIMEMultipart()
         message = f"Сформирован новый заказ № {order_number}: Наименование {name}, код {code_of_item}, колличество {count}, цена {price}, доставка {delivery}, оплата {payment}, имя клиента {buyer_data}, телефон {buyer_tel}"
         message_m = MIMEText(message, 'plain','utf-8') 
         # setup the parameters of the message
         password = "12Serg0591"
         msg['From'] = "pythontestflask@gmail.com"
         msg['To'] = "pythontestflask@gmail.com"
         msg['Subject'] = f"Новый Заказ {order_number}" 
         # add in the message body
         msg.attach(message_m)
         #create server
         server = smtplib.SMTP('smtp.gmail.com: 587')
         server.starttls()
         # Login Credentials for sending the mail
         server.login(msg['From'], password) 
         # send the message via the server.
         server.sendmail(msg['From'], msg['To'], msg.as_string().encode("utf-8"))
         server.quit()
         
         bot.send_message(chat_id=526088889,  text=message)
                                                                
         session.pop('card')
         session.pop('payment')
         url = f'/check_out_delivery/method1/{order_number}'              
         return redirect(url)      
      elif delivery == "Самовывоз" and payment == "Оплата на сайте":
         order = Orders(order_number=order_number,
                     date=date,
                     code_of_item=code_of_item,
                     buyer_data=buyer_data,
                     email=email,
                     buyer_tel=buyer_tel,
                     name=name,
                     count=count,
                     price=price,
                     amount=amount,
                     delivery=delivery,
                     payment=payment                    
                     )
         db.session.add(order)
         db.session.commit()
         
         for el in session['card']:            
            try:
               c_amount = Goods.query.filter_by(code_of_item = str(el)).first()              
               new_amount = int(c_amount.amount - session['card'][el]['counter'])                            
               c_amount.amount = new_amount             
               db.session.commit()
            except:
               print('hren tam bil') 
         
         session.pop('card')
         session.pop('payment')
         url = f'/check_out_delivery/method2/{order_number}'              
         return redirect(url)
      elif delivery == "Новая почта" and payment == "Оплата в отделении Новая Почта":
         order = Orders(order_number=order_number,
                     date=date,
                     code_of_item=code_of_item,
                     buyer_data=buyer_data,
                     email=email,
                     buyer_tel=buyer_tel,
                     name=name,
                     count=count,
                     price=price,
                     amount=amount,
                     delivery=delivery,
                     payment=payment                    
                     )
         db.session.add(order)
         db.session.commit()
         
         url = f'/check_out_delivery/method3/{order_number}'              
         return redirect(url)
      elif delivery == "Новая почта" and payment == "Оплата на сайте":
         order = Orders(order_number=order_number,
                     date=date,
                     code_of_item=code_of_item,
                     buyer_data=buyer_data,
                     email=email,
                     buyer_tel=buyer_tel,
                     name=name,
                     count=count,
                     price=price,
                     amount=amount,
                     delivery=delivery,
                     payment=payment                    
                     )
         db.session.add(order)
         db.session.commit()
         session.pop('card')
         session.pop('payment')
         url = f'/check_out_delivery/<{order_number}>'              
         return redirect(url)     
      else:
         flash("Проверьте пожалуйста правильность заполнения разделов: Доставка и Оплата")
         return redirect('/check_out')
  
   return render_template('card/check_out.html', data = [session])


@app.route('/check_out_delivery/method1/<pk>', methods=['get', 'post'])
def check_out_delivery_m1(pk):
   order_number = pk
   string = f"Заказ {order_number} успешно сформирован, мы с Вами свяжемся в ближайшее аремя!"

      
   return render_template('card/check_out_delivery.html', data=[string])


@app.route('/check_out_delivery/method2/<pk>')
def check_out_delivery_m2(pk):
   total_sum_order = Orders.query.filter_by(order_number=pk).first()
   fondy_sum = round(float(total_sum_order.amount)*100)        
   api = Api(merchant_id=1396424, secret_key='test')
   checkout = Checkout(api=api)
   data = {
      "currency": "UAH",
      "amount": fondy_sum
   }
   try:
      url = checkout.url(data).get('checkout_url')
      return redirect(url)
   except BaseException:     
      return redirect('/card')
   

@app.route('/check_out_delivery/method3/<pk>', methods =['POST', 'GET'])
def check_out_delivery_m3(pk):
   pk=pk
   
   def get():
      url = 'https://api.novaposhta.ua/v2.0/json/'
      
      x_json = """{"modelName": "Address", "calledMethod": "getCities", "apiKey": "e3b0e87c7311099d1f91a0282ab542b7"}"""

      r = requests.post(url=url, data=x_json)
      unswer_dict = dict(r.json())
      return unswer_dict
   
   city_info = get()
   
   if request.method == 'POST':
      code_of_city = request.form['city']
      session['code_of_city']=code_of_city
      r_url = f'/check_out_delivery/method3/city/{pk}'
      return redirect(r_url)
      
   return render_template('card/check_out_delivery_post.html', data=[city_info])


@app.route('/check_out_delivery/method3/city/<pk>', methods =['POST', 'GET'])
def check_out_delivery_m3_city(pk):
   pk=pk
                          
   def get():
      url = 'https://api.novaposhta.ua/v2.0/json/'
         
      x_json = {
            "modelName": "Address",
            "calledMethod": "getWarehouses",
            "methodProperties": {
               "CityName": str(session['code_of_city'])
            },
            "apiKey": "e3b0e87c7311099d1f91a0282ab542b7"
         }
      x = json.dumps(x_json)      
         
      r = requests.post(url=url, data=x)
      unswer_dict = dict(r.json())
      
      return unswer_dict
        
   post_points_dict = get()
   name_of_city = str(session['code_of_city'])
   
   if request.method == 'POST':
      delivery_point = request.form['point']
      session['delivery_point'] = delivery_point
      url_order_close = f"/check_out_delivery/method3/order_close/{pk}"
      return redirect(url_order_close)
   
   return render_template('card/check_out_delivery_post_points.html', data=[post_points_dict, name_of_city])
   

@app.route('/check_out_delivery/method3/order_close/<pk>')
def post_order_close(pk):
   
   for el in session['card']:            
            try:
               c_amount = Goods.query.filter_by(code_of_item = str(el)).first()              
               new_amount = int(c_amount.amount - session['card'][el]['counter'])                            
               c_amount.amount = new_amount             
               db.session.commit()
            except:
               print('hren tam bil') 
   
   string_order = f"Заказ {pk} успешно сформирован, мы с Вами свяжемся в ближайшее аремя!"
   string_delivery = f"Доставка Новая Почта: г. {session['code_of_city']} в {session['delivery_point']}"
   session.pop('code_of_city')
   session.pop('delivery_point')
   session.pop('card')
   session.pop('payment')
      
   return render_template('card/check_out_delivery.html', data = [string_order, string_delivery])


   




   






