import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import seaborn as sns
import warnings
from sklearn.decomposition import TruncatedSVD
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
from tensorflow.keras.layers import Input, Dense
from tensorflow.keras.models import Model
from keras.optimizers import Adam
from keras.layers import Input, Dense, Dropout
from keras.models import Model
import pyodbc # pip install pyodbc
from pymongo import MongoClient
from bson import json_util
import json
from dotenv import dotenv_values # pip install python-dotenv
from Service.IRepository.IrecommenderRepository import IrecommenderRepository
from Service.DataRepository import DataRepository
from Util.MongodbClient import MongodbClient

config = dotenv_values(".env")


class RecommenderRepository(IrecommenderRepository):
    
    def test_db_connection():
        res = MongodbClient.db_mongo_find_documents(config["connection_string_mongo"],'test','products', {"product_id":"B081FJWN52"})
        
        if res:
           return ("Able to connect with Mongo DB"), 201
        else:
           return ("Unable to connect with Mongo DB"), 400       
    
    def content_based_filtering_by_cosine_similarities():
        
        # Get all documents
        query = {}
        res = MongodbClient.db_mongo_find_documents(config["connection_string_mongo"],'test','products', query)
        products_dataset = pd.DataFrame(res)
        
        products_dataset['product_name'] =products_dataset['product_name'].str.lower() 
        products_dataset['product_description'] =products_dataset['product_description'].str.lower() 

        new_subset_products_dataset = products_dataset.drop(['category','price','img_link','product_link','rating','no_of_ratings'], axis=1)
        new_subset_products_dataset['data'] = new_subset_products_dataset[new_subset_products_dataset.columns[1:]].apply(lambda x: ' '.join(x.dropna().astype(str)),axis=1)

        new_subset_products_dataset['data']['product_name'] =products_dataset['product_name'].str.lower() 
       
        vectorizer = CountVectorizer()
        vectorized = vectorizer.fit_transform(new_subset_products_dataset['data'])
        similarities = cosine_similarity(vectorized)

        products_dataset_new = pd.DataFrame(similarities, columns=products_dataset['product_name'], index=products_dataset['product_name']).reset_index()
                
        recommendationsSetList = []
        for index,row in products_dataset.iterrows():
            product_id = row["product_id"]
            productName = row["product_name"].lower()
            recommendations = pd.DataFrame(products_dataset_new.nlargest(11,productName)['product_name'])
            recommendations = recommendations[recommendations['product_name']!=productName]
            #print("productId - " + productId)
            recommendationsSet = []
            for index,row in recommendations.iterrows():
                    recommendationsSet.append(new_subset_products_dataset.loc[index]['product_id'])
            
            obj = {"product_id":product_id,"product_recommendations":recommendationsSet}
            recommendationsSetList.append(obj);        
        
        return recommendationsSetList
    
    def loadData_content_based_filtering_by_cosine_similarities():
        recommendationsSetList = RecommenderRepository.content_based_filtering_by_cosine_similarities();
        
        for data in recommendationsSetList:
            try:
                obj = {"$set":{"product_recommendations":data['product_recommendations']}}
                MongodbClient.db_mongo_update_many_documents(config["connection_string_mongo"],'test','products', {"product_id":data['product_id']},obj)
            except:
                print(data['product_id'])
                return 
        
        if recommendationsSetList == True:
           print("Product Data Loading Done")
           return (recommendationsSetList), 201
        else:
           return (recommendationsSetList), 400
        
    def correlation_matrix_on_product_rating():
        
        productRes = MongodbClient.db_mongo_find_documents(config["connection_string_mongo"],'test','products', {})
        products_dataset = pd.DataFrame(productRes)
        
        reviewRes = MongodbClient.db_mongo_find_documents(config["connection_string_mongo"],'test','reviews', {})
        review_dataset = pd.DataFrame(reviewRes)
        
        userRes = MongodbClient.db_mongo_find_documents(config["connection_string_mongo"],'test','users', {})
        users_dataset = pd.DataFrame(userRes)
        
        products_dataset = products_dataset.dropna()
                
        popular_products = products_dataset[['product_id','no_of_ratings']]
        review_sub_dataset = review_dataset.drop(['_id','rating'], axis=1)
        New_Product_Rating_Dataset = pd.merge(products_dataset,review_sub_dataset,on="product_id") 

        # Sorting the no_of_rating in the descending order
        most_popular = popular_products.sort_values('no_of_ratings', ascending=False)

        popular_products_1 =pd.DataFrame(New_Product_Rating_Dataset.groupby('product_id')['rating'].count())

        New_Product_Rating_Dataset = pd.merge(products_dataset,review_sub_dataset,on="product_id") 

        New_Product_Rating_Dataset = pd.merge(New_Product_Rating_Dataset,users_dataset,on="user_id")

        most_popular_products_1 = popular_products_1.sort_values('rating',ascending=False)

        ratings_utility_matrix = New_Product_Rating_Dataset.pivot_table(values='rating', index='user_id',columns='product_id',fill_value=0)

        #transpose the matrix
        X = ratings_utility_matrix.T

        #unique products
        X1 = X

        #Decomposing the matrix
        SVD = TruncatedSVD(n_components=10)
        decomposed_matrix = SVD.fit_transform(X)

        # Correlation Matrix
        correlation_matrix = np.corrcoef(decomposed_matrix)

        # lets say this product id purchased by customer
        product_names = list(X.index)

        RecommandedProducts = pd.DataFrame(columns=["product_id",'RecommendedList'])

        for indexNum, rowData in products_dataset.iterrows():
            productId = rowData['product_id']
            
            if productId in product_names:
                product_ID = product_names.index(productId)
            
                correlation_product_ID = correlation_matrix[product_ID]

                # recommending top 10 highly correlated products
                Recommend = list(X.index[correlation_product_ID > 0.90])

                # Removes the item already bought by the customer
                Recommend.remove(productId) 
                Recommend_products = Recommend[0:9]
                RecommandedProducts.loc[len(RecommandedProducts.index)]=[productId, Recommend_products] 
            
        RecommandedProducts_json_dataset = RecommandedProducts.to_dict(orient='records')
       
        return RecommandedProducts_json_dataset

    def autoencoder_based_collaborative_filter_model():
        
        productRes = MongodbClient.db_mongo_find_documents(config["connection_string_mongo"],'test','products', {})
        products_dataset = pd.DataFrame(productRes)

        reviewRes = MongodbClient.db_mongo_find_documents(config["connection_string_mongo"],'test','reviews', {})
        review_dataset = pd.DataFrame(reviewRes)
        
        userRes = MongodbClient.db_mongo_find_documents(config["connection_string_mongo"],'test','users', {})
        users_dataset = pd.DataFrame(userRes)
        
        amazon_review_data = review_dataset
        amazon_review_data = amazon_review_data[['user_id', 'product_id', 'rating']]
        amazon_review_data = amazon_review_data.drop_duplicates()
        
        # Creating a sparse pivot table with users in rows and items in columns
        users_items_matrix_df = amazon_review_data.pivot(index = 'user_id', columns = 'product_id', values  = 'rating').fillna(0)
        
        # input
        X = users_items_matrix_df.values
        y = users_items_matrix_df.values
        
        # Build model
        model = RecommenderRepository.autoEncoder(X)
        model.compile(optimizer = 'Adam', loss='mse')
        model.summary()
        
        # Predict new Matrix Interactions, set score zero on visualized games
        new_matrix = model.predict(X) * (X == 0)
        
        # converting the reconstructed matrix back to a Pandas dataframe
        new_users_items_matrix_df  = pd.DataFrame(new_matrix, columns = users_items_matrix_df.columns, index   = users_items_matrix_df.index)
        # Content Data of products
        amazon_review_data_ref = products_dataset
        amazon_review_data_ref = amazon_review_data_ref.drop(['_id','product_description','category','img_link','product_link','rating',"no_of_ratings","product_recommendations","price"], axis=1)

        userProductRecommendationList = []
        for index, row in users_dataset.iterrows():
            userId = row['user_id']
            tempDf = RecommenderRepository.recommender_for_user_cfm(users_items_matrix_df,user_id= userId, interact_matrix = users_items_matrix_df,df_content= amazon_review_data_ref)
            productsRecommendedListTemp = []
            for innerIndex, innerDfRow in tempDf.iterrows():
                productId = innerDfRow['product_id']
                score = innerDfRow["score"]
                productName = innerDfRow["product_name"]
                obj = {"product_id":productId,"score":score,"product_name":productName}
                productsRecommendedListTemp.append(obj)
            fullObj = {"user_id":userId,"recommended_products":productsRecommendedListTemp}
            userProductRecommendationList.append(fullObj)
            
        return userProductRecommendationList

    def autoencoder():
        
        reviewRes = MongodbClient.db_mongo_find_documents(config["connection_string_mongo"],'test','reviews', {})
        review_dataset = pd.DataFrame(reviewRes)
        
        userRes = MongodbClient.db_mongo_find_documents(config["connection_string_mongo"],'test','users', {})
        users_dataset = pd.DataFrame(userRes)

        user_product_rating_dataset = review_dataset.drop(['_id','review_id','review_title','review_content'], axis=1)

        # Create user-item interaction matrix
        user_product_matrix = user_product_rating_dataset.pivot(index='user_id', columns='product_id', values='rating').fillna(0).values

        # Split the data into training and testing sets
        train_data, test_data = train_test_split(user_product_matrix, test_size=0.2, random_state=42)

        # Build the autoencoder model
        num_users, num_items = user_product_matrix.shape
        latent_dim = 50

        input_layer = Input(shape=(num_items,))
        encoded = Dense(latent_dim, activation='relu')(input_layer)
        decoded = Dense(num_items, activation='sigmoid')(encoded)

        autoencoder = Model(inputs=input_layer, outputs=decoded)
        autoencoder.compile(optimizer='adam', loss='mean_squared_error')

        # Train the autoencoder
        autoencoder.fit(train_data, train_data, epochs=10, batch_size=64, shuffle=True, validation_data=(test_data, test_data))

        # Extract user and item representations from the encoder part of the autoencoder
        encoder = Model(inputs=input_layer, outputs=encoded)
        user_embeddings = encoder.predict(user_product_matrix)      

        userProductRecommendationList = []
        for index, row in users_dataset.iterrows():
            userId = row['user_id']
            productsRecommendedListTemp = RecommenderRepository.recommender_for_user(userId,user_product_rating_dataset, user_embeddings)
            if len(productsRecommendedListTemp) > 0:
                fullObj = {"user_id":userId,"recommended_products":productsRecommendedListTemp}
                userProductRecommendationList.append(fullObj)
                
        return userProductRecommendationList

    def loadData_autoencoder():
        userProductRecommendationList = RecommenderRepository.autoencoder();
        
        for data in userProductRecommendationList:
            try:
                obj = {"$set":{"product_recommendations":data['recommended_products']}}
                MongodbClient.db_mongo_update_many_documents(config["connection_string_mongo"],'test','users', {"user_id":data['user_id']},obj)
            except:
                print(data['user_id'])
                return 
        
        if userProductRecommendationList == True:
           print("Product Data Loading Done")
           return (userProductRecommendationList), 201
        else:
           return (userProductRecommendationList), 400
        
    
    # Private
    def autoEncoder(X):
        '''
        Autoencoder for Collaborative Filter Model
        '''

        # Input
        input_layer = Input(shape=(X.shape[1],), name='UserScore')
        
        # Encoder
        # -----------------------------
        enc = Dense(512, activation='selu', name='EncLayer1')(input_layer)

        # Latent Space
        # -----------------------------
        lat_space = Dense(256, activation='selu', name='LatentSpace')(enc)
        lat_space = Dropout(0.8, name='Dropout')(lat_space) # Dropout

        # Decoder
        # -----------------------------
        dec = Dense(512, activation='selu', name='DecLayer1')(lat_space)

        # Output
        output_layer = Dense(X.shape[1], activation='linear', name='UserScorePred')(dec)

        # this model maps an input to its reconstruction
        model = Model(input_layer, output_layer)    
        
        return model

    # Private
    def recommender_for_user_cfm(users_items_matrix_df,user_id, interact_matrix, df_content,topn = 10):
        '''
        Recommender Products for UserWarning
        '''
        pred_scores = interact_matrix.loc[user_id].values

        df_scores   = pd.DataFrame({'product_id': list(users_items_matrix_df.columns), 
                                'score': pred_scores})

        df_rec      = df_scores.set_index('product_id')\
                        .join(df_content.set_index('product_id'))\
                        .sort_values('score', ascending=False)\
                        .head(topn)[['score', 'product_name']]
        
        return df_rec[df_rec.score > 0].reset_index()    

    # Private
    def recommender_for_user(user_id, user_product_rating_dataset, user_embeddings):
        
        recommendationsList=[]
        try:
            user_index = user_product_rating_dataset.index[user_product_rating_dataset['user_id'] == user_id].tolist()[0]
            if(len(user_embeddings) > user_index):
                user_representation = user_embeddings[user_index - 1]
            else:
                return recommendationsList

            # Calculate the predicted ratings for all items
            predicted_ratings = np.dot(user_embeddings, user_representation)

            # Display top N recommendations
            top_n = np.argsort(predicted_ratings)[::-1][:10]

            for x in top_n:
                recommendationsList.append(user_product_rating_dataset.loc[x+1,"product_id"])
        except Exception as error:
            print(error);

        return recommendationsList

    # Don't Remove below products
    def loadPopularRecommandedProducts():
        popular_recommanded_products_dataset = RecommenderRepository.popular_recommanded_products()
        
        res = MongodbClient.db_mongo_insert_all_document(config["connection_string_mongo"],'test','PopularRecommandedProducts', popular_recommanded_products_dataset)
        
        if res == True:
            return (res), 201
        else:
            return (res), 400
   
    def load_popular_products(productId):
        
        products_dataset =pd.json_normalize(DataRepository.clean_products_data())
        
        temp_review_df = pd.json_normalize(DataRepository.clean_reviews_data())
        
        users_dataset = pd.json_normalize(DataRepository.clean_users_data())
        
        products_dataset = products_dataset.dropna()
        
        popular_products = products_dataset[
            [
                'product_id',
                'no_of_ratings'
            ]
        ]
        
        New_Product_Rating_Dataset = pd.merge(products_dataset,temp_review_df,on="product_id") 
        
        # Sorting the no_of_rating in the descending order
        most_popular = popular_products.sort_values('no_of_ratings', ascending=False)
        
        popular_products_1 =pd.DataFrame(New_Product_Rating_Dataset.groupby('product_id')['rating'].count())
        
        New_Product_Rating_Dataset = pd.merge(products_dataset,temp_review_df,on="product_id") 
        
        New_Product_Rating_Dataset = pd.merge(New_Product_Rating_Dataset,users_dataset,on="user_id")
        
        most_popular_products_1 = popular_products_1.sort_values('rating',ascending=False)
        
        ratings_utility_matrix = New_Product_Rating_Dataset.pivot_table(values='rating', index='user_id',columns='product_id',fill_value=0)
        
        #transpose the matrix
        X = ratings_utility_matrix.T
        
        #unique products
        X1 = X
       
        #Decomposing the matrix
        SVD = TruncatedSVD(n_components=10)
        decomposed_matrix = SVD.fit_transform(X)
        
        # Correlation Matrix

        correlation_matrix = np.corrcoef(decomposed_matrix)
        
        # lets say this product id purchased by customer

        product_names = list(X.index)

        product_ID = product_names.index(productId)

        product_ID
        # correlation for all items with the item purchased by this customer based on items rated by other customers who bought 
        # the same product
        correlation_product_ID = correlation_matrix[product_ID]

        # recommending top 10 highly correlated products
        Recommend = list(X.index[correlation_product_ID > 0.90])

        # Removes the item already bought by the customer
        Recommend.remove(productId) 

        Recommend_products = Recommend[0:9]

        Recommend_products
       
       
        return Recommend_products
    
    # Recommender based on textual clustering analysis given in product description to 
    # Recommend the products to the user without any purchase history
    def load_user_recommend_products_using_searchText(searchText):
        
        products_dataset =pd.json_normalize(DataRepository.clean_products_data())
        
             
        temp_review_df = pd.json_normalize(DataRepository.clean_reviews_data())
        
        users_dataset = pd.json_normalize(DataRepository.clean_users_data())
        
        New_Product_Rating_Dataset = pd.merge(products_dataset,temp_review_df,on="product_id") 
        
        New_Product_Rating_Dataset = pd.merge(New_Product_Rating_Dataset,users_dataset,on="user_id")
        
        Product_Description_Dataset = New_Product_Rating_Dataset[["product_id","product_name"]]
        
        Product_Description_Dataset.drop_duplicates()
        
        Product_Description_Dataset_1 = Product_Description_Dataset["product_name"].drop_duplicates()
        
        # Feature extraction from product description

        vectorizer = TfidfVectorizer(stop_words='english')
        X1 = vectorizer.fit_transform(Product_Description_Dataset_1)
        X1
        
        # visualizing the product cluster in subset of data

        X=X1

        k_means = KMeans(n_clusters = 10, init = 'k-means++')
        y_k_means = k_means.fit_predict(X)
        plt.plot(y_k_means, ".")
        
        # Recommend products based on current product selected

        def print_cluster(i):
            print("Cluster %d:" % i),
            for ind in order_centroids[i, :10]:
                print(' %s' % terms[ind]),
            print
        
        true_k = 10

        model = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)
        model.fit(X1)

        print("Top terms per cluster:")
        order_centroids = model.cluster_centers_.argsort()[:, ::-1]
        terms = vectorizer.get_feature_names_out()
        for i in range(true_k):
            print_cluster(i)
            
            
        # predicting cluster based on the key search words
        def show_recommendations(product):
            #print("Cluster ID:")
            Y = vectorizer.transform([product])
            prediction = model.predict(Y)
            #print(prediction)
            print_cluster(prediction[0])
            
        # let say the product we are searching for is iPhone
        Recommended_user_products = show_recommendations(searchText)
        
        return Recommended_user_products
        
        