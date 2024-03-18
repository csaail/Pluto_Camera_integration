import cv2

# Open the H.264 file
video_file = 'out.h264'

# Create a VideoCapture object
cap = cv2.VideoCapture(video_file)

# Check if the file was opened successfully
if not cap.isOpened():
    print("Error: Could not open video file.")
    exit()

# Loop through the video frames
while True:
    # Read a frame from the video
    ret, frame = cap.read()

    # If the frame was not read successfully, break the loop
    if not ret:
        break

    # Display the frame
    cv2.imshow('Frame', frame)

    # Check for user input to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the VideoCapture object and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()