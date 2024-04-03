from flask import Flask, request, jsonify, render_template # pip install flask
from flask_httpauth import HTTPBasicAuth # pip install flask_httpauth
from dotenv import dotenv_values # pip install python-dotenv
import logging
from bson import json_util # pip install pymongo
from Service.DataRepository import DataRepository
from Service.RecommenderRepository import RecommenderRepository
from flask_cors import CORS # pip install -U flask-cors

server = Flask(__name__)
CORS(server)
auth = HTTPBasicAuth() # for authentication
logging.basicConfig(filename='app.log',level=logging.INFO)
config = dotenv_values(".env")

# ----------------------------[  Web Application  ]----------------------------
#Home Page
@server.route("/home",methods=['GET'])
def homepage():
    # routeList = getDefinedRoutesList()
    # otherList =[] 
    # dataLoadingList =[]
    # dataRecommendationList =[]
    # for x in routeList:
    #     if "DataLoading" in x:
    #         dataLoadingList.append(x)
    #     elif "DataRecommendation" in x:
    #         dataRecommendationList.append(x)
    #     elif "/" in x:
    #         otherList.append(x)
    
    # return render_template("index.html", otherList=otherList,dataLoadingList=dataLoadingList,dataRecommendationList=dataRecommendationList)
    return render_template("index.html")

# ----------------------------[  Server Health  ]----------------------------
#Server Health
@server.route("/status",methods=['GET'])
def home():
    return "Server is up and running", 200

# Test DB Connection
@server.route("/health",methods=['GET'])
def testDbConnection():

    response = jsonify(RecommenderRepository.test_db_connection())
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response,200
# --------------------------------------------------------------------------


# ----------------------------[  Clean Data  ]----------------------------
# This will be executed only once
@server.route("/api/v1/cleanDataset",methods=['GET'])
def cleanDataset():

    return jsonify(DataRepository.clean_dataset()),200
# --------------------------------------------------------------------------


# ----------------------------[  Data Loading  ]----------------------------
# load products dataset from DataRepository.py
@server.route("/api/v1/DataLoading/loadProductsData",methods=['GET'])
def loadProductsData():
    
    return jsonify(DataRepository.load_products_data()),200

# load users dataset from DataRepository.py
@server.route("/api/v1/DataLoading/loadUsersData",methods=['GET'])
def loadUsersData():
    
    return jsonify(DataRepository.load_users_data()),200

# load reviews dataset from DataRepository.py
@server.route("/api/v1/DataLoading/loadReviewsData",methods=['GET'])
def loadReviewsData():
    
    return jsonify(DataRepository.load_reviews_data()),200

# Content Based Filtering By Cosine Similarities
@server.route("/api/v1/DataLoading/loadContentBasedFilteringByCountVectorizer",methods=['GET'])
# @cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def loadContentBasedFilteringByCosineSimilarities():

    response = jsonify(RecommenderRepository.loadData_content_based_filtering_by_cosine_similarities())
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response,200

# Variational Autoencoder
@server.route("/api/v1/DataLoading/loadVariationalAutoencoder",methods=['GET'])
# @cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def loadVariationalAutoencoder():

    response = jsonify(RecommenderRepository.loadData_variational_autoencoder())
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response,200

# --------------------------------------------------------------------------

# ----------------------------[  Data Recommendation  ]----------------------------
# Content Based Filtering By Cosine Similarities
@server.route("/api/v1/DataRecommendation/contentBasedFilteringByCountVectorizer",methods=['GET'])
# @cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def content_based_filtering_by_cosine_similarities():

    response = jsonify(RecommenderRepository.content_based_filtering_by_cosine_similarities())
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response,200

# Correlation Matrix On Product Rating
@server.route("/api/v1/DataRecommendation/correlationMatrixOnProductRating",methods=['GET'])
# @cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def correlation_matrix_on_product_rating():

    response = jsonify(RecommenderRepository.correlation_matrix_on_product_rating())
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response,200

# Autoencoder based Collaborative Filter Model
@server.route("/api/v1/DataRecommendation/autoencoderBasedCollaborativeFilterModel",methods=['GET'])
# @cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def autoencoder_based_collaborative_filter_model():

    response = jsonify(RecommenderRepository.autoencoder_based_collaborative_filter_model())
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response,200

# Variational Autoencoder
@server.route("/api/v1/DataRecommendation/Autoencoder",methods=['GET'])
# @cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def autoencoder():

    response = jsonify(RecommenderRepository.autoencoder())
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response,200

#------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------

# load products dataset from DataRepository.py
@server.route("/api/v1/getPopularRecommendedData",methods=['GET'])
# @cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def getPopularRecommendedData():

    productId = request.args.get('productId') 
    response = jsonify(RecommenderRepository.load_popular_products(productId))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response,200

@server.route("/api/v1/getPopularRecommendedProducts",methods=['GET'])
# @cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def getPopularRecommendedProducts():

    response = jsonify(RecommenderRepository.loadPopularRecommandedProducts())
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response,200

# load users dataset from DataRepository.py
@server.route("/api/v1/getUserRecommendedDatabySearchText",methods=['GET'])
def getUserRecommendedData():
    
    productText = request.args.get('productText') 
    return jsonify(RecommenderRepository.load_user_recommend_products_using_searchText(productText)),200
# --------------------------------------------------------------------------

def getDefinedRoutesList():
    routes = []
    for route in server.url_map.iter_rules():
       routes.append('%s' % route)
    
    return routes

if __name__ == "__main__":
    print("Server Started on: " + config["hostServer"] + ", Port: " + config["portNumber"])
    server.run(port=config["portNumber"], debug=True)

