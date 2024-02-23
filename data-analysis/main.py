from flask import Flask, request, jsonify # pip install flask
from flask_httpauth import HTTPBasicAuth # pip install flask_httpauth
from dotenv import dotenv_values # pip install python-dotenv
import logging
from bson import json_util # pip install pymongo
from Service.DataRepository import DataRepository
from Service.RecommenderRepository import RecommenderRepository
from flask_cors import CORS # pip install -U flask-cors

config = dotenv_values(".env")

server = Flask(__name__)
CORS(server)
auth = HTTPBasicAuth() # for authentication
logging.basicConfig(filename='app.log',level=logging.INFO)

data = [];    

# ----------------------------[  Server  ]----------------------------
#Server Health
@server.route("/")
def home():
    return "Server is up and running", 200
# --------------------------------------------------------------------------


# ----------------------------[  Data Loading  ]----------------------------
# load products dataset from DataRepository.py
@server.route("/api/v1/loadProductsData")
def loadProductsData():
    
    return jsonify(DataRepository.load_products_data()),200

# load users dataset from DataRepository.py
@server.route("/api/v1/loadUsersData")
def loadUsersData():
    
    return jsonify(DataRepository.load_users_data()),200

# load reviews dataset from DataRepository.py
@server.route("/api/v1/loadReviewsData")
def loadReviewsData():
    
    return jsonify(DataRepository.load_reviews_data()),200
# --------------------------------------------------------------------------


# ----------------------------[  Recommended Data  ]----------------------------
# load products dataset from DataRepository.py
@server.route("/api/v1/getPopularRecommendedData")
# @cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def getPopularRecommendedData():

    productId = request.args.get('productId') 
    response = jsonify(RecommenderRepository.load_popular_products(productId))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response,200

@server.route("/api/v1/getPopularRecommendedProducts")
# @cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def getPopularRecommendedProducts():

    response = jsonify(RecommenderRepository.loadPopularRecommandedProducts())
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response,200

# load users dataset from DataRepository.py
@server.route("/api/v1/getUserRecommendedDatabySearchText")
def getUserRecommendedData():
    
    productText = request.args.get('productText') 
    return jsonify(RecommenderRepository.load_user_recommend_products_using_searchText(productText)),200
# --------------------------------------------------------------------------


if __name__ == "__main__":
    print("Server Started on: " + config["hostServer"] + ", Port: " + config["portNumber"])
    server.run(port=config["portNumber"], debug=True)

