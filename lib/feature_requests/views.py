from lib.models.feature_requests import FeatureRequest
from lib.models import db
from datetime import datetime


def get_feature_requests():
    raw = (db.db_session
           .query(FeatureRequest.id, FeatureRequest.title,
                  FeatureRequest.description,
                  FeatureRequest.client,
                  FeatureRequest.client_priority,
                  FeatureRequest.target_date,
                  FeatureRequest.product_area)
           .all())
    keys = ['id', 'title', 'description', 'client',
            'client_priority', 'target_date', 'product_area']
    frs = [dict(zip(keys, result)) for result in raw]
    return frs


def submit_feature_requests(title, description, client, priority,
                            target_date, product_area):
    raw = (FeatureRequest.query
           .filter(FeatureRequest.client_priority == priority)
           .filter(FeatureRequest.client == client)
           .first())
    if raw:
        rows = (FeatureRequest.query
                .filter(FeatureRequest.client_priority >= priority)
                .filter(FeatureRequest.client == client)
                .all())
        for row in rows:
            row.client_priority = row.client_priority + 1
            db.db_session.add(row)
    target_date = datetime.strptime(target_date, '%Y-%m-%d')
    fr = FeatureRequest(title, description, client, priority,
                        target_date, product_area)
    db.db_session.add(fr)
