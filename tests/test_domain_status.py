from src.domain.status import (
    Invalid,
    Canceled,
    Terminated,
    DriverArrived,
    DriverAssigned,
    InProgress,
    Requested,
    StatusFactory,
)


class TestStatusDomain:
    def test_invalid_status(self):
        status = Invalid()
        assert status.name() == "INVALID"
        assert status.next() == Invalid()
        assert status.cancel() == Invalid()

    def test_canceled_status(self):
        status = Canceled()
        assert status.name() == "CANCELED"
        assert status.next() == Canceled()
        assert status.cancel() == Canceled()

    def test_requested_status(self):
        status = Requested()
        assert status.name() == "REQUESTED"
        assert status.next() == DriverAssigned()
        assert status.cancel() == Canceled()

    def test_driver_assigned_status(self):
        status = DriverAssigned()
        assert status.name() == "DRIVER_ASSIGNED"
        assert status.next() == DriverArrived()
        assert status.cancel() == Canceled()

    def test_driver_arrived_status(self):
        status = DriverArrived()
        assert status.name() == "DRIVER_ARRIVED"
        assert status.next() == InProgress()
        assert status.cancel() == Canceled()

    def test_in_progress_status(self):
        status = InProgress()
        assert status.name() == "IN_PROGRESS"
        assert status.next() == Terminated()
        assert status.cancel() == Canceled()

    def test_terminated_status(self):
        status = Terminated()
        assert status.name() == "TERMINATED"
        assert status.next() == Terminated()
        assert status.cancel() == Terminated()

    def test_status_factory(self):
        invalid = "INVALID"
        canceled = "CANCELED"
        requested = "REQUESTED"
        driver_assigned = "DRIVER_ASSIGNED"
        driver_arrived = "DRIVER_ARRIVED"
        in_progress = "IN_PROGRESS"
        terminated = "TERMINATED"

        assert StatusFactory(invalid) == Invalid()
        assert StatusFactory(canceled) == Canceled()
        assert StatusFactory(requested) == Requested()
        assert StatusFactory(driver_assigned) == DriverAssigned()
        assert StatusFactory(driver_arrived) == DriverArrived()
        assert StatusFactory(in_progress) == InProgress()
        assert StatusFactory(terminated) == Terminated()
