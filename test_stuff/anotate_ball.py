import supervision as sv
from ultralytics import YOLO
import numpy as np
import logging

logging.basicConfig(level = logging.DEBUG,
                    format = '%(message)s',
                    handlers = [
                        logging.FileHandler("cords_xyxy.log"),  # Log to a file
                    ])


model = YOLO("/home/hestabit/PROJECTS/image-stuff/test_stuff/2best.pt")
tracker = sv.ByteTrack()

bounding_box_annotator = sv.BoundingBoxAnnotator()
label_annotator = sv.LabelAnnotator()

def callback(frame: np.ndarray, index: int) -> np.ndarray:
    results = model(frame)[0]
    detections = sv.Detections.from_ultralytics(results)
    detections = tracker.update_with_detections(detections)

    labels = [f"#{tracker_id}" for tracker_id in detections.tracker_id]
    logging.info(f"{detections.xyxy}")
    annotated_frame = bounding_box_annotator.annotate(
        scene=frame.copy(), detections=detections)
    annotated_frame = label_annotator.annotate(
        scene=annotated_frame, detections=detections, labels=labels)
    return annotated_frame

sv.process_video(
    source_path="/home/hestabit/PROJECTS/image-stuff/test_stuff/recorded_video_0.avi",
    target_path="/home/hestabit/PROJECTS/image-stuff/test_stuff/track_result_3.mp4",
    callback=callback
)