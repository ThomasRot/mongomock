from unittest.mock import call
import unittest

import mongomock


class MongoMockCollectionHistory(unittest.TestCase):
    def setUp(self):
        super(MongoMockCollectionHistory, self).setUp()
        self.client = mongomock.MongoClient()
        self.db = self.client['somedb']

    def test__assert_called_with(self):
        col = self.db.a
        call_history = col.mongo_mock_call_history

        col.insert_one({'key': 'value'})
        call_history.insert_one.assert_called_with({'key': 'value'})
        call_history.insert_one.assert_called_once()
        call_history.insert_one.assert_called()
        with self.assertRaises(AssertionError):
            call_history.insert_one.assert_called_with({'key': 'other'})

        col.insert_one({'key': 'new_value'})
        with self.assertRaises(AssertionError):
            call_history.insert_one.assert_called_with({'key': 'value'})

    def test__assert_any_call(self):
        col = self.db.a
        call_history = col.mongo_mock_call_history

        col.insert_one({'key': 'value'})
        col.insert_one({'key': 'new_value'})

        call_history.insert_one.assert_any_call({'key': 'value'})
        with self.assertRaises(AssertionError):
            call_history.insert_one.assert_any_call({'key': 'other'})

    def test__assert_has_calls(self):
        col = self.db.a
        call_history = col.mongo_mock_call_history

        col.insert_one({'key': 'value'})
        col.insert_one({'key': 'new_value'})

        call_history.insert_one.assert_has_calls(
            [call({'key': 'value'}), call({'key': 'new_value'})])
        with self.assertRaises(AssertionError):
            call_history.insert_one.assert_has_calls(
                [call({'key': 'value'}), call({'key': 'false_value'})])

        call_history.insert_one.assert_has_calls(
            [call({'key': 'new_value'}), call({'key': 'value'})], any_order=True)

        with self.assertRaises(AssertionError):
            call_history.insert_one.assert_has_calls(
                [call({'key': 'false_value'}), call({'key': 'value'})], any_order=True)

        with self.assertRaises(AssertionError):
            call_history.insert_one.assert_has_calls([call({'key': 'value'})], any_order=True)

        with self.assertRaises(AssertionError):
            call_history.insert_one.assert_has_calls([call({'key': 'value'}), call(
                {'key': 'value'}), call({'key': 'new_value'})], any_order=True)

    def test__assert_not_called(self):
        col = self.db.a
        call_history = col.mongo_mock_call_history

        call_history.insert_one.assert_not_called()
        col.insert_one({'key': 'value'})

        with self.assertRaises(AssertionError):
            call_history.insert_one.assert_not_called()


if __name__ == '__main__':
    unittest.main()
