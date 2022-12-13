# import mongomock
# from mongomock import helpers
# from mongomock import read_concern
# from fastapi.encoders import jsonable_encoder
# from src.domain.fare_rule import FareRule
# import src.services.fare as service
# from datetime import datetime, timedelta


# from os import environ
# # DB_NAME = environ["DB_NAME"]
# DB_NAME = "Fiuumber"

# class TestFareService:
#     # def setUp(self):
#     #     external_data_1 = {
#     #         "id": "1",
#     #         "passengerId": "10",
#     #         "driverId": "50",
#     #         "from_latitude": -34.603683,
#     #         "from_longitude": -58.381557,
#     #         "to_latitude": -34.6175841,
#     #         "to_longitude": -58.3682286,
#     #         "subscription": "REGULAR",
#     #         "status": "TERMINATED",
#     #         "finalPrice": 500,
#     #         "from_address": "Calle Falsa 123",
#     #         "to_address": "Calle Falsa 666",
#     #         "start": datetime.now(),
#     #         "finish": datetime.now()
#     #     }
#     #     fare_rule1 = FareRule(**external_data_1)

#     #     external_data_2 = {
#     #         "id": "2",
#     #         "passengerId": "10",
#     #         "driverId": "50",
#     #         "from_latitude": -39.603683,
#     #         "from_longitude": -50.381557,
#     #         "to_latitude": -31.6175841,
#     #         "to_longitude": -55.3682286,
#     #         "subscription": "REGULAR",
#     #         "status": "REQUESTED",
#     #         "finalPrice": 1000,
#     #         "from_address": "Calle Real 123",
#     #         "to_address": "Calle Real 111",
#     #         "start": datetime.now(),
#     #         "finish": datetime.now()
#     #     }
#     #     fare_rule2 = FareRule(**external_data_2)
    
#     #     self.fare_rule1 = jsonable_encoder(fare_rule1)
#     #     self.fare_rule2 = jsonable_encoder(fare_rule2)
    
#     def test_get_trip_fare(self):
#         assert service.get_trip_fare(-39.603683, -31.6175841, -50.381557, -55.3682286) == 40067.74