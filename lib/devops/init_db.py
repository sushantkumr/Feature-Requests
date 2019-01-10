"""Initialize the DB with seed data."""

import os
import sys
from datetime import datetime

sys.path.append(os.getcwd())

from lib.core.config import get_config
from lib.models import db
from lib.models.featurerequests import FeatureRequest


try:
    os.remove(get_config()['connection_string'][10:])
except:
    # If it doesn't exist already
    pass

db.init_db()

due_date = datetime(2019, 6, 1, 10, 10, 10)
user = FeatureRequest('Title-1', 'Words dont matter', 'Client A', 1,
                      due_date, 'Billing')
user.email_verified = True
db.db_session.add(user)

db.db_session.commit()
