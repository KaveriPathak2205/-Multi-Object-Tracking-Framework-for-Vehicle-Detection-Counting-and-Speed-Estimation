import numpy as np
from filterpy.kalman import KalmanFilter

class Track:
    def __init__(self, id, bbox, label):
        self.track_id = id
        self.label = label
        self.kf = KalmanFilter(dim_x=7, dim_z=4)
        self.kf.F = np.array([[1, 0, 0, 0, 1, 0, 0],
                              [0, 1, 0, 0, 0, 1, 0],
                              [0, 0, 1, 0, 0, 0, 1],
                              [0, 0, 0, 1, 0, 0, 0],
                              [0, 0, 0, 0, 1, 0, 0],
                              [0, 0, 0, 0, 0, 1, 0],
                              [0, 0, 0, 0, 0, 0, 1]])
        self.kf.H = np.array([[1, 0, 0, 0, 0, 0, 0],
                              [0, 1, 0, 0, 0, 0, 0],
                              [0, 0, 1, 0, 0, 0, 0],
                              [0, 0, 0, 1, 0, 0, 0]])
        self.kf.x[:4] = np.array([[bbox[0]], [bbox[1]], [bbox[2]], [bbox[3]]])
        self.bbox = bbox
        self.age = 0
        self.hits = 1
        self.time_since_update = 0

    def predict(self):
        self.kf.predict()
        self.age += 1
        if self.time_since_update > 0:
            self.hits = 0
        self.time_since_update += 1
        self.bbox = self.kf.x[:4].reshape(-1)
        return self.bbox

    def update(self, bbox):
        self.kf.update(np.array([[bbox[0]], [bbox[1]], [bbox[2]], [bbox[3]]]))
        self.bbox = bbox
        self.time_since_update = 0
        self.hits += 1

class KalmanTracker:
    def __init__(self):
        self.tracks = []
        self.next_id = 0

    def update(self, detections, frame):
        updated_tracks = []
        for t in self.tracks:
            t.predict()

        for det in detections:
            x, y, w, h = det['bbox']
            label = det['label']
            matched = False
            for t in self.tracks:
                if t.time_since_update < 1 and np.linalg.norm(np.array(t.bbox[:2]) - np.array([x, y])) < 30:
                    t.update([x, y, x + w, y + h])
                    updated_tracks.append({"track_id": t.track_id, "bbox": [x, y, w, h], "confirmed": True, "label": t.label})
                    matched = True
                    break
            if not matched:
                new_track = Track(self.next_id, [x, y, x + w, y + h], label)
                self.tracks.append(new_track)
                updated_tracks.append({"track_id": self.next_id, "bbox": [x, y, w, h], "confirmed": True, "label": label})
                self.next_id += 1

        return updated_tracks
