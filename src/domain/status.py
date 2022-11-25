class Status:
    def name(self):
        pass

    def next(self):
        pass

    def cancel(self):
        pass

    def __eq__(self, other):
        return self.name() == other.name()


class Invalid(Status):
    def name(self):
        return "INVALID"

    def next(self):
        return Invalid()

    def cancel(self):
        return Invalid()


class Canceled(Status):
    def name(self):
        return "CANCELED"

    def next(self):
        return Canceled()

    def cancel(self):
        return Canceled()


class Requested(Status):
    def name(self):
        return "REQUESTED"

    def next(self):
        return DriverAssigned()

    def cancel(self):
        return Canceled()


class DriverAssigned(Status):
    def name(self):
        return "DRIVER_ASSIGNED"

    def next(self):
        return DriverArrived()

    def cancel(self):
        return Canceled()


class DriverArrived(Status):
    def name(self):
        return "DRIVER_ARRIVED"

    def next(self):
        return InProgress()

    def cancel(self):
        return Canceled()


class InProgress(Status):
    def name(self):
        return "IN_PROGRESS"

    def next(self):
        return Terminated()

    def cancel(self):
        return InProgress()


class Terminated(Status):
    def name(self):
        return "TERMINATED"

    def next(self):
        return Terminated()

    def cancel(self):
        return Terminated()


def StatusFactory(name):
    if name == Requested().name():
        return Requested()
    elif name == DriverAssigned().name():
        return DriverAssigned()
    elif name == DriverArrived().name():
        return DriverArrived()
    elif name == InProgress().name():
        return InProgress()
    elif name == Terminated().name():
        return Terminated()
    elif name == Canceled().name():
        return Canceled()
    else:
        return Invalid()
