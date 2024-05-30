import os
import subprocess
import cv2
import csv

# Function to get processes using the camera
def get_camera_using_processes():
    # Replace '/dev/video0' with your camera device if it's different
    cmd = "lsof /dev/video0"
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    
    processes = []
    if stdout:
        lines = stdout.decode().splitlines()
        for line in lines[1:]:  # Skip the header line
            parts = line.split()
            if len(parts) >= 2:
                processes.append(parts[1])  # PID is the second column
    return processes

# Function to kill processes using the camera
def kill_processes(pids):
    for pid in pids:
        try:
            os.kill(int(pid), 9)  # Signal 9 is SIGKILL
            print(f"Killed process {pid} using the camera.")
        except Exception as e:
            print(f"Failed to kill process {pid}: {e}")

# Callback function to get the coordinates of the point clicked
def get_coordinates(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"Coordinates: ({x}, {y})")
        global current_frame, frame_count, csv_writer
        if current_frame is not None:
            frame_copy = current_frame.copy()
            cv2.circle(frame_copy, (x, y), 5, (0, 255, 0), -1)  # Draw a circle at the click point
            filename = f"{frame_count}.png"
            cv2.imwrite(filename, frame_copy)
            print(f"Saved frame as {filename}")
            
            # Write click info to CSV
            csv_writer.writerow([frame_count, x, y])
            frame_count += 1

# Try to get and kill processes using the camera
camera_device = '/dev/video0'  # Adjust if necessary
processes_using_camera = get_camera_using_processes()
if processes_using_camera:
    print(f"Processes using the camera: {processes_using_camera}")
    kill_processes(processes_using_camera)

# Create a video capture object
cap = cv2.VideoCapture(0)  # 0 for default webcam

if not cap.isOpened():
    print("Error: Could not open video source.")
    exit()

cv2.namedWindow('Video Frame')
cv2.setMouseCallback('Video Frame', get_coordinates)

current_frame = None
frame_count = 1  # Initialize frame counter

# Open CSV file to log click information
csv_file = open('click_info.csv', 'w', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Frame', 'X', 'Y'])  # Write CSV header

while cap.isOpened():
    ret, frame = cap.read()
    
    if not ret:
        print("Error: Could not read frame.")
        break
    
    current_frame = frame
    cv2.imshow('Video Frame', frame)
    
    key = cv2.waitKey(1)  # Wait 1 ms for a key press, to allow video to keep playing
    if key == 27:  # Press 'ESC' to exit
        break

# Release the video capture object and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()

# Close the CSV file
csv_file.close()
