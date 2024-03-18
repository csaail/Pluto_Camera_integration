import cv2
import numpy as np
import pylwdrone
import ffmpeg
import sys
import threading

# Function to display the video stream from the drone
def display_video_stream():
    # Initialize the drone object
    drone = pylwdrone.LWDrone()
    # Set the time for the drone
    drone.set_time()
    # Define the window name for displaying the video stream
    window_name = 'Drone Video Stream'
    # Create a named window for the video stream
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

    # Iterate over the video stream packets received from the drone
    for packet in drone.start_video_stream():
        # Use ffmpeg to decode the video packet and convert it to a numpy array
        out, _ = (
            ffmpeg.input('pipe:0')
            .output('pipe:', format='rawvideo', pix_fmt='bgr24')
            .run(input=packet.frame_bytes, capture_stdout=True, capture_stderr=True)
        )
        frame = np.frombuffer(out, np.uint8)
        height, width = 1152, 2048
        frame = frame.reshape((height, width, 3))

        # Convert frame to UMat
        frame_umat = cv2.UMat(frame)

        # Draw a small square on the frame (example coordinates and color)
        cv2.rectangle(frame_umat, (200, 200), (150, 150), (0, 255, 0), 2)

        # Convert frame back to numpy array
        frame = frame_umat.get()

        # Display the frame
        cv2.imshow(window_name, frame)

        # Check for 'q' key press to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Close OpenCV windows
    cv2.destroyAllWindows()
    # Stop the video stream
    drone.stop_video_stream()

# Create and start a new thread for displaying the video stream
display_thread = threading.Thread(target=display_video_stream)
display_thread.start()
