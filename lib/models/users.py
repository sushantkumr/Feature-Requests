from lib.models.db import Base
from flask_login import UserMixin
from sqlalchemy import Boolean, Column, DateTime, String

import datetime
import uuid
from lib.models import utils


class User(UserMixin, Base):
    __tablename__ = 'user'
    id = Column(String(36), primary_key=True)
    name = Column(String(100))
    created_at = Column(DateTime)
    salt = Column(String(29))
    hash = Column(String(60))
    is_admin = Column(Boolean)

    def __init__(self, password, name, is_admin=False):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.datetime.now()
        self.name = name
        self.salt, self.hash = utils.hash_password(password)
        self.is_admin = is_admin
        self.email_verified = False

    def __repr__(self):
        return '<User %r>' % (self.name)