import time


class Book:
    def __init__(self, _id=''):
        self._id = _id
        self.title = ''
        self.authors = []
        self.publisher = ''
        self.description = None
        self.owner = None
        self.created_at = int(time.time())
        self.last_updated_at = int(time.time())

    def to_dict(self):
        return {
            '_id': self._id,
            'title': self.title,
            'authors': self.authors,
            'publisher': self.publisher,
            'description': self.description,
            'owner': self.owner,
            'createdAt': self.created_at,
            'lastUpdatedAt': self.last_updated_at
        }

    def from_dict(self, json_dict: dict):
        self._id = json_dict.get('_id', self._id)
        self.title = json_dict.get('title', '')
        self.authors = json_dict.get('authors', [])
        self.publisher = json_dict.get('publisher', '')
        self.description = json_dict.get('description')
        self.owner = json_dict.get('owner')
        self.created_at = json_dict.get('createdAt', int(time.time()))
        self.last_updated_at = json_dict.get('lastUpdatedAt', int(time.time()))
        return self


create_book_json_schema = {
    'type': 'object',
    'properties': {
        'title': {'type': 'string'},
        'authors': {'type': 'array', 'items': {'type': 'string'}},
        'publisher': {'type': 'string'},
        'description': {'type': 'string'},
    },
    'required': ['title', 'authors', 'publisher']
}
