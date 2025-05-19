from ultralytics import YOLO
class YOLODetector:
    def __init__(self, model_path='yolov8s.pt'):
        self.model = YOLO(model_path)
        self.class_list = self.model.names

    def detect(self, frame):
        results = self.model(frame)[0]
        detections = []
        for box in results.boxes.data:
            x1, y1, x2, y2, conf, cls_id = box
            label = self.class_list[int(cls_id)]
            detections.append({
                "bbox": [int(x1), int(y1), int(x2 - x1), int(y2 - y1)],
                "class": int(cls_id),
                "conf": float(conf),
                "label": label
            })
        return detections