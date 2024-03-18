import cv2
import numpy as np
import pylwdrone
from ffpyplayer.player import MediaPlayer
import sys
import threading

def display_video_stream():
    drone = pylwdrone.LWDrone()
    drone.set_time()
    window_name = 'Drone Video Stream'
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

    player = None
    for packet in drone.start_video_stream():
        try:
            if player is None:
                player = MediaPlayer('pipe:0', ff_opts={'format':'rawvideo', 'pix_fmt':'bgr24'})
            frame, val = player.get_frame()
            if val == 'eof':
                break
            if frame is not None:
                img, _ = frame
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert frame to RGB format
                cv2.imshow(window_name, img)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        except Exception as e:
            print('An error occurred:', e, file=sys.stderr)
            break

    cv2.destroyAllWindows()
    drone.stop_video_stream()

# Create and start a new thread for displaying the video stream
display_thread = threading.Thread(target=display_video_stream)
display_thread.start()
