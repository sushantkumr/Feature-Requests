"""Initialize the DB with seed data."""

import os
import sys
from datetime import datetime

sys.path.append(os.getcwd())

from lib.core.config import get_config # noqa
from lib.models import db # noqa
from lib.models.feature_requests import FeatureRequest # noqa
from lib.models.users import User # noqa


try:
    os.remove(get_config()['connection_string'][10:])
except:  # noqa
    # If it doesn't exist already
    pass

db.init_db()

user = User('123456789012', 'sushant')
db.db_session.add(user)

due_date = datetime(2019, 6, 1, 10, 10, 10)
user = FeatureRequest('Title-1', 'Words dont matter', 'Client A', 1,
                      due_date, 'Billing')
user.email_verified = True
db.db_session.add(user)

db.db_session.commit()
