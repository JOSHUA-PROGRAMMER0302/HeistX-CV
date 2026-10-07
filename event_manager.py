import json
import os
from datetime import datetime

os.makedirs(
    "events/json",
    exist_ok=True
)

os.makedirs(
    "events/screenshots",
    exist_ok=True
)

def save_event(event):

    filename = (
        datetime.now()
        .strftime("%Y%m%d_%H%M%S")
        + ".json"
    )

    path = f"events/json/{filename}"

    with open(path, "w") as f:

        json.dump(
            event,
            f,
            indent=4
        )