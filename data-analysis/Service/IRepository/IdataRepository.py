from abc import abstractmethod


class IdataRepository(object):

    @abstractmethod
    def load_products_data(self):
        raise NotImplementedError

    @abstractmethod
    def load_users_data(self):
        raise NotImplementedError
    
    @abstractmethod
    def load_ratings_data(self):
        raise NotImplementedError