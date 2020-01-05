from flask import Flask, request, jsonify, abort, redirect, url_for
import numpy as np
import pickle


app = Flask(__name__)
knn = pickle.load(open('model.pkl', "rb"))

@app.route('/')
def hello_world():
    print(1+12)
    return '<h1>Hello, Darling!!!</h1>'

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    username = float(username)*float(username)
    return f'User {username}'

def mean(numbers):
    return float(sum(numbers))/max(len(numbers),1)
    
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
    params = np.array(params).reshape(1,-1)
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
        params = np.array(params).reshape(1,-1)
        predict = knn.predict(params)

        predict = {'class': int(predict[0])}
    except:
        return redirect(url_for('bad_request'))

    return jsonify(predict)

@app.route('/badrequest400')
def bad_request():
    abort(400)