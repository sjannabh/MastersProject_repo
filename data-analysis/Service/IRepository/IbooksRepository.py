from abc import abstractmethod

class IbooksRepository(object):

    @abstractmethod
    def get_book_suggestions(self):
        raise NotImplementedError

    @abstractmethod
    def get_book_suggestions_by_user(self, userId):
        raise NotImplementedError




