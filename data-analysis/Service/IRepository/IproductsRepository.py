from abc import abstractmethod

class IproductsRepository(object):

    @abstractmethod
    def get_trading_products(self):
        raise NotImplementedError

    @abstractmethod
    def get_popular_products(self):
        raise NotImplementedError
    
    @abstractmethod
    def get_user_browsing_history(self):
        raise NotImplementedError