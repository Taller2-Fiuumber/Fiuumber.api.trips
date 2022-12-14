from src.domain.fare_rule import FareRule
from datetime import datetime
from fastapi.encoders import jsonable_encoder


class TestFareRuleDomain:
    def test_create_fare_rule_domain(self):
        createdAt = datetime(2022, 9, 9, 2)
        updatedAt = datetime(2022, 9, 9, 2)
        external_data_1 = {
            "selected": False,
            "createdAt": createdAt,
            "updatedAt": updatedAt,
            "minimum": 200.0,
            "duration": 5,
            "distance": 6,
            "dailyTripAmountDriver": 0.7,
            "dailyTripAmountPassenger": -0.7,
            "monthlyTripAmountDrive": 0.8,
            "monthlyTripAmountPassenger": -0.8,
            "seniorityDriver": 0.5,
            "seniorityPassenger": -0.25,
            "recentTripAmount": -0.2,
        }
        fare_rule = FareRule(**external_data_1)
        fare_rule = jsonable_encoder(fare_rule)

        assert fare_rule["selected"] is False
        assert fare_rule["createdAt"] == str(createdAt).replace(" ", "T")
        assert fare_rule["updatedAt"] == str(updatedAt).replace(" ", "T")
        assert fare_rule["minimum"] == 200.0
        assert fare_rule["duration"] == 5
        assert fare_rule["distance"] == 6
        assert fare_rule["dailyTripAmountDriver"] == 0.7
        assert fare_rule["dailyTripAmountPassenger"] == -0.7
        assert fare_rule["monthlyTripAmountDrive"] == 0.8
        assert fare_rule["monthlyTripAmountPassenger"] == -0.8
        assert fare_rule["seniorityDriver"] == 0.5
        assert fare_rule["seniorityPassenger"] == -0.25
        assert fare_rule["recentTripAmount"] == -0.2
