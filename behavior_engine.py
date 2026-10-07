from collections import defaultdict
import math
import time

track_history = defaultdict(list)
track_paths = defaultdict(list)

first_seen = {}
last_alert = {}

def update_track(track_id, x, y):

    current = time.time()

    if track_id not in first_seen:
        first_seen[track_id] = current

    track_history[track_id].append(
        (x, y, current)
    )

    track_paths[track_id].append(
        (x, y)
    )

    if len(track_history[track_id]) > 200:
        track_history[track_id].pop(0)

    if len(track_paths[track_id]) > 50:
        track_paths[track_id].pop(0)


def get_path(track_id):
    return track_paths[track_id]


def get_total_movement(track_id):

    pts = track_history[track_id]

    if len(pts) < 2:
        return 0

    total = 0

    for i in range(1, len(pts)):

        x1, y1, _ = pts[i - 1]
        x2, y2, _ = pts[i]

        total += math.sqrt(
            (x2 - x1) ** 2 +
            (y2 - y1) ** 2
        )

    return total


def dwell_time(track_id):

    if track_id not in first_seen:
        return 0

    return time.time() - first_seen[track_id]


def is_loitering(track_id):

    movement = get_total_movement(track_id)
    duration = dwell_time(track_id)

    return (
        duration > 10
        and
        movement < 100
    )


def is_running(track_id):

    movement = get_total_movement(track_id)

    return movement > 1200


def loitering_confidence(track_id):

    movement = get_total_movement(track_id)

    confidence = max(
        0,
        min(
            100,
            int(100 - movement / 2)
        )
    )

    return confidence


def should_alert(track_id, cooldown=30):

    current = time.time()

    if track_id not in last_alert:
        last_alert[track_id] = 0

    if current - last_alert[track_id] > cooldown:

        last_alert[track_id] = current
        return True

    return False