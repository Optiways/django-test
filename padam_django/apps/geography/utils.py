def is_shifts_compatible(departure_shift_a, arrival_shift_a, departure_shift_b, arrival_shift_b):
    """Determine if the two shifts given in params do not overlap.
    :param departure_shift_a: Departure time of shift A
    :param departure_shift_b: Departure time of shift B
    :param arrival_shift_a: Arrival time of shift A
    :param arrival_shift_b: Arrival time of shift B
    :returns: shifts compatibility
    :rtype: bool
    """
    if departure_shift_a < arrival_shift_b < arrival_shift_a:
        return False
    if arrival_shift_b > arrival_shift_a > departure_shift_b:
        return False
    return True
