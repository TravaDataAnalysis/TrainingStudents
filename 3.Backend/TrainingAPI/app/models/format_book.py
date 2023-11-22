from typing import Optional

from pydantic import BaseModel

class Create_Book(BaseModel):
    self._id = _id
    self.title = ''
    self.authors = []
    self.publisher = ''
    self.description = None
    self.owner = None
    self.created_at = int(time.time())
    self.last_updated_at = int(time.time())