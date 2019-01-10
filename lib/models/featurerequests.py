from sqlalchemy import Column, Integer, String, Text, DateTime
from lib.models.db import Base


class FeatureRequest(Base):
    CLIENTS = [
        (u'client-a', u'Client A'),
        (u'client-b', u'Client B'),
        (u'client-c', u'Client C'),
    ]
    PRODUCT_AREAS = [
        (u'policies', u'Policies'),
        (u'billing', u'Billing'),
        (u'claims', u'Claims'),
        (u'reports', u'Reports'),
    ]
    __tablename__ = 'feature_requests'
    id = Column(Integer, primary_key=True)
    title = Column(String(50))
    description = Column(Text)
    client = Column(String(20))
    client_priority = Column(Integer, nullable=False)
    target_date = Column(DateTime, nullable=False)
    product_area = Column(String(20))
    # product_area = Column(ChoiceType(PRODUCT_AREAS))

    def __init__(self, title=None, description=None, client=None,
                 client_priority=1, target_date=None, product_area=None):
        """Constructor."""
        self.title = title
        self.description = description
        self.client = client
        self.client_priority = client_priority
        self.target_date = target_date
        self.product_area = product_area

    def __repr__(self):
        return '<FeatureRequest %r>' % (self.title)
