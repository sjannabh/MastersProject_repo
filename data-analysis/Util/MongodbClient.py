import pyodbc # pip install pyodbc
from pymongo import MongoClient
from bson import json_util
import json


class MongodbClient():
            
    def parse_json(data):
        return json.loads(json_util.dumps(data, indent=4))

    def db_mongo_insert_all_document(Connection_String, dbName, dbCollection, data):
        
        #Connecting to mongodb compass
        client = MongoClient(Connection_String)   
        
        #Accessing the database
        db = client[dbName]
        
        #Accessing the collection within the database
        collection = db[dbCollection]
       
        # for inserting more than one record at a time
        res = collection.insert_many(data) 

        return res.acknowledged
    
    def db_mongo_insert_one_documents(Connection_String, dbName, dbCollection, data):

        #Connecting to mongodb compass
        client = MongoClient(Connection_String)   

        #Accessing the database
        db = client[dbName]
        
        #Accessing the collection within the database
        collection = db[dbCollection]
            
        #inserting one document into collection
        res = collection.insert_one(data) 
        
        return res.acknowledged
        
    def db_mongo_find_a_document(Connection_String, dbName, dbCollection, query):

        #Connecting to mongodb compass
        client = MongoClient(Connection_String)   

        #Accessing the database
        db = client[dbName]

        #Accessing the collection within the database
        collection = db[dbCollection]
        
        # finding a particular document
        x = collection.find(query) 
        res = []
        
        for data in x:
            res.append(data)

        return MongodbClient.parse_json(res)
    
    def db_mongo_update_one_field_in_document(Connection_String, dbName, dbCollection, query, newData):

        #Connecting to mongodb compass
        client = MongoClient(Connection_String)   
        
        #Accessing the database
        db = client[dbName]
        
        #Accessing the collection within the database
        collection = db[dbCollection]

        # taking the reference of the document and setting the price value as 15.00
        res = collection.update_one( query, newData)
        
        return res.acknowledged
    
    def db_mango_update_sub_sub_field(Connection_String, dbName, dbCollection, query, newData):

        #Connecting to mongodb compass
        client = MongoClient(Connection_String)   

        #Accessing the database
        db = client[dbName]

        #Accessing the collection within the database
        collection = db[dbCollection]
               
        res = collection.update_one(query,newData)
        
        return res.acknowledged
    
    def db_mango_delete_sub_category_field(Connection_String, dbName, dbCollection, query, newData):

        #Connecting to mongodb compass
        client = MongoClient(Connection_String)   

        #Accessing the database
        db = client[dbName]

        #Accessing the collection within the database
        collection = db[dbCollection]
        
        # pull will remove specific value
        res = collection.delete_one(query,newData)
        
        return res.acknowledged
    
    def db_mongo_update_many_documents(Connection_String, dbName, dbCollection, query, newData):

        #Connecting to mongodb compass
        client = MongoClient(Connection_String)   

        #Accessing the database
        db = client[dbName]

        #Accessing the collection within the database
        collection = db[dbCollection]
        
        #taking the price as reference changing the rating values for the documents where price is 15        
        # pull will remove specific value
        res = collection.update_many(query,newData)
        
        return res.acknowledged
    
    def db_mongo_delete_all_documents(Connection_String, dbName, dbCollection, query):

        #Connecting to mongodb compass
        client = MongoClient(Connection_String)   

        #Accessing the database
        db = client[dbName]

        #Accessing the collection within the database
        collection = db[dbCollection]
        
        # to delete existing documents
        res = collection.delete_many(query)
        
        return res.acknowledged
        