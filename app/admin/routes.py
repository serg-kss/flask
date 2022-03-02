import base64
from flask import Blueprint, flash, redirect, render_template, request
from werkzeug.utils import secure_filename
from app import db
from app import app
from app.models import Img


admin_bp = Blueprint('admin_blueprint', __name__)


@app.route('/upload_img_to_database',  methods=['GET','POST'])

def upload():
    if request.method == 'POST':
        code = request.form['code']
        pic = request.files['pic']
        blobData = pic.read()
        image_64_encode = base64.b64encode(blobData)
        if not pic:
            return 'No pic uploaded!', 400

        filename = secure_filename(pic.filename)
        mimetype = pic.mimetype
        if not filename or not mimetype:
            return 'Bad upload!', 400

        img = Img(img=(str(image_64_encode,'utf-8')), name=filename, mimetype=mimetype, code_of_pic=code)
        db.session.add(img)
        db.session.commit()
        flash(f"Вы добавили новое изображение с артикулом {code}")

        return redirect('/upload_img_to_database')
   
    else:   
        return render_template('admin/create_pic.html')
    




      
      
     
      
    

