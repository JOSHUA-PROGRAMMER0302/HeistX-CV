def get_zone(cx, cy, zones):

    for zone_name, (x1, y1, x2, y2) in zones.items():

        if x1 < cx < x2 and y1 < cy < y2:
            return zone_name

    return "Unknown"