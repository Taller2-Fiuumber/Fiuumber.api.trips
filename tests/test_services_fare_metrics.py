import mongomock
from fastapi.encoders import jsonable_encoder
from src.domain.trip import Trip
import src.services.fare_metrics as service


DB_NAME = "Fiuumber"


class TestFareCalculator:
    def setUp(self):
        external_data_1 = {
            "id": "1",
            "passengerId": "066de609-b04a-4b30-b46c-32537c7f1f6e",
            "driverId": "2320930329-b04a-4b30-b46c-fsdfwefwefw",
            "from_latitude": -34.603683,
            "from_longitude": -58.381557,
            "to_latitude": -34.6175841,
            "to_longitude": -58.3682286,
            "subscription": "REGULAR",
            "status": "TERMINATED",
            "finalPrice": 500.0,
            "from_address": "Calle Falsa 123",
            "to_address": "Calle Falsa 666",
        }
        trip1 = Trip(**external_data_1)

        external_data_2 = {
            "id": "2",
            "passengerId": "077de609-b04a-4b30-b46c-32537c7f1f6e",
            "driverId": "2220930329-b04a-4b30-b46c-fsdfwefwefw",
            "from_latitude": -39.603683,
            "from_longitude": -50.381557,
            "to_latitude": -31.6175841,
            "to_longitude": -55.3682286,
            "subscription": "REGULAR",
            "status": "TERMINATED",
            "finalPrice": 1000.0,
            "from_address": "Calle Real 123",
            "to_address": "Calle Real 111",
        }
        trip2 = Trip(**external_data_2)

        self.trip1 = jsonable_encoder(trip1)
        self.trip2 = jsonable_encoder(trip2)

    def test_find_fare_avg(self):
        self.setUp()
        mongo_client = mongomock.MongoClient()
        mongo_client[DB_NAME]["trips"].insert_one(self.trip1)
        mongo_client[DB_NAME]["trips"].insert_one(self.trip2)

        assert service.find_fare_avg(mongo_client) == 750

    def test_find_fare_min(self):
        self.setUp()
        mongo_client = mongomock.MongoClient()
        mongo_client[DB_NAME]["trips"].insert_one(self.trip1)
        mongo_client[DB_NAME]["trips"].insert_one(self.trip2)

        assert service.find_fare_min(mongo_client) == 500

    def test_find_fare_max(self):
        self.setUp()
        mongo_client = mongomock.MongoClient()
        mongo_client[DB_NAME]["trips"].insert_one(self.trip1)
        mongo_client[DB_NAME]["trips"].insert_one(self.trip2)
        assert service.find_fare_max(mongo_client) == 1000
