from pymongo import MongoClient

from app.constants.mongodb_constants import MongoCollections
from app.models.book import Book
from app.utils.logger_utils import get_logger
from config import MongoDBConfig

logger = get_logger('MongoDB')


class MongoDB:
    def __init__(self, connection_url=None):
        if connection_url is None:
            connection_url = f'mongodb://{MongoDBConfig.USERNAME}:{MongoDBConfig.PASSWORD}@{MongoDBConfig.HOST}:{MongoDBConfig.PORT}'

        self.connection_url = connection_url.split('@')[-1]
        self.client = MongoClient(connection_url)
        self.db = self.client[MongoDBConfig.DATABASE]

        self._books_col = self.db[MongoCollections.books]

    def get_books(self, filter_=None, projection=None):
        try:
            if not filter_:
                filter_ = {}
            cursor = self._books_col.find(filter_, projection=projection)
            data = []
            for doc in cursor:
                data.append(Book().from_dict(doc))
            return data
        except Exception as ex:
            logger.exception(ex)
        return []

    def get_book(self, _filter=None, projection=None):
        try:
            if not _filter:
                _filter = {}
                cursor = self._books_col.find_one(filter=_filter, projection=projection)

                return cursor
        except Exception as ex:
            logger.exception(ex)
            return None

    def add_book(self, book: Book):
        try:
            inserted_doc = self._books_col.insert_one(book.to_dict())
            return inserted_doc
        except Exception as ex:
            logger.exception(ex)
        return None

    def update_book(self, _id):
        try:
            _filter = {"_id": _id}
            update_operation = {"$set": {"name": "English 1"}}
            update_doc = self._books_col.update_one(_filter, update_operation)
            return update_doc
        except Exception as ex:
            logger.exception(ex)
            return None

    def delete_book(self, _id):
        try:
            _filter = {"_id": _id}
            delete_doc = self._books_col.delete_one(_filter)
            return delete_doc
        except Exception as ex:
            logger.exception(ex)
            return None
