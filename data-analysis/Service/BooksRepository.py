from Service.IRepository.IbooksRepository import IbooksRepository
from os import sep
import pandas as pd # pip install pandas
from scipy.sparse import csr_matrix # pip install scipy
from sklearn.neighbors import NearestNeighbors # pip install -U scikit-learn scipy matplotlib

class BooksRepository(IbooksRepository):

    def get_book_suggestions():

        # delimiter is to separate the content, encoding- a the dataset is formatted with latin 1, on_bad_lines is to skip the lines that have issues
        books = pd.read_csv("./Data/BX-Books.csv", delimiter=';', encoding='latin-1', on_bad_lines='skip')

        # from about all columns we are ignoring few columns
        books = books[['ISBN', 'Book-Title', 'Book-Author', 'Year-Of-Publication', 'Publisher', 'Image-URL-L']]

        #rename the column as names as they are little big
        books.rename(columns={
                "Book-Title": 'title',
                "Book-Author":'author',
                'Year-Of-Publication':'year',
                'Publisher':'publisher',
                'Image-URL-L':'img_url',
            }, inplace=True) # inplace is to permanently change the column names

        # read users dataset
        users = pd.read_csv("./Data/BX-Users.csv", sep=';', encoding='latin-1', on_bad_lines='skip')
        
        ratings = pd.read_csv("./Data/BX-Book-Ratings.csv", delimiter=';', encoding='latin-1', on_bad_lines='skip')
        
        ratings.rename(columns={
                "User-ID": 'user_id',
                "Book-Rating":'rating'
            },inplace = True)

        # Taking only the users who rated more than 200 books and ignoring the users rated less 
        print(ratings['user_id'].unique().shape) # total no of users rated the books  (105283,)
        x = ratings['user_id'].value_counts() > 200 # no of users rated more than 200 books
        print(x[x].shape) # (899,) - this is the total no of users who rated more than 200 books out of 105283 user ratings
        
        y = x[x].index # taking the index of the users who rated more than 200 books and store it in the variable y
        
        print(y) # so there will be total of 899 user id's
        
        ratings = ratings[ratings['user_id'].isin(y)]
        
        print(ratings.head()) # information of users and their ratings for the particular book ISBN
        
        print(ratings.shape)# (526356, 3)
        
        # now get the name of the books by combining this table with the books data
        ratings_with_books = ratings.merge(books, on='ISBN') # merging two table as they have the common colum of ISBN in both table
        print(ratings_with_books.head(4))
        print(ratings_with_books.columns)
        
        # making title and no_of_ratings to that book in one table
        num_rating = ratings_with_books.groupby('title')['rating'].count().reset_index()
        print(num_rating.head())
        print(num_rating.columns)
        
        num_rating.rename(columns={ # changing the name of the column
                "rating": 'num_of_rating'
            
        },inplace = True)
        
    
        final_rating = ratings_with_books.merge(num_rating, on ='title') #merging two table ratings_with_books and num_rating by making title of the book as the common column

        # filtering the books having the num_of_rating more than or equal to 50
        final_rating = final_rating[final_rating['num_of_rating']>=50]
        final_rating.drop_duplicates(['user_id','title'],inplace=True)
        
        #making the pivot table by taking user_id, title and rating
        book_pivot = final_rating.pivot_table(columns='user_id', index='title',values='rating')

        # make all NaN values to 0 in the matrix
        book_pivot.fillna(0, inplace=True)

        # As this book_pivot matrix has more zeroes and when we train the dataset which is given to the clustering algorithm it will measure the distance between the columns
        # so we should not consider zeros. to do that we need to add csr_matrix on top of the book_pivot which helps in ignoring zeros and calculate by considering only the values more than zero
        book_sparse = csr_matrix(book_pivot)  

        # Now we have the dataset with no zeros and e will pass this data to the nearest neighbor model and use the algorithm called brute algorithm
        model = NearestNeighbors(algorithm='brute')
        model.fit(book_sparse)

        #We need to pass the index of the row and pass all the columns with their values. reshape is because we are passing one record having its index as 237 in the matrix
        # and the n_neighbors is how many books you want to see in the suggestion
        distance , suggestion = model.kneighbors(book_pivot.iloc[240,:].values.reshape(1,-1), n_neighbors=6) # kneighbors produces two outputs, one is the distance between the columns and other is the suggestion
        
        # to see the names of the suggested book we need to loop through the suggestions
        for i in range(len(suggestion)):
            suggested_books = book_pivot.index[suggestion[i]]
            json_string = suggested_books.tolist()
            
        return json_string


    def get_book_suggestions_by_user(self, userId):
        
        return ""
    
