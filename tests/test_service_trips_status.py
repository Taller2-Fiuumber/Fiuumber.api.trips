import mongomock
from fastapi.encoders import jsonable_encoder
from src.domain.trip import Trip
import src.services.trips_status as service
from datetime import datetime


from os import environ

DB_NAME = environ["DB_NAME"] if "DB_NAME" in environ else "fiuumber"


class TestServiceTripStatus:
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
            "start": datetime.now(),
            "finish": datetime.now(),
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
            "status": "REQUESTED",
            "finalPrice": 1000,
            "from_address": "Calle Real 123",
            "to_address": "Calle Real 111",
            "start": datetime.now(),
            "finish": datetime.now(),
        }
        trip2 = Trip(**external_data_2)

        external_data_3 = {
            "id": "3",
            "passengerId": "0771de609-b04a-4b30-b46c-32537c7f1f6e",
            "driverId": "22209330329-b04a-4b30-b46c-fsdfwefwefw",
            "from_latitude": -19.603683,
            "from_longitude": -70.381557,
            "to_latitude": -32.6175841,
            "to_longitude": -54.3682286,
            "subscription": "REGULAR",
            "status": "DRIVER_ASSIGNED",
            "finalPrice": 1000,
            "from_address": "Calle Real 123",
            "to_address": "Calle Real 111",
            "start": datetime.now(),
            "finish": datetime.now(),
        }
        trip3 = Trip(**external_data_3)

        external_data_4 = {
            "id": "4",
            "passengerId": "087de609-b04a-4b30-b46c-32537c7f1f6e",
            "driverId": "22202930329-b04a-4b30-b46c-fsdfwefwefw",
            "from_latitude": -39.603683,
            "from_longitude": -50.381557,
            "to_latitude": -31.6175841,
            "to_longitude": -55.3682286,
            "subscription": "REGULAR",
            "status": "IN_PROGRESS",
            "finalPrice": 1000,
            "from_address": "Calle Real 123",
            "to_address": "Calle Real 111",
            "start": datetime.now(),
            "finish": datetime.now(),
        }
        trip4 = Trip(**external_data_4)

        external_data_5 = {
            "id": "5",
            "passengerId": "087de609-b04a-4b30-b46c-32537c7f1f6e",
            "driverId": "22202930329-b04a-4b30-b46c-fsdfwefwefw",
            "from_latitude": -39.603683,
            "from_longitude": -50.381557,
            "to_latitude": -31.6175841,
            "to_longitude": -55.3682286,
            "subscription": "REGULAR",
            "status": "DRIVER_ARRIVED",
            "finalPrice": 1000,
            "from_address": "Calle Real 123",
            "to_address": "Calle Real 111",
            "start": datetime.now(),
            "finish": datetime.now(),
        }

        trip5 = Trip(**external_data_5)
        external_data_6 = {
            "id": "6",
            "passengerId": "087de609-b04a-4b30-b46c-32537c7f1f6e",
            "driverId": "22202930329-b04a-4b30-b46c-fsdfwefwefw",
            "from_latitude": -39.603683,
            "from_longitude": -50.381557,
            "to_latitude": -31.6175841,
            "to_longitude": -55.3682286,
            "subscription": "REGULAR",
            "status": "INVALID",
            "finalPrice": 1000,
            "from_address": "Calle Real 123",
            "to_address": "Calle Real 111",
            "start": datetime.now(),
            "finish": datetime.now(),
        }

        trip6 = Trip(**external_data_6)

        self.trip1 = jsonable_encoder(trip1)
        self.trip2 = jsonable_encoder(trip2)
        self.trip3 = jsonable_encoder(trip3)
        self.trip4 = jsonable_encoder(trip4)
        self.trip5 = jsonable_encoder(trip5)
        self.trip6 = jsonable_encoder(trip6)

    def test_find_trip_status(self):
        self.setUp()
        mongo_client = mongomock.MongoClient()

        mongo_client[DB_NAME]["trips"].insert_one(self.trip1)

        assert service.find_trip_status("1", mongo_client) == "TERMINATED"

    def test_find_trip_status_is_none(self):
        self.setUp()
        mongo_client = mongomock.MongoClient()
        assert service.find_trip_status("80", mongo_client) is None

    def test_update_trip_status(self):
        self.setUp()
        mongo_client = mongomock.MongoClient()

        mongo_client[DB_NAME]["trips"].insert_one(self.trip2)
        result = self.trip2
        result["status"] = "DRIVER_ASSIGNED"
        assert (
            service.update_trip_status("2", mongo_client, "DRIVER_ASSIGNED") == result
        )

    def test_update_trip_status_is_none(self):
        self.setUp()
        mongo_client = mongomock.MongoClient()
        assert service.update_trip_status("90", mongo_client, "DRIVER_ASSIGNED") is None

    def test_update_trip_to_next_status_driver_assigned(self):
        self.setUp()
        mongo_client = mongomock.MongoClient()

        mongo_client[DB_NAME]["trips"].insert_one(self.trip3)
        assert (
            service.update_trip_to_next_status("3", mongo_client)["status"]
            == "DRIVER_ARRIVED"
        )

    def test_update_trip_to_next_status_driver_arrived(self):
        self.setUp()
        mongo_client = mongomock.MongoClient()

        mongo_client[DB_NAME]["trips"].insert_one(self.trip5)
        assert (
            service.update_trip_to_next_status("5", mongo_client)["status"]
            == "IN_PROGRESS"
        )

    def test_update_trip_to_next_status_in_progress(self):
        self.setUp()
        mongo_client = mongomock.MongoClient()

        mongo_client[DB_NAME]["trips"].insert_one(self.trip4)
        assert (
            service.update_trip_to_next_status("4", mongo_client)["status"]
            == "TERMINATED"
        )

    def test_update_trip_to_next_status_is_none(self):
        self.setUp()
        mongo_client = mongomock.MongoClient()
        assert service.update_trip_to_next_status("114", mongo_client) is None

    def test_update_trip_to_next_status_invalid(self):
        self.setUp()
        mongo_client = mongomock.MongoClient()

        mongo_client[DB_NAME]["trips"].insert_one(self.trip6)
        assert (
            service.update_trip_to_next_status("6", mongo_client)["status"] == "INVALID"
        )

    def test_cancel_trip_is_none(self):
        self.setUp()
        mongo_client = mongomock.MongoClient()

        assert service.cancel_trip("60", mongo_client) is None

    def test_cancel_trip_driver_assigned(self):
        self.setUp()
        mongo_client = mongomock.MongoClient()

        mongo_client[DB_NAME]["trips"].insert_one(self.trip3)

        assert service.cancel_trip("3", mongo_client)["status"] == "CANCELED"
