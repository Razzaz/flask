from datetime import timedelta
from types import MethodType
from flask import Flask, redirect, url_for, render_template, request, session, flash, Response
import urllib.request
import os
from werkzeug.utils import secure_filename

from db import db_init, db
from models import Img


app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads/'

app.secret_key = "gru-sketch"

# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///img.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db_init(app)

# ALLOWED_EXTENSIONS = set(['png'])


# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def home():
    return render_template("index.html")


@app.route('/upload', methods=['POST'])
def upload():
    pic = request.files['pic']

    if not pic:
        return 'No pic uploaded', 400

    filename = secure_filename(pic.filename)
    mimetype = pic.mimetype
    img = Img(img=pic.read(), mimetype=mimetype, name=filename)
    db.session.add(img)
    db.session.commit()

    return 'Image has been uploaded', 200


@app.route('/<int:id>')
def get_img(id):
    img = Img.query.filter_by(id=id).first()

    if not img:
        return 'No image with that id'

    return Response(img.img, mimetype=img.mimetype)


# @app.route("/", methods=['POST'])
# def upload_image():
#     if 'file' not in request.files:
#         flash('No file part')
#         return redirect(request.url)
#     file = request.files['file']
#     if file.filename == '':
#         flash('No image selected for uploading')
#         return redirect(request.url)
#     if file and allowed_file(file.filename):
#         filename = secure_filename(file.filename)
#         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#         #print('upload_image filename: ' + filename)
#         flash('Image successfully uploaded and displayed below')
#         return render_template('index.html', filename=filename)
#     else:
#         flash('Allowed image types are - png, jpg, jpeg, gif')
#         return redirect(request.url)


if __name__ == "__main__":
    app.run(debug=True)
