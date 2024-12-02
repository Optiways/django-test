def period_overlap(p1_start, p1_end, p2_start, p2_end):
    return (min(p1_end, p2_end) - max(p1_start, p2_start)).days + 1 > 0
