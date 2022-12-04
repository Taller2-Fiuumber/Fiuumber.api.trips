import unittest
import mongomock
import pymongo
import datetime


class PatchTest(unittest.TestCase):
    @mongomock.patch()
    def test__decorator(self):
        client1 = pymongo.MongoClient()

        client1.db.coll.insert_one(
            {
                "driverId": 1,
                "tripId": 2,
                "start": datetime.datetime(2002, 11, 28, 6, 0, 0),
            }
        )
        client1.db.coll.insert_one(
            {
                "driverId": 1,
                "tripId": 5,
                "start": datetime.datetime(2002, 10, 28, 6, 0, 0),
            }
        )

        client2 = pymongo.MongoClient()
        self.assertEqual(["db"], client2.list_database_names())

        self.assertEqual(
            5,
            client2.db.coll.find_one(
                {"driverId": 1, "start": datetime.datetime(2002, 10, 28, 6, 0, 0)}
            )["tripId"],
        )
        client2.db.coll.drop()

        self.assertEqual(None, client1.db.coll.find_one())

    @mongomock.patch()
    def test_trip_get_today(self):
        client1 = pymongo.MongoClient()

        client1.db.coll.insert_one(
            {
                "driverId": 1,
                "tripId": 2,
                "start": datetime.datetime(2002, 10, 28, 2, 0, 0),
            }
        )
        client1.db.coll.insert_one(
            {
                "driverId": 1,
                "tripId": 5,
                "start": datetime.datetime(2002, 10, 28, 6, 0, 0),
            }
        )

        client2 = pymongo.MongoClient()
        self.assertEqual(["db"], client2.list_database_names())

        self.assertEqual(
            5,
            client2.db.coll.find_one(
                {"driverId": 1, "start": datetime.datetime(2002, 10, 28, 6, 0, 0)}
            )["tripId"],
        )
        client2.db.coll.drop()

        self.assertEqual(None, client1.db.coll.find_one())
