import subprocess
import cv2
import numpy as np

def process_frame(frame):
  # Convert to grayscale
  gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

  # Get frame dimensions
  height, width, _ = gray_frame.shape

  # Define triangle coordinates (adjust as needed)
  top_left = (int(width/4), int(height/4))
  top_right = (int(3*width/4), int(height/4))
  bottom = (int(width/2), int(3*height/4))

  # Draw green triangle
  cv2.line(gray_frame, top_left, top_right, (0, 255, 0), 2)  # Green line, thickness 2
  cv2.line(gray_frame, top_left, bottom, (0, 255, 0), 2)  # Green line, thickness 2
  cv2.line(gray_frame, top_right, bottom, (0, 255, 0), 2)  # Green line, thickness 2

  return gray_frame

command = "pylwdrone stream start --out-file - | ffmpeg -i - -f image2pipe pipe:1"

# Start the video stream and process frames
with subprocess.Popen(command, shell=True, stdout=subprocess.PIPE) as proc:
  while True:
    raw_frame = proc.stdout.read(1152 * 2048 * 3) 

    if not raw_frame:
      break 
    
    frame = np.frombuffer(raw_frame, dtype=np.uint8).reshape((1152, 2048, 3))

    processed_frame = process_frame(frame)

    # Display the processed frame with OpenCV
    cv2.imshow('Processed Frame', processed_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break

cv2.destroyAllWindows()
