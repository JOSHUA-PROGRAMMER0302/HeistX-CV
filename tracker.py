from ultralytics import YOLO

model = YOLO("yolov8n.pt")

def track(frame):

    results = model.track(
        frame,
        persist=True,
        tracker="bytetrack.yaml",
        classes=[0]
    )

    return results