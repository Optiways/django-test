class BusOtherShiftsOverlapException(Exception):
    pass


class DriverOtherShiftsOverlapException(Exception):
    pass


class StopWouldOverlapBusOtherShifts(Exception):
    pass


class StopWouldOverlapDriverOtherShifts(Exception):
    pass
