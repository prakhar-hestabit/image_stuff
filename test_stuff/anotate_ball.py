import cv2
import supervision as sv
from ultralytics import YOLO

model = YOLO("yolov8n.pt")
image = cv2.imread("/home/hestabit/PROJECTS/image-stuff/test_stuff/f_ball.jpg")
results = model(image)[0]
detections = sv.Detections.from_ultralytics(results)
detections = detections[detections.class_id == 0]

# Annotator
ellipse_annotator = sv.EllipseAnnotator(thickness = 10, color = sv.Color.RED)
triangle_annotator = sv.TriangleAnnotator(base = 50, height = 50, color=sv.Color.RED)
annotated_frame = triangle_annotator.annotate(
    scene=image.copy(),
    detections=detections
)
label_annotator = sv.LabelAnnotator()
labels = [
    model.model.names[class_id]
    for class_id
    in detections.class_id
]
annotated_image = triangle_annotator.annotate(
    scene=image, detections=detections)
annotated_image2 = ellipse_annotator.annotate(
    scene=annotated_image, detections=detections)

annotated_image = label_annotator.annotate(
    scene=annotated_image, detections=detections, labels=labels)
annotated_image2 = label_annotator.annotate(
    scene=annotated_image, detections=detections, labels=labels)

sv.plot_image(annotated_image)
# sv.plot_image(annotated_image2)