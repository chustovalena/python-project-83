import os
from flask import Flask, render_template, request
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.debug = True


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/urls')
def urls():
    url = request.form.get('url')
    return f'Получен URL: {url}'

