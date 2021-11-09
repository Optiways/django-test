def overlap(r1: tuple, r2: tuple) -> bool:
    """Return true if the times ranges are overlapping"""
    latest_start = max(r1[0], r2[0])
    earliest_end = min(r1[1], r2[1])
    delta = (earliest_end - latest_start).days + 1
    return max(0, delta) != 0
