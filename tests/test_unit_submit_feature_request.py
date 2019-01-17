"""Unit test for submit_feature_request."""

import sys
import os
sys.path.append(os.getcwd())


import unittest # noqa
from mock import Mock, patch # noqa
from lib.feature_requests.views import submit_feature_requests  # noqa


class TestSubmitFeatureRequest(unittest.TestCase):

    def setUp(self):
        def create_object(*args):
            return Mock(client_priority=args[3])

        self.fr_instance_1 = Mock(client_priority=1)
        self.fr_instance_2 = Mock(client_priority=2)

        self.FeatureRequestMock = Mock(client_priority=0,
                                       side_effect=create_object)
        self.FeatureRequestMock.query.filter().count.return_value = 2
        self.FeatureRequestMock.query.filter().filter().all.return_value = [
            self.fr_instance_1, self.fr_instance_2
        ]

        self.db_mock = Mock()

        self.added_to_db = list()

        def add_to_db(item):
            self.added_to_db.append(item)

        self.db_mock.db_session.add = Mock(side_effect=add_to_db)

        self.patch = patch.multiple(
            'lib.feature_requests.views',
            FeatureRequest=self.FeatureRequestMock,
            db=self.db_mock
        )

        self.patch.start()
        self.addCleanup(self.patch.stop)

    def test_priority_less_than_one(self):
        self.FeatureRequestMock.query.filter().filter().all.return_value = []
        submit_feature_requests('title', 'description', {'name': 'client_1'},
                                -1, '2100-01-01', 'billing')

        # Only item has changed
        self.assertEqual(len(self.added_to_db), 1)

        # Priority has been set to 1 instead of -1 that was passed
        self.assertEqual(self.added_to_db[0].client_priority, 1)

    def test_priority_collision(self):
        submit_feature_requests('title', 'description', {'name': 'client_1'},
                                1, '2100-01-01', 'billing')

        # Three items have changed
        self.assertEqual(len(self.added_to_db), 3)

        # Existing requests have their priorities bumped down
        self.assertEqual(self.added_to_db[0].client_priority, 2)
        self.assertEqual(self.added_to_db[1].client_priority, 3)

        # New request gets priority 1 as per the function call
        self.assertEqual(self.added_to_db[2].client_priority, 1)

    def test_priority_more_than_number_of_items(self):
        self.FeatureRequestMock.query.filter().filter().all.return_value = []
        submit_feature_requests('title', 'description', {'name': 'client_1'},
                                10, '2100-01-01', 'billing')

        # Only item has changed
        self.assertEqual(len(self.added_to_db), 1)

        # Priority has been set to 3 (number of requests) instead of 10
        self.assertEqual(self.added_to_db[0].client_priority, 3)


if __name__ == "__main__":
    unittest.main()
