from lib.models.feature_requests import FeatureRequest
from lib.models import db, utils
from flask_login import current_user
from datetime import datetime


def get_feature_requests():
    if current_user.client == 'ALL':
        raw = (db.db_session
               .query(FeatureRequest.id, FeatureRequest.title,
                      FeatureRequest.description,
                      FeatureRequest.client,
                      FeatureRequest.client_priority,
                      FeatureRequest.target_date,
                      FeatureRequest.product_area)
               .order_by(FeatureRequest.client)
               .order_by(FeatureRequest.client_priority)
               .all())
    else:
        raw = (db.db_session
               .query(FeatureRequest.id, FeatureRequest.title,
                      FeatureRequest.description,
                      FeatureRequest.client,
                      FeatureRequest.client_priority,
                      FeatureRequest.target_date,
                      FeatureRequest.product_area)
               .filter(FeatureRequest.client == current_user.client)
               .order_by(FeatureRequest.client)
               .order_by(FeatureRequest.client_priority)
               .all())
    keys = ['id', 'title', 'description', 'client',
            'client_priority', 'target_date', 'product_area']
    frs = [dict(zip(keys, result)) for result in raw]
    return frs


def get_client_list():
    return current_user.client


def submit_feature_requests(title, description, client, priority,
                            target_date, product_area):
    # If a FR for the client with the same priority is present
    client = client['name']
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
    raw = (FeatureRequest.query
           .filter(FeatureRequest.id == id)
           .first())
    raw = utils.to_dict(raw)
    raw['clientList'] = current_user.client
    return raw


def update_feature_requests(id, title, description, client, priority,
                            target_date, product_area):
    # Update current row
    client = client['name']
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
    db.db_session.commit()  # To reflect the changes in the next block of code

    # Update priority of other FRs if affected
    raw = (FeatureRequest.query
           .filter(FeatureRequest.client_priority == priority)
           .filter(FeatureRequest.client == client)
           .first())
    if raw:
        rows = (FeatureRequest.query
                .filter(FeatureRequest.client_priority >= priority)
                .filter(FeatureRequest.client == client)
                .filter(FeatureRequest.id != id)  # To prevent incrementing the same row
                .all())
        for row in rows:
            row.client_priority = int(row.client_priority) + 1  # Why is this happening
            db.db_session.add(row)


def update_for_drag_drop(client, new_priorities):
    rows = (FeatureRequest.query
            .filter(FeatureRequest.client == client)
            .all())
    for row in rows:
        row.client_priority = new_priorities[str(row.id)]
    db.db_session.add(row)
    db.db_session.commit()
    return get_feature_requests()
