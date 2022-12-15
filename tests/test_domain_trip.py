from src.domain.trip import Trip
from datetime import datetime
from fastapi.encoders import jsonable_encoder


class TestTripDomain:
    def test_create_trip_domain(self):
        start = datetime.now()
        finish = datetime.now()
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
            "start": start,
            "finish": finish,
        }
        trip1 = Trip(**external_data_1)
        trip1 = jsonable_encoder(trip1)

        assert trip1["_id"] == "1"
        assert trip1["passengerId"] == "066de609-b04a-4b30-b46c-32537c7f1f6e"
        assert trip1["driverId"] == "2320930329-b04a-4b30-b46c-fsdfwefwefw"
        assert trip1["from_latitude"] == -34.603683
        assert trip1["from_longitude"] == -58.381557
        assert trip1["to_latitude"] == -34.6175841
        assert trip1["to_longitude"] == -58.3682286
        assert trip1["subscription"] == "REGULAR"
        assert trip1["status"] == "TERMINATED"
        assert trip1["finalPrice"] == 500
        assert trip1["from_address"] == "Calle Falsa 123"
        assert trip1["to_address"] == "Calle Falsa 666"
        assert trip1["start"] == str(start).replace(" ", "T")
        assert trip1["finish"] == str(finish).replace(" ", "T")
