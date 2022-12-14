import mongomock
from mongomock import helpers
from mongomock import read_concern
from fastapi.encoders import jsonable_encoder
from src.domain.trip import Trip
import src.services.trips as service
from datetime import datetime, timedelta


from os import environ
# DB_NAME = environ["DB_NAME"]
DB_NAME = "Fiuumber"


class TestTrips:
    def setUp(self):
        external_data_1 = {
            "id": "1",
            "passengerId": "10",
            "driverId": "50",
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
            "finish": datetime.now()
        }
        trip1 = Trip(**external_data_1)

        external_data_2 = {
            "id": "2",
            "passengerId": "10",
            "driverId": "50",
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
            "finish": datetime.now()
        }
        trip2 = Trip(**external_data_2)

        external_data_3 = {
            "id": "3",
            "passengerId": "5-b04a-4b30-b46c-32537c7f1f6e",
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
            "finish": datetime.now()
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
            "finish": datetime.now()
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
            "finish": datetime.now()
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
            "finish": datetime.now()
        }

        trip6 = Trip(**external_data_6)


        self.trip1 = jsonable_encoder(trip1)
        self.trip2 = jsonable_encoder(trip2)
        self.trip3 = jsonable_encoder(trip3)
        self.trip4 = jsonable_encoder(trip4)
        self.trip5 = jsonable_encoder(trip5)
        self.trip6 = jsonable_encoder(trip6)

    def test_create_trip(self):
        self.setUp()
        mongo_client = mongomock.MongoClient()

        result = self.trip1 
        result['_id'] = 1
        assert service.create_trip(mongo_client, self.trip1) == result

    def test_list_trips(self):
        self.setUp()
        mongo_client = mongomock.MongoClient()

        mongo_client[DB_NAME]["trips"].insert_one(self.trip1)
        mongo_client[DB_NAME]["trips"].insert_one(self.trip2)
        mongo_client[DB_NAME]["trips"].insert_one(self.trip3)

        assert service.list_trips(mongo_client) == [self.trip1, self.trip2, self.trip3]

    def test_find_trip_by_id(self):
        self.setUp()
        mongo_client = mongomock.MongoClient()

        mongo_client[DB_NAME]["trips"].insert_one(self.trip1)
        mongo_client[DB_NAME]["trips"].insert_one(self.trip2)

        assert service.find_trip_by_id('1', mongo_client) == self.trip1

    def test_find_trip_by_id_is_none(self):
        self.setUp()
        mongo_client = mongomock.MongoClient()

        mongo_client[DB_NAME]["trips"].insert_one(self.trip1)
        mongo_client[DB_NAME]["trips"].insert_one(self.trip2)

        assert service.find_trip_by_id('1000', mongo_client) == None


    def test_duration_by_id_not_terminated_trip(self):
        self.setUp()
        mongo_client = mongomock.MongoClient()

        mongo_client[DB_NAME]["trips"].insert_one(self.trip2)

        assert service.duration_by_id('2', mongo_client) == -1

    
    # TEST QUE NO PUEDO TESTEAR POR EL TEMA DE LAS FECHAS: 

    # def test_duration_by_id(self):
    #     self.setUp()
    #     mongo_client = mongomock.MongoClient()

    #     mongo_client[DB_NAME]["trips"].insert_one(self.trip1)

    #     assert service.duration_by_id('1', mongo_client) == 

    def test_update_trip(self):
        self.setUp()
        mongo_client = mongomock.MongoClient()

        mongo_client[DB_NAME]["trips"].insert_one(self.trip1)
        modified = self.trip1 
        modified['finalPrice'] = 10 
        assert service.update_trip('1', mongo_client, modified) == modified

    def test_delete_trip(self):
        self.setUp()
        mongo_client = mongomock.MongoClient()

        mongo_client[DB_NAME]["trips"].insert_one(self.trip1)
        assert service.delete_trip('1', mongo_client) ==  1

    def test_delete_all_trips(self):
        self.setUp()
        mongo_client = mongomock.MongoClient()

        mongo_client[DB_NAME]["trips"].insert_one(self.trip1)
        mongo_client[DB_NAME]["trips"].insert_one(self.trip2)
        mongo_client[DB_NAME]["trips"].insert_one(self.trip3)
        assert service.delete_all_trip(mongo_client) ==  3

    def test_find_trip_status(self):
        self.setUp()
        mongo_client = mongomock.MongoClient()

        mongo_client[DB_NAME]["trips"].insert_one(self.trip1)
        assert service.find_trip_status('1', mongo_client) ==  "TERMINATED"



    # COMO TESTEAR EXCEPCIONES ?

    # def test_assign_driver_not_requested_trip(self):
    #     self.setUp()
    #     mongo_client = mongomock.MongoClient()

    #     mongo_client[DB_NAME]["trips"].insert_one(self.trip1)
    #     with pytest.assertRaises(Exception):
    #         service.assign_driver('1', '20', mongo_client)
    #     # assert service.assign_driver('1', '20', mongo_client)

    def test_assign_driver(self):
        self.setUp()
        mongo_client = mongomock.MongoClient()

        mongo_client[DB_NAME]["trips"].insert_one(self.trip2)
        result = self.trip2
        result['driverId'] = '2'
        result['status'] = "DRIVER_ASSIGNED"
        assert service.assign_driver("2", "2", mongo_client) ==  result

    def test_trips_by_passenger_id(self):
        self.setUp()
        mongo_client = mongomock.MongoClient()

        mongo_client[DB_NAME]["trips"].insert_one(self.trip1)
        mongo_client[DB_NAME]["trips"].insert_one(self.trip2)
        mongo_client[DB_NAME]["trips"].insert_one(self.trip3)
        assert service.trips_by_passenger_id("10", 0, 5, mongo_client) ==  [self.trip1, self.trip2]

    def test_trips_by_driver_id(self):
        self.setUp()
        mongo_client = mongomock.MongoClient()

        mongo_client[DB_NAME]["trips"].insert_one(self.trip1)
        mongo_client[DB_NAME]["trips"].insert_one(self.trip2)
        mongo_client[DB_NAME]["trips"].insert_one(self.trip3)
        assert service.trips_by_driver_id("50", 0, 5, mongo_client) ==  [self.trip1, self.trip2]