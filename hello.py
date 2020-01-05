from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    print(1+12)
    return '<h1>Hello, Darling!!!</h1>'