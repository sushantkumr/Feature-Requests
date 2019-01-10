from lib.models.feature_requests import FeatureRequest
from lib.models import db, utils
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
    # If a FR for the client with the same priority is present
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


def get_feature_request_details(id):
    # import pudb; pudb.set_trace();
    raw = (FeatureRequest.query
           .filter(FeatureRequest.id == id)
           .first())
    raw = utils.to_dict(raw)
    return raw


def update_feature_requests(id, title, description, client, priority,
                            target_date, product_area):
    import pudb; pudb.set_trace();
    # Update current row
    row = (FeatureRequest.query
           .filter(FeatureRequest.id == id)
           .first())
    row.title = title
    row.description = description
    row.client = client
    row.client_priority = priority
    row.target_date = datetime.strptime(target_date, '%Y-%m-%d')
    row. product_area = product_area
    db.db_session.add(row)

    # Update priority of other FRs if affected
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
