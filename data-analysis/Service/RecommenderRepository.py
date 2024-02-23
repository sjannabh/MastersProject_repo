from Service.IRepository.IrecommenderRepository import IrecommenderRepository
from Service.DataRepository import DataRepository
from sklearn.decomposition import TruncatedSVD
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.neighbors import NearestNeighbors
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
import matplotlib.pyplot as plt
from Util.MongodbClient import MongodbClient
from dotenv import dotenv_values

config = dotenv_values(".env")


class RecommenderRepository(IrecommenderRepository):
    
    def popular_recommanded_products():
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
            
        RecommandedProducts_dataset = RecommandedProducts.to_dict(orient='records')
       
        return RecommandedProducts_dataset
    
    def loadPopularRecommandedProducts():
        popular_recommanded_products_dataset = RecommenderRepository.popular_recommanded_products()
        
        res = res = MongodbClient.db_mongo_insert_all_document(config["connection_string_mongo"],'MyDb','PopularRecommandedProducts', popular_recommanded_products_dataset)
        
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
        
        