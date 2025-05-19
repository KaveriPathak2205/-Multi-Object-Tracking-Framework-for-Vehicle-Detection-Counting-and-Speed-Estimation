# -Multi-Object-Tracking-Framework-for-Vehicle-Detection-Counting-and-Speed-Estimation
# Multi-Level Hybrid Vehicle Monitoring System (MHVMS)

MHVMS is a real-time system for vehicle detection, tracking, counting, and speed estimation using YOLOv8 and a Kalman Filter with Re-ID buffer. This solution is designed for traffic surveillance, smart city planning, and highway monitoring.

## Features
- Real-time vehicle detection with YOLOv8
- Kalman Filter-based object tracking with persistent IDs
- Re-identification buffer to prevent ID switches
- Bidirectional counting using virtual red/blue lines
- Speed estimation using inter-frame time
- Modular structure for easy extensibility

## Project Structure
MHVMS/
├── main.py
├── detector.py
├── tracker_module.py
├── utils/
│   ├── speed_estimator.py
│   └── line_logic.py
├── data/
│   └── test_video.mp4
├── output/
│   └── output_video.mp4
└── requirements.txt

## Run the Pipeline
```bash
python main.py
```

## Input Format
- MP4 video (e.g., `data/test_video.mp4`)
- Static camera preferred
- Horizontal vehicle motion for speed tracking

## Output
- Annotated video with tracking ID, bounding box
- Direction (left/right)
- Speed in km/h
- Logs printed to console:
```
Vehicle 3 | Dir: right | Speed: 42.12 km/h
Vehicle 4 | Dir: left | Speed: 37.45 km/h
```

## License
MIT

## Future Enhancements
- Replace simple Kalman with DeepSORT/ByteTrack
- Integrate dashboard using Streamlit
- Add anomaly detection for lane-jumping or over-speeding
