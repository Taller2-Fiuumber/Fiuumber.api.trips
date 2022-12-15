import mongomock
from fastapi.encoders import jsonable_encoder
from src.domain.trip import Trip
import src.services.trips_metrics as service
from datetime import datetime


from os import environ

DB_NAME = environ["DB_NAME"] if "DB_NAME" in environ else "Fiuumber"


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
            "status": "TERMINATED",
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
            "status": "TERMINATED",
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
            "status": "TERMINATED",
            "finalPrice": 1000,
            "from_address": "Calle Real 123",
            "to_address": "Calle Real 111",
            "start": datetime.now(),
            "finish": datetime.now(),
        }
        trip4 = Trip(**external_data_4)

        self.trip1 = jsonable_encoder(trip1)
        self.trip2 = jsonable_encoder(trip2)
        self.trip3 = jsonable_encoder(trip3)
        self.trip4 = jsonable_encoder(trip4)

    # def test_get_trip_duration_min(self):
    #     self.setUp()
    #     mongo_client = mongomock.MongoClient()

    #     mongo_client[DB_NAME]["trips"].insert_one(self.trip1)
    #     mongo_client[DB_NAME]["trips"].insert_one(self.trip2)
    #     mongo_client[DB_NAME]["trips"].insert_one(self.trip3)
    #     mongo_client[DB_NAME]["trips"].insert_one(self.trip4)

    #     print("_____type_______", type(datetime.today().replace(hour=1, minute=0, second=0, microsecond=0)))
    #     print("_____datetime_______", datetime.today().replace(hour=1, minute=0, second=0, microsecond=0))
    #     print("____Start____", self.trip1['start'])
    #     assert service.get_trip_duration_min(mongo_client) == 750

    def test_count_trips_by_status(self):
        self.setUp()
        mongo_client = mongomock.MongoClient()

        mongo_client[DB_NAME]["trips"].insert_one(self.trip1)
        mongo_client[DB_NAME]["trips"].insert_one(self.trip2)
        mongo_client[DB_NAME]["trips"].insert_one(self.trip3)
        mongo_client[DB_NAME]["trips"].insert_one(self.trip4)
        assert service.count_trips_by_status("TERMINATED", mongo_client) == 4

    def test_count_trips(self):
        self.setUp()
        mongo_client = mongomock.MongoClient()

        mongo_client[DB_NAME]["trips"].insert_one(self.trip1)
        mongo_client[DB_NAME]["trips"].insert_one(self.trip2)
        mongo_client[DB_NAME]["trips"].insert_one(self.trip3)
        mongo_client[DB_NAME]["trips"].insert_one(self.trip4)
        assert service.count_trips(mongo_client) == 4

    def test_count_trips_new_count_today(self):
        self.setUp()
        mongo_client = mongomock.MongoClient()

        mongo_client[DB_NAME]["trips"].insert_one(self.trip1)
        assert service.count_trips_new_count_today(mongo_client) == 0

    def test_count_trips_new_countlast_n_days(self):
        self.setUp()
        mongo_client = mongomock.MongoClient()

        mongo_client[DB_NAME]["trips"].insert_one(self.trip1)
        assert service.count_trips_new_countlast_n_days(1, mongo_client) == 0

    def test_count_trips_new_countlast_n_days_range(self):
        self.setUp()
        mongo_client = mongomock.MongoClient()

        assert service.count_trips_new_countlast_n_days_range(1, mongo_client) == []

    def test_count_trips_new_count_last_n_months(self):
        self.setUp()
        mongo_client = mongomock.MongoClient()
        assert service.count_trips_new_count_last_n_months(1, mongo_client) == 0

    def test_count_trips_new_count_last_n_months_range(self):
        self.setUp()
        mongo_client = mongomock.MongoClient()
        assert service.count_trips_new_count_last_n_months_range(1, mongo_client) == []

    def test_count_trips_new_count_last_n_years_range(self):
        self.setUp()
        mongo_client = mongomock.MongoClient()
        assert service.count_trips_new_count_last_n_years_range(1, mongo_client) == []

    def test_count_trips_new_count_last_n_years_and_m_months_range(self):
        self.setUp()
        mongo_client = mongomock.MongoClient()
        assert (
            service.count_trips_new_count_last_n_years_and_m_months_range(
                1, 1, mongo_client
            )
            == []
        )

    def test_count_trips_new_count_last_n_years(self):
        self.setUp()
        mongo_client = mongomock.MongoClient()
        assert service.count_trips_new_count_last_n_years(10, mongo_client) == 0

    def test_count_trips_duration_last_n_years_range(self):
        self.setUp()
        mongo_client = mongomock.MongoClient()
        assert service.count_trips_duration_last_n_years_range(10, mongo_client) == []
