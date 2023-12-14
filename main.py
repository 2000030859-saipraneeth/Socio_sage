from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import re
import time
from pymongo import MongoClient
from fb_scrap import fbscrap
from twitter_scrap import twitterscrap
from linkedin_scrap import linkedinscrap
from urllib.parse import quote
from flask import Flask, render_template, request, jsonify

app = Flask(__name__, template_folder='template', static_folder='stylesheet',static_url_path='/stylesheet')
client = MongoClient('mongodb://localhost:27017/')
db = client['Socio_sage']
collection = db['Posts']

options = Options()
options.add_experimental_option("detach", True)
options.add_argument("--disable-infobars")
options.add_argument("--headless")
options.add_argument("start-maximized")
options.add_argument("--disable-extensions")

options.add_experimental_option(
    "prefs", {"profile.default_content_setting_values.notifications": 1}
)

# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)




def fetch_results(keyword):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    linkedinscrap(driver,collection,keyword)
    print("linkedin data scrapped")

    twitterscrap(driver,collection,keyword)
    print("twitter data scrapped")

    fbscrap(driver,collection,keyword)
    print("fb data scrapped")


@app.route('/')
def index():
    return render_template('test.html')

@app.route('/api/fetch_results', methods=['GET'])
def api_fetch_results():
    keyword = request.args.get('keyword')
    keyword = quote(keyword)

    # Clear existing data in the collection
    collection.delete_many({})

    print(f"Starting search of {keyword}")

    # Call the fetch_results function with the keyword
    fetch_results(keyword)
    result_data = list(collection.find())
    for record in result_data:
        record['_id'] = str(record['_id'])

    return jsonify(result_data)

#


@app.route('/api/get_data_from_db', methods=['GET'])
def api_get_data_from_db():
    # Retrieve data from the database
    result_data = list(collection.find())
    for record in result_data:
        record['_id'] = str(record['_id'])
    return jsonify(result_data)

# if __name__ == '__main__':
#     collection.delete_many({})
#     keyword = str(input("Enter keyword: "))
#     keyword=quote(keyword)
#     print(f"Starting search of {keyword}")
#     fetch_results(keyword)

if __name__ == '__main__':
    # collection.delete_many({})
    app.run(debug=True)