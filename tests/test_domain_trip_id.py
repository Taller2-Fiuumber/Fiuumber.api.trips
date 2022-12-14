from src.domain.trip_id import TripId
from fastapi.encoders import jsonable_encoder


class TestTripIdDomain:
    def test_create_trip_id_domain(self):
        external_data_1 = {"trip_id": "15576e35-390a-478b-bd05-0572c023bdee"}
        trip_id = TripId(**external_data_1)
        trip_id = jsonable_encoder(trip_id)

        assert trip_id["trip_id"] == "15576e35-390a-478b-bd05-0572c023bdee"
