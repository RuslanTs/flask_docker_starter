from flask import Flask, request, jsonify, flash, \
    abort, redirect, url_for, render_template, send_file
import numpy as np
import pickle
import os
from werkzeug.utils import secure_filename
from flask_wtf import FlaskForm
from wtforms import StringField
from flask_wtf.file import FileField
from wtforms.validators import DataRequired
import pandas as pd

app = Flask(__name__)
knn = pickle.load(open('model.pkl', "rb"))


@app.route('/')
def hello_world():
    return '<h1>Hello, Darling!!!</h1>'


@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    username = float(username) * float(username)
    return f'User {username}'


def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)


@app.route('/avg/<nums>')
def avg(nums):
    nums = nums.split(',')
    nums = [float(num) for num in nums]
    nums_mean = mean(nums)
    print(nums_mean)
    return str(nums_mean)


@app.route('/iris/<params>')
def iris(params):

    params = params.split(',')
    params = [float(num) for num in params]
    params = np.array(params).reshape(1, -1)
    predict = knn.predict(params)

    return show_image(predict)


@app.route('/show_image/<iris>')
def show_image(iris):

    setosa = '<img src="/static/setosa.jpg" alt="setosa">'
    virginica = '<img src="/static/virginica.jpg" alt="virginica">'
    versicolor = '<img src="/static/versicolor.jpg" alt="versicolor">'
    images = {0: setosa, 1: versicolor, 2: virginica}
    return images[int(iris)]


@app.route('/iris_post', methods=['POST'])
def add_message():

    try:
        content = request.get_json()
        # print(content) # Do your processing

        params = content['flower'].split(',')
        params = [float(num) for num in params]
        params = np.array(params).reshape(1, -1)
        predict = knn.predict(params)

        predict = {'class': int(predict[0])}
    except:
        return redirect(url_for('bad_request'))

    return jsonify(predict)


@app.route('/badrequest400')
def bad_request():
    abort(400)


class MyForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    file = FileField()


@app.route('/submit', methods=('GET', 'POST'))
def submit():
    form = MyForm()
    if form.validate_on_submit():
        print(form.name.data)

        f = form.file.data
        filename = form.name.data + '.csv'
        df = pd.read_csv(f, header=None)

        predict = knn.predict(df)
        result = pd.DataFrame(predict)
        result.to_csv(filename, index=False, header=False)

        return send_file(filename,
                         mimetype='text/csv',
                         attachment_filename=filename,
                         as_attachment=True)
    return render_template('submit.html', form=form)


app.config.update(dict(
    SECRET_KEY="powerful secretkey",
    WTF_CSRF_SECRET_KEY="a csrf secret key"
))


UPLOAD_FOLDER = ''
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename + 'uploaded')
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return 'file uploaded'

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''
