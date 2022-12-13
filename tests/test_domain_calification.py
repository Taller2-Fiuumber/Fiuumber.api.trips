from src.domain.calification import Calification
from datetime import datetime, timedelta
from fastapi.encoders import jsonable_encoder

class TestCalificationDomain:
    def test_create_calification_domain(self):
        createdAt = datetime.now()
        updatedAt = datetime.now()
        external_data_1 = {
            "_id": "1",
            "passengerId": "5",
            "driverId": "6",
            "tripId": "100",
            "createdAt": createdAt,
            "updatedAt": updatedAt,
            "stars": 3,
            "comments": "Nice driver. Love the scene.",
            "reviewer": "PASSENGER",
        }
        calification1 = Calification(**external_data_1)
        calification1 = jsonable_encoder(calification1)

        assert calification1['_id'] == "1"
        assert calification1["passengerId"] == "5"
        assert calification1["driverId"] == "6"
        assert calification1["tripId"] == "100"
        assert calification1["createdAt"] == str(createdAt).replace(" ", "T")
        assert calification1["updatedAt"] == str(updatedAt).replace(" ", "T")
        assert calification1["stars"] == 3
        assert calification1["comments"] == "Nice driver. Love the scene."
        assert calification1["reviewer"] == "PASSENGER"
        

