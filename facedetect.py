import pylwdrone
import sys
drone = pylwdrone.LWDrone()

for frame in drone.start_video_stream():
    sys.stdout.buffer.write(frame.frame_bytes)