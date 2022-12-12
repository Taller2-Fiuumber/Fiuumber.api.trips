import mongomock
from mongomock import helpers
from mongomock import read_concern
from fastapi.encoders import jsonable_encoder
from src.domain.trip import Trip
import src.services.fare_metrics as service

from os import environ
DB_NAME = environ["DB_NAME"]


class TestTripMetrics:

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
            "finalPrice": 500,
            "from_address": "Calle Falsa 123",
            "to_address": "Calle Falsa 666",
            "start": "2022-09-09T02:00:00",
            "finish": "2022-09-10T09:00:00",
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
            "finalPrice": 1000,
            "from_address": "Calle Real 123",
            "to_address": "Calle Real 111",
            "start": "2022-09-09T02:00:00",
            "finish": "2022-09-10T02:10:00",
        }
        trip2 = Trip(**external_data_2)

        external_data_3 = {
            "id": "2",
            "passengerId": "0771de609-b04a-4b30-b46c-32537c7f1f6e",
            "driverId": "22209330329-b04a-4b30-b46c-fsdfwefwefw",
            "from_latitude": -19.603683,
            "from_longitude": -70.381557,
            "to_latitude": -32.6175841,
            "to_longitude": -54.3682286,
            "subscription": "REGULAR",
            "status": "TERMINATED",
            "finalPrice": 1000,
            "from_address": "Calle Real 123",
            "to_address": "Calle Real 111",
            "start": "2022-09-09T02:00:00",
            "finish": "2022-09-10T02:01:00",
        }
        trip3 = Trip(**external_data_3)

        external_data_4 = {
            "id": "2",
            "passengerId": "087de609-b04a-4b30-b46c-32537c7f1f6e",
            "driverId": "22202930329-b04a-4b30-b46c-fsdfwefwefw",
            "from_latitude": -39.603683,
            "from_longitude": -50.381557,
            "to_latitude": -31.6175841,
            "to_longitude": -55.3682286,
            "subscription": "REGULAR",
            "status": "TERMINATED",
            "finalPrice": 1000,
            "from_address": "Calle Real 123",
            "to_address": "Calle Real 111",
            "start": "2022-09-09T02:00:00",
            "finish": "2022-09-10T07:00:00",
        }
        trip4 = Trip(**external_data_4)

        self.trip1 = jsonable_encoder(trip1)
        self.trip2 = jsonable_encoder(trip2)
        self.trip3 = jsonable_encoder(trip3)
        self.trip4 = jsonable_encoder(trip4)


    def test_find_fare_avg(self):
        self.setUp()
        mongo_client = mongomock.MongoClient()
        mongo_client[DB_NAME]["trips"].insert_one(self.trip1)
        mongo_client[DB_NAME]["trips"].insert_one(self.trip2)

        assert service.find_fare_avg(mongo_client) == 750