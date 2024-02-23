from Service.IRepository.IdataRepository import IdataRepository
from os import sep
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
import json
from dotenv import dotenv_values # pip install python-dotenv
from Util.MongodbClient import MongodbClient
import numpy as np
import sklearn

from flask import jsonify

config = dotenv_values(".env")

class DataRepository(IdataRepository):
    
    def load_data():
        # Column Names (['product_id', 'product_name', 'category', 'discounted_price', 'actual_price', 'discount_percentage', 'rating', 'rating_count', 'about_product', 'user_id', 'user_name', 'review_id', 'review_title', 'review_content', 'img_link', 'product_link'],  dtype='object')
        fullDataset = pd.read_csv("./Data/amazon.csv", delimiter=",")

        return fullDataset
    
    def clean_products_data():
        fullDataset = DataRepository.load_data()
        
        # ignore the columns that are not needed
        products_dataset = fullDataset [
            [
                "product_id",
                "product_name",
                "category",
                "actual_price",
                "img_link",
                "product_link",
                "about_product",
                "rating",
                "rating_count"   
            ]
        ]
                
        products_dataset.rename(columns={
            "actual_price": 'price',
            "about_product":'product_description',
            "rating_count":'no_of_ratings'
        },inplace=True)

        #df['Salary'].str.replace(',', '').str.replace('₹', '').astype(int)
        products_dataset['no_of_ratings'] = products_dataset['no_of_ratings'].str.replace('[,]','', regex=True).astype(int)        
        products_dataset['rating'] = (products_dataset['rating'].astype(float)).round(1)
        products_dataset['price'] = (products_dataset['price'].str.replace('[\₹\,]','', regex=True).astype(float) / 80).round(2)
        products_dataset["category"] = products_dataset["category"].str.split("|") 
        
        products_dataset.drop_duplicates(subset=['product_id'], inplace=True)
        
        products_json_dataset = products_dataset.to_dict(orient='records')
        
        return products_json_dataset
        
    def clean_users_data():
        fullUserData = pd.read_csv("./Data/userInfo.csv", delimiter=",")
        
        fullDataset = DataRepository.load_data()
        
        users_id_dataset = fullDataset[
            [
                "user_id"
            ]
        ]
        users_id_dataset["user_id"] = users_id_dataset["user_id"].str.split(",")
        users_json_dataset = users_id_dataset.to_dict(orient='records')
        json.dumps(users_json_dataset, indent=4)
        
        userId_df = pd.DataFrame(columns = ['user_id'])

        for index, row in users_id_dataset.iterrows():
            for itemData in row["user_id"]:
                userId_df.loc[len(userId_df)]=[itemData]
                
        userId_df
        
        first_names=fullUserData["fname"].tolist()
        last_names=fullUserData["lname"].tolist()
        phoneNo=fullUserData["phoneNo"].tolist()


        userId_df["fname"] = np.random.choice(first_names, size=len(userId_df))
        userId_df["lname"] = np.random.choice(last_names, size=len(userId_df))
        userId_df["phoneNo"] = np.random.choice(phoneNo, size=len(userId_df))
        userId_df["email"] = userId_df["fname"] + '.' + userId_df["lname"] + '@ecommerce.com'
        userId_df["password"] = userId_df["fname"] + '@1234'
        
        userId_df.drop_duplicates(subset=['user_id'], inplace=True)
        
        users_json_dataset = userId_df.to_dict(orient='records')
        
        return users_json_dataset
    
    def clean_reviews_data():
        fullDataset = DataRepository.load_data()
        
        review_dataset = fullDataset[
            [
                "review_id",
                "review_title",
                "review_content",
                "user_id",
                "product_id"
            ]
       ]
                        
        review_dataset["product_id"] = fullDataset["product_id"]
        review_dataset["user_id"] = fullDataset["user_id"].str.split(",")
        review_dataset["review_id"] = fullDataset["review_id"].str.split(",")
        review_dataset["review_title"] = fullDataset["review_title"].str.split(",")
        review_dataset["review_content"] = fullDataset["review_content"].str.split(",")

        review_dataset.drop_duplicates(subset=['product_id'], inplace=True)
        
        temp_review_df = pd.DataFrame(columns = ['product_id','user_id','review_id','review_title','review_content'])
        for index, row in review_dataset.iterrows():
            limit = len(row['user_id'])
            pid = row['product_id']
            #print(limit)
            for index in range(limit):
                temp_review_df.loc[len(temp_review_df)]=[pid,row['user_id'][index],row['review_id'][index],row['review_title'][index],row['review_content'][index]]
         
        temp_review_df.drop_duplicates(subset=['review_id'], inplace=True)
                
        temp_review_json_dataset = temp_review_df.to_dict(orient='records')        
                
        return temp_review_json_dataset
    
    def load_products_data():
        products_dataset = DataRepository.clean_products_data()   
       
        #products_json_dataset = products_dataset.to_dict(orient='records')
        
        # go to MongoClient.py       
        res = MongodbClient.db_mongo_insert_all_document(config["connection_string_mongo"],'MyDb','ProductData', products_dataset)
        
        if res == True:
           return (res), 201
        else:
           return (res), 400
        
    def load_users_data():
                
        users_dataset = DataRepository.clean_users_data()
      
        #users_data = users_dataset.to_dict(orient='records')
        res = MongodbClient.db_mongo_insert_all_document(config["connection_string_mongo"],'MyDb','UserData', users_dataset)
                                                                                                                                                                                                                                                                                                                        
        if res == True:
            return (res), 201
        else:
            return (res), 400
   
    def load_reviews_data():
        temp_review_df = DataRepository.clean_reviews_data()
        
        #reviews_json_dataset = temp_review_df.to_dict(orient='records')

        res = MongodbClient.db_mongo_insert_all_document(config["connection_string_mongo"],'MyDb','ReviewData', temp_review_df)
    
        if res == True:
            return res, 201
        else:
          return (res), 400
    