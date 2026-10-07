import cv2
import time

from tracker import track

from behavior_engine import (
    update_track,
    get_total_movement,
    get_path,
    dwell_time,
    is_loitering,
    is_running,
    loitering_confidence,
    should_alert
)

from risk_engine import calculate_risk
from event_manager import save_event

cap = cv2.VideoCapture("videos/test.mp4")

event_count = 0
loitering_count = 0
running_count = 0

prev_time = time.time()

while True:

    ret, frame = cap.read()

    if not ret:
        break

    results = track(frame)

    annotated_frame = frame.copy()

    boxes = results[0].boxes

    person_count = 0

    current_time = time.time()

    fps = int(
        1 / max(
            current_time - prev_time,
            0.0001
        )
    )

    prev_time = current_time

    for box in boxes:

        if box.id is None:
            continue

        person_count += 1

        track_id = int(box.id.item())

        x1, y1, x2, y2 = map(
            int,
            box.xyxy[0]
        )

        cx = int((x1 + x2) / 2)
        cy = int((y1 + y2) / 2)

        update_track(
            track_id,
            cx,
            cy
        )

        movement = int(
            get_total_movement(track_id)
        )

        dwell = int(
            dwell_time(track_id)
        )

        path = get_path(track_id)

        for i in range(1, len(path)):

            cv2.line(
                annotated_frame,
                path[i - 1],
                path[i],
                (0, 255, 255),
                2
            )

        status = "Normal"

        if is_loitering(track_id):
            status = "Loitering"

        elif is_running(track_id):
            status = "Running"

        risk_score, risk_level = calculate_risk(
            loitering=is_loitering(track_id),
            running=is_running(track_id)
        )

        if risk_level == "HIGH":
            risk_color = (0, 0, 255)

        elif risk_level == "MEDIUM":
            risk_color = (0, 165, 255)

        else:
            risk_color = (0, 255, 0)

        cv2.rectangle(
            annotated_frame,
            (x1, y1),
            (x2, y2),
            (255, 0, 0),
            2
        )

        cv2.putText(
            annotated_frame,
            f"Risk:{risk_level}",
            (x1, y1 - 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            risk_color,
            2
        )

        cv2.putText(
            annotated_frame,
            f"ID:{track_id}",
            (x1, y1 - 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255,255,255),
            2
        )

        cv2.putText(
            annotated_frame,
            f"Status:{status}",
            (x1, y2 + 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0,255,0),
            2
        )

        cv2.putText(
            annotated_frame,
            f"Move:{movement}",
            (x1, y2 + 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255,255,0),
            2
        )

        cv2.putText(
            annotated_frame,
            f"Dwell:{dwell}s",
            (x1, y2 + 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255,255,255),
            2
        )

        if is_loitering(track_id):

            confidence = loitering_confidence(
                track_id
            )

            cv2.putText(
                annotated_frame,
                f"Loitering {confidence}%",
                (x1, y1 - 85),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0,0,255),
                2
            )

        if should_alert(track_id):

            if (
                is_loitering(track_id)
                or
                is_running(track_id)
            ):

                event_count += 1

                if status == "Loitering":
                    loitering_count += 1

                if status == "Running":
                    running_count += 1

                screenshot_path = (
                    f"events/screenshots/"
                    f"{track_id}_{status}.jpg"
                )

                cv2.imwrite(
                    screenshot_path,
                    frame
                )

                event = {

                    "person_id": track_id,

                    "behavior": status,

                    "risk_score": risk_score,

                    "risk_level": risk_level,

                    "movement": movement,

                    "dwell_time": dwell,

                    "timestamp": time.strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),

                    "screenshot": screenshot_path
                }

                save_event(event)

    cv2.rectangle(
        annotated_frame,
        (10, 10),
        (350, 190),
        (35, 35, 35),
        -1
    )

    cv2.putText(
        annotated_frame,
        "SentinelAI V3",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        (255,255,255),
        2
    )

    cv2.putText(
        annotated_frame,
        f"Persons : {person_count}",
        (20, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255,255,255),
        2
    )

    cv2.putText(
        annotated_frame,
        f"Events  : {event_count}",
        (20, 110),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255,255,255),
        2
    )

    cv2.putText(
        annotated_frame,
        f"Loitering : {loitering_count}",
        (20, 140),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0,165,255),
        2
    )

    cv2.putText(
        annotated_frame,
        f"Running : {running_count}",
        (20, 170),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0,255,255),
        2
    )

    cv2.putText(
        annotated_frame,
        f"FPS:{fps}",
        (250, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0,255,0),
        2
    )

    cv2.imshow(
        "SentinelAI V3",
        annotated_frame
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()