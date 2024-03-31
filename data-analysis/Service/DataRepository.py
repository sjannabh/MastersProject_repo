import pandas as pd
import numpy as np
import sklearn
from Service.IRepository.IdataRepository import IdataRepository
from os import sep
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
import json
from dotenv import dotenv_values # pip install python-dotenv
from Util.MongodbClient import MongodbClient
from flask import jsonify
from functools import reduce
from random import random 
import requests

config = dotenv_values(".env")

class DataRepository(IdataRepository):
    
    def load_data():
        # Column Names (['product_id', 'product_name', 'category', 'discounted_price', 'actual_price', 'discount_percentage', 'rating', 'rating_count', 'about_product', 'user_id', 'user_name', 'review_id', 'review_title', 'review_content', 'img_link', 'product_link'],  dtype='object')
        fullDataset = pd.read_csv("./Data/amazon_cleaned_data.csv", delimiter=",")

        return fullDataset

    def verifyArr(arr, maxRating):
        arr.sort(reverse = True)
        length = len(arr)-1
        for idx, x in enumerate(arr):
            if(arr[idx] > maxRating):
                arr[length-idx] = arr[length-idx] + (arr[idx] - maxRating)
                arr[idx] = maxRating
            arr[idx] = round(arr[idx],1)
        return arr

    def divide_rating_into_multiple_ratings(number, parts, minRating, maxRating):
        randombit = number - minRating * parts;
        out = [];
        for index in range(parts):
            out.append(random());
        mult = randombit / reduce((lambda x, y: x + y), out)
        temp = list(map((lambda x: x * mult + minRating), out));
        temp = DataRepository.verifyArr(temp,maxRating)
        temp = DataRepository.verifyArr(temp,maxRating)
        return temp;
    
    # Function for validating HTTP status code.
    def validate_url(url):
        r = requests.head(url)
        return r.status_code == 200
    
    def clean_dataset():
        fullDataset = pd.read_csv('C:\\Repos\\MastersProject\\data-analysis\\Data\\amazon.csv', delimiter=",")
                        
        fullDataset.rename(columns={
            "actual_price": 'price',
            "about_product":'product_description',
            "rating_count":'no_of_ratings'
        },inplace=True)

        fullDataset['no_of_ratings'] = fullDataset['no_of_ratings'].str.replace('[,]','', regex=True).astype(int)        
        fullDataset['rating'] = (fullDataset['rating'].astype(float)).round(1)
        fullDataset['price'] = (fullDataset['price'].str.replace('[\₹\,]','', regex=True).astype(float) / 80).round(2)
        fullDataset["category"] = fullDataset["category"].str.split("|") 
        fullDataset.fillna(0)
        
        fullDataset_new_dict = []
        for i, x in fullDataset.to_dict('index').items():
            if DataRepository.validate_url(x['img_link']) == True:
                fullDataset_new_dict.append(x)
        
        fullDataset_new_df = pd.DataFrame(fullDataset_new_dict);
        fullDataset_new_df.drop_duplicates(subset=['product_id'], inplace=True)
        fullDataset_new_df.drop_duplicates(subset=['product_name'], inplace=True)
        
        fullDataset_new_df.to_csv('C:\\Repos\\MastersProject\\data-analysis\\Data\\amazon_cleaned_data.csv', index=False)
                
        return True
    
    def clean_products_data():
        fullDataset = DataRepository.load_data()
        
        # ignore the columns that are not needed
        products_dataset = fullDataset [
            [
                "product_id",
                "product_name",
                "category",
                "price",
                "img_link",
                "product_link",
                "product_description",
                "rating",
                "no_of_ratings"   
            ]
        ]
        
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
        
        userId_df = pd.DataFrame(columns = ['user_id'])

        for index, row in users_id_dataset.iterrows():
            for itemData in row["user_id"]:
                userId_df.loc[len(userId_df)]=[itemData]
                
        first_names=fullUserData["fname"].tolist()
        last_names=fullUserData["lname"].tolist()
        phoneNo=fullUserData["phoneNo"].tolist()

        userId_df["fname"] = np.random.choice(first_names, size=len(userId_df))
        userId_df["lname"] = np.random.choice(last_names, size=len(userId_df))
        userId_df["phoneNo"] = np.random.choice(phoneNo, size=len(userId_df))
        userId_df["email"] = userId_df["fname"] + '.' + userId_df["lname"] + '@ecommerce.com'
        userId_df["password"] = userId_df["fname"] + '@1234'
        
        userId_df.drop_duplicates(subset=['user_id'], inplace=True)
        userId_df.drop_duplicates(subset=['fname','lname'], inplace=True)
        
        users_json_dataset = userId_df.to_dict(orient='records')
        #will convert a subset of Python objects into a json string
        #json.dumps(users_json_dataset, indent=4)
        
        return users_json_dataset
    
    def clean_reviews_data():
        fullDataset = DataRepository.load_data()
        
        review_dataset = fullDataset[
            [
                "review_id",
                "review_title",
                "review_content",
                "user_id",
                "product_id",
                'rating'
            ]
       ]
                        
        review_dataset["product_id"] = fullDataset["product_id"]
        review_dataset["user_id"] = fullDataset["user_id"].str.split(",")
        review_dataset["review_id"] = fullDataset["review_id"].str.split(",")
        review_dataset["review_title"] = fullDataset["review_title"].str.split(",")
        review_dataset["review_content"] = fullDataset["review_content"].str.split(",")
        review_dataset["rating"] = fullDataset["rating"]

        review_dataset.drop_duplicates(subset=['product_id'], inplace=True)
        
        review_final_df = pd.DataFrame(columns = ['product_id','user_id','review_id','review_title','review_content','rating'])

        for index, row in review_dataset.iterrows():
            limit = len(row['user_id'])
            pid = row['product_id']
            #print(limit)
            ratingList = DataRepository.divide_rating_into_multiple_ratings(row['rating']*limit,limit,1,5)
            for index in range(limit):
                review_final_df.loc[len(review_final_df)]=[pid,row['user_id'][index],row['review_id'][index],row['review_title'][index],row['review_content'][index],ratingList[index]]
            
        review_final_df.drop_duplicates(subset=['review_id'], inplace=True)

        # NOTE: To Be Integrated in Recommendations
        #review_final_df.to_csv('required_dataset.csv', index=False)
                
        temp_review_json_dataset = review_final_df.to_dict(orient='records')        
        
        return temp_review_json_dataset
    
    def load_products_data():
        products_dataset = DataRepository.clean_products_data()   
       
        #products_json_dataset = products_dataset.to_dict(orient='records')
        
        # go to MongoClient.py       
        res = MongodbClient.db_mongo_insert_all_document(config["connection_string_mongo"],'test','products', products_dataset)
        
        if res == True:
           print("Product Data Loading Done")
           return (res), 201
        else:
           return (res), 400
        
    def load_users_data():
                
        users_dataset = DataRepository.clean_users_data()
      
        #users_data = users_dataset.to_dict(orient='records')
        res = MongodbClient.db_mongo_insert_all_document(config["connection_string_mongo"],'test','users', users_dataset)
        if res == True:
           print("User Data Loading Done")
           return (res), 201
        else:
            return (res), 400
   
    def load_reviews_data():
        temp_review_df = DataRepository.clean_reviews_data()
        
        #reviews_json_dataset = temp_review_df.to_dict(orient='records')
        res = MongodbClient.db_mongo_insert_all_document(config["connection_string_mongo"],'test','reviews', temp_review_df)
    
        if res == True:
            print("Review Data Loading Done")
            return res, 201
        else:
          return (res), 400
    