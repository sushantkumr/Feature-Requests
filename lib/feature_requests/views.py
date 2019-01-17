from lib.models.feature_requests import FeatureRequest
from lib.models import db, utils
from flask_login import current_user
from datetime import datetime


def get_feature_requests():
    if current_user.client == 'ALL':
        rows = (db.db_session
                .query(FeatureRequest.id, FeatureRequest.title,
                       FeatureRequest.description,
                       FeatureRequest.client,
                       FeatureRequest.client_priority,
                       FeatureRequest.target_date,
                       FeatureRequest.product_area)
                .order_by(FeatureRequest.client_priority)
                .order_by(FeatureRequest.client)
                .all())
    else:
        rows = (db.db_session
                .query(FeatureRequest.id, FeatureRequest.title,
                       FeatureRequest.description,
                       FeatureRequest.client,
                       FeatureRequest.client_priority,
                       FeatureRequest.target_date,
                       FeatureRequest.product_area)
                .filter(FeatureRequest.client == current_user.client)
                .order_by(FeatureRequest.client_priority)
                .order_by(FeatureRequest.client)
                .all())
    keys = ['id', 'title', 'description', 'client',
            'client_priority', 'target_date', 'product_area']
    frs = [dict(zip(keys, result)) for result in rows]
    return frs


def get_client_list():
    # TODO: Move this to database
    client = current_user.client
    if client == 'ALL':
        return [
                {'id': 0, 'name': 'ALL'},
                {'id': 1, 'name': 'Client A'},
                {'id': 2, 'name': 'Client B'},
                {'id': 3, 'name': 'Client C'},
               ]
    else:
        return [{'id': 0, 'name': client}]


def submit_feature_requests(title, description, client, priority,
                            target_date, product_area):
    client = client['name']
    if int(priority) < 1:
        priority = 1
    count = (FeatureRequest.query
             .filter(FeatureRequest.client == client)
             .count())
    if int(priority) > count:
        priority = count + 1
    # If a FR for the client with the same priority is present
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
    fr_details = (FeatureRequest.query
                  .filter(FeatureRequest.id == id)
                  .first())
    fr_details = utils.to_dict(fr_details)
    fr_details['clientList'] = get_client_list()
    return fr_details


def update_feature_requests(id, title, description, client, priority,
                            target_date, product_area):
    # Update current row
    import pudb; pudb.set_trace();
    client = client['name']
    row = (FeatureRequest.query
           .filter(FeatureRequest.id == id)
           .first())

    old_client = row.client
    old_priority = row.client_priority
    if int(priority) < 1:
        priority = 1
    count = (FeatureRequest.query
             .filter(FeatureRequest.client == client)
             .count())
    if int(priority) > count:
        priority = count + 1

    row.title = title
    row.description = description
    row.client = client
    row.client_priority = priority
    row.target_date = datetime.strptime(target_date, '%Y-%m-%d')
    row.product_area = product_area

    db.db_session.add(row)
    db.db_session.flush()  # To reflect the changes in the next block of code

    # Restrict movement within moved FRs
    if old_client == client:
        if old_priority < int(priority):
            rows = (FeatureRequest.query
                    .filter(FeatureRequest.client_priority >= old_priority)
                    .filter(FeatureRequest.client_priority <= priority)
                    .filter(FeatureRequest.client == client)
                    .filter(FeatureRequest.id != id)
                    .all())
            for row in rows:
                row.client_priority = int(row.client_priority) - 1
                db.db_session.add(row)
        else:
            rows = (FeatureRequest.query
                    .filter(FeatureRequest.client_priority <= old_priority)
                    .filter(FeatureRequest.client_priority >= priority)
                    .filter(FeatureRequest.client == client)
                    .filter(FeatureRequest.id != id)
                    .all())
            for row in rows:
                row.client_priority = int(row.client_priority) + 1
                db.db_session.add(row)
    else:
        # Fill gap created by the moved FR
        rows = (FeatureRequest.query
                .filter(FeatureRequest.client_priority > old_priority)
                .filter(FeatureRequest.client_priority > 0)
                .filter(FeatureRequest.client == old_client)
                .all())
        for row in rows:
            row.client_priority = int(row.client_priority) - 1
            db.db_session.add(row)

        # Push other FRs to accomodate new FR
        rows = (FeatureRequest.query
                .filter(FeatureRequest.client_priority >= priority)
                .filter(FeatureRequest.id != id)
                .filter(FeatureRequest.client == client)
                .all())
        for row in rows:
            row.client_priority = int(row.client_priority) + 1
            db.db_session.add(row)


def update_for_drag_drop(client, new_priorities):
    rows = (FeatureRequest.query
            .filter(FeatureRequest.client == client)
            .all())
    for row in rows:
        row.client_priority = new_priorities[str(row.id)]
    db.db_session.add(row)
    db.db_session.flush()
    return get_feature_requests()


def delete_request(id, priority, client):
    rows = (FeatureRequest.query
            .filter(FeatureRequest.id != id)
            .filter(FeatureRequest.client == client)
            .all())
    for row in rows:
        if row.client_priority > priority:
            row.client_priority = int(row.client_priority) - 1
            db.db_session.add(row)
    (FeatureRequest.query
     .filter(FeatureRequest.id == id).delete())
    db.db_session.flush()
    return get_feature_requests()
