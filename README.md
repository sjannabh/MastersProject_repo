# MastersProject
Final Semester Project of Masters


# oldReadMongo.py

import pyodbc
import pymongo # pip install pymongo

# https://github.com/alimisumanth/miscellaneous/blob/main/mongodb-crud%20operations.py

class ReadMongo(object):
    def __init__(self):
        self.conn_params = ''

    def db_mongo_insert_update_delete(self,query, params=()):
        conn = None
        db = None
        try:
            conn = pyodbc.connect(self.conn_params)
        except pyodbc.Error as e:
            print(str(e))
        else:
            db = conn.cursor()
            db.execute(query, params).commit()
            row_count = db.rowcount # rows affected
        finally:
            if conn:
                conn.close()
        return row_count

    def db_mongo_select(self,query, params=()):
        conn = None
        db = None
        try:
            conn = pyodbc.connect(self.conn_params)
        except pyodbc.Error as e:
            print(str(e))
        else:
            db = conn.cursor()
            db.execute(query, params)
            rows = db.fetchall()
        finally:
            if conn:
                conn.close()
        return rows
    

#Connecting to mondodb compass
connection_url="mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.0.2" #MongoDB compass local host URL. You can replace the SRV string if you are connecting with mongodb atlas  
client=pymongo.MongoClient(connection_url)
client.list_database_names()#listing the available databases 

database_name="student_database"
student_db=client[database_name]#creating a database named student_database
collection_name="computer science"
collection=student_db[collection_name]#creating a collection in student_database
#inserting documents 

document={"Name":"Raj",
"Roll No":  153,
"Branch": "CSE"}
collection.insert_one(document)#insetring single document 


documents=[{"Name":"Roshan","Roll No":159,"Branch":"CSE"},{"Name":"Rahim","Roll No":155,"Branch":"CSE"},{"Name":"Ronak","Roll No":156,"Branch":"CSE"}]
collection.insert_many(documents)#inserting multiple documents

#Retrieving data from collection
query={"Name":"Raj"}
print(collection.find_one(query))#Retrieving single document


query={"Branch":"CSE"}
result=collection.find(query)#Retrieving multiple documents
for i in result:
    print(i)


result=collection.find({}).limit(2)#limiting the results
for i in result:
    print(i)


query={"Roll No":{"$eq":153}}
print(collection.find_one(query))# using filter to retrive document

#Updating documents in collection

query={"Roll No":{"$eq":153}}
present_data=collection.find_one(query)
new_data={'$set':{"Name":'Ramesh'}}
collection.update_one(present_data,new_data)#updating single document


present_data={"Branch":"CSE"}
new_data={"$set":{"Branch":"ECE"}}
collection.update_many(present_data,new_data)#updating multiple documents

#deleting documents from collection
query={"Roll No":153}
collection.delete_one(query)#deleting single document


query={"Branch":"ECE"}
collection.delete_many(query)#deleting multiple documents


#dropping collection

collection.drop()


------------------------------------------------------------------------------------








client =MongoClient('localhost',27017)
#JRAfncgQCTXQ4NDQ
#client = MongoClient('mongodb+srv://qwerty:JRAfncgQCTXQ4NDQ@myecomcluster.attg9.mongodb.net/MyEcomCluster', connect=False)
db = client.MyDb
collection = db.UsersData



inserted = collection.insert_many(products_json_dataset)


print(str(len(inserte.inserted_ids)) + " documents inserted")

def get_database():
 
   # Provide the mongodb atlas url to connect python to mongodb using pymongo
   CONNECTION_STRING = "mongodb+srv://qwerty:JRAfncgQCTXQ4NDQ@myecomcluster.attg9.mongodb.net/MyEcomCluster"
 
   # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
   client = MongoClient(CONNECTION_STRING)
 
   # Create the database for our example (we will use the same database throughout the tutorial
   return client['products_list']

   # Get the database



collection.delete_many({})
mongodb+srv://qwerty:JRAfncgQCTXQ4NDQ@myecomcluster.attg9.mongodb.net/MyEcomCluster

--------------------------------------------
--------------------------------------------

# List of Book Suggestions
@server.route("/api/v1/getBookSuggestions")
def getBookSuggestions():
    
    return jsonify(BooksRepository.get_book_suggestions()),200

@server.route("/api/v1/getSuggestions/<suggestionType>")
def getSuggestionsq(suggestionType):
    data = {
        "name":"qwerty",
        "address":"123 qwerty",
        "QueryParameter":suggestionType
    }
    
    extra = request.args.get("type")
    if extra:
            data["type"] = extra;
    
    return jsonify(data),200


@server.route("/books", methods=["GET","POST"])
def books():
    if request.method=="GET":
        if len(data) > 0:
            return jsonify(data), 200
        else:
            "Error", 404
    
    if request.method=="POST":
 
        new_author = request. form['author'] 
        new_lang = request. form[' language'] 
        new_title = request. form['title'] 
        iD = data[-1]["id"]+1 

        new_obj ={
            'id': iD,
            'author' : new_author, 
            'language': new_lang, 
            'title': new_title 
            }
        
        data. serverend( new_obj ) 
        return jsonify(data), 201     

# https://github.com/mongodb-developer/pymongo-fastapi-crud/tree/main            
# @app.on_event("startup")
# def startup_db_client():
#     app.mongodb_client = MongoClient(config["ATLAS_URI"])
#     app.database = app.mongodb_client[config["DB_NAME"]]

# @app.on_event("shutdown")
# def shutdown_db_client():
#     app.mongodb_client.close()


# Mongo Code --------------------------------

# ProductsData

@server.route("/api/v1/getOneDocumentFromMongoDb")
def getOneDocumentFromMongodb():
    
    Sample_data ={
                "category": [
                "Computers&Accessories",
                "Accessories&Peripherals",
                "Cables&Accessories",
                "Cables",
                "USBCables"
                ],
                "img_link": "https://m.media-amazon.com/images/I/41V5FtEWPkL._SX300_SY300_QL70_FMwebp_.jpg",
                "no_of_ratings": "94,363",
                "price": 8.74,
                "product_description": "The boAt Deuce USB 300 2 in 1 cable is compatible with smartphones, tablets, PC peripherals, Bluetooth speakers, power banks and all other devices with Type-C as well as Micro USB port|It ensures 3A fast charging and data transmissions with rapid sync at 480 mbps|The premium Nylon braided skin makes it sturdy and invincible against external damage|Its Aluminium alloy shell housing makes it last longer with 10000+ Bends Lifespan with extended frame protection for strain relief|The resilient and flexible design offers a tangle free experience seamlessly|Deuce USB 300 cable offers a perfect 1.5 meters in length for smooth & hassle-free user experience|2 years warranty from the date of purchase",
                "product_id": "B08HDJ86NZ",
                "product_link": "https://www.amazon.in/Deuce-300-Resistant-Tangle-Free-Transmission/dp/B08HDJ86NZ/ref=sr_1_4?qid=1672909124&s=electronics&sr=1-4",
                "product_name": "boAt Deuce USB 300 2 in 1 Type-C & Micro USB Stress Resistant, Tangle-Free, Sturdy Cable with 3A Fast Charging & 480mbps Data Transmission, 10000+ Bends Lifespan and Extended 1.5m Length(Martian Red)",
                "rating": "4.2"
            }
            
    res = MongodbClient.db_mongo_insert_one_documents(config["connection_string_mongo"],'MyDb','NewProductData', Sample_data)
    
    return jsonify(res), 200

@server.route("/api/v1/findOneDocumentFromMongoDb")
def findOneDocumentFromMongodb():
    
    qurey = {"product_id":"B07JW9H4J1"}
    res = MongodbClient.db_mongo_find_a_document(config["connection_string_mongo"],'MyDb','NewProductData', qurey)

    return res, 200

@server.route("/api/v1/updateOneDocumentInMongoDb")
def updateOneDataFromMongodb():
    
    query = {"product_id":"B098NS6PVG"}
    newData = {"$set": { 'price': 150.00 }}

    res = MongodbClient.db_mongo_update_one_field_in_document(config["connection_string_mongo"],'MyDb','NewProductData', query, newData)
    
    return jsonify(res), 200

@server.route("/api/v1/updateManyDocumentsInMongoDb")
def updateManyDocumentsFromMongodb():
    
    query = {'price':15.00}
    newData = {"$set":{
                "rating":"4.5"
            }}
    
    res = MongodbClient.db_mongo_update_many_documents(config["connection_string_mongo"],'MyDb','NewProductData', query, newData)
    
    return jsonify(res), 200


@server.route("/api/v1/addNewSubCategoryValueToInMongoDb")
def add_new_sub_category_to_Mongodb():
    query = {"product_id": "B07JW9H4J1"}
    newData = {"$push":{"category":"Electronics"}}

    res = MongodbClient.db_mango_update_sub_sub_field(config["connection_string_mongo"],'MyDb','NewProductData', query, newData)
    
    return jsonify(res), 200

@server.route("/api/v1/deleteNewSubCategoryValueToInMongoDb")
def delete_new_sub_category_to_Mongodb():

    query = {"product_id": "B07JW9H4J1"}
    newData= {"$pop":{"category":"Electronics"}}

    res = MongodbClient.db_mango_delete_sub_category_field(config["connection_string_mongo"],'MyDb','NewProductData', query, newData)
    
    return jsonify(res), 200



@server.route("/api/v1/dataDeletedInMongoDb")
def deleteAllDocumentsFromOneCollection():
    
    query = {}
    res = MongodbClient.db_mongo_delete_all_documents(config["connection_string_mongo"],'MyDb','NewProductData', query)
    
    return jsonify(res), 200



# Users Data





#-----------------------------------------------------------------------



# -------------------------------------------------------------------------------------------------------------------------


