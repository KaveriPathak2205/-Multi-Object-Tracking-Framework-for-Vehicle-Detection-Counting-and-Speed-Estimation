import cv2
import csv
from detector import YOLODetector
from tracker_module import KalmanTracker
from utils.speed_estimator import estimate_speed
from utils.utils.line_logic import check_crossing
import os
import pandas as pd

video_path = 'C:\\Users\\utpal\\OneDrive\\Desktop\\Year III\\Sem 2\\Design Project\\MHVMS\\data\\datatest_video.mp4'
cap = cv2.VideoCapture(video_path)
fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

tracker = KalmanTracker()
detector = YOLODetector()
red_line_x = 400
blue_line_x = 700
offset = 10

id_frame_log = {}
crossed_ids = set()
counter_left = set()
counter_right = set()
detection_log = []

os.makedirs("output", exist_ok=True)
out = cv2.VideoWriter('output/output_video.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

while True:
    ret, frame = cap.read()
    if not ret:
        break

    detections = detector.detect(frame)
    tracks = tracker.update(detections, frame)

    for track in tracks:
        if not track['confirmed']:
            continue

        tid = track['track_id']
        x, y, w, h = track['bbox']
        label = track['label']
        cx = (x + x + w) // 2

        # Check if vehicle has already crossed to avoid multiple counting
        if tid not in id_frame_log:
            id_frame_log[tid] = [cx, cap.get(cv2.CAP_PROP_POS_FRAMES)]
        else:
            prev_cx, prev_frame = id_frame_log[tid]
            direction = check_crossing(cx, prev_cx, red_line_x, blue_line_x, offset)

            if direction:
                current_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)
                frame_diff = current_frame - prev_frame
                speed = estimate_speed(frame_diff, fps)

                track['speed'] = speed
                track['direction'] = direction

                log = {
                    'id': tid,
                    'class': label,
                    'direction': direction,
                    'speed': int(speed),
                    'frame': int(current_frame)
                }
                detection_log.append(log)

                if direction == "right" and tid not in counter_right:
                    counter_right.add(tid)
                elif direction == "left" and tid not in counter_left:
                    counter_left.add(tid)

                # Ensure unique counting
                crossed_ids.add(tid)

        speed_text = f"ID:{tid} {label}"
        if 'speed' in track:
            speed_value = int(track['speed'])
            direction = track.get('direction', '')
            speed_text += f" | {speed_value} km/h | {direction}"
            color = (0, 0, 255) if speed_value > 80 else (0, 255, 0)
        else:
            color = (0, 255, 0)

        cv2.rectangle(frame, (int(x), int(y)), (int(x + w), int(y + h)), color, 2)
        cv2.putText(frame, speed_text, (int(x), int(y - 5)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    # Line drawing and stats
    cv2.line(frame, (red_line_x, 0), (red_line_x, height), (0, 0, 255), 2)
    cv2.line(frame, (blue_line_x, 0), (blue_line_x, height), (255, 0, 0), 2)
    cv2.putText(frame, f"Right →: {len(counter_right)}", (40, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    cv2.putText(frame, f"← Left: {len(counter_left)}", (40, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

    out.write(frame)
    cv2.imshow("MHVMS", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
out.release()
cv2.destroyAllWindows()

# Save CSV log
if detection_log:
    df = pd.DataFrame(detection_log)
    df.to_csv("C:\\Users\\utpal\\OneDrive\\Desktop\\Year III\\Sem 2\\Design Project\\MHVMS\\output\\detection_log.csv", index=False)
    print("✅ CSV export done: output/detection_log.csv")
else:
    print("⚠ No detections to save in CSV.")
