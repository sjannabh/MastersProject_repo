from abc import abstractmethod


class IrecommenderRepository(object):

    @abstractmethod
    def load_popular_products(self, productId):
        raise NotImplementedError
    
    @abstractmethod
    def load_user_recommend_products(self, searchText):
        raise NotImplementedError