from flask import Flask, render_template
from pymongo import MongoClient

app = Flask(__name__, template_folder='template', static_folder='stylesheet',static_url_path='/stylesheet')


@app.route('/')
def index():
    return render_template('test.html')

if __name__ == '__main__':
    app.run(debug=True)