def estimate_speed(frame_diff, fps, distance_m=10):
    time_s = frame_diff / fps
    speed_mps = distance_m / time_s
    return round(speed_mps * 3.6, 2)  #Km/hr