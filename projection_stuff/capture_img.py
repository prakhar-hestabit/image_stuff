import cv2

# Set the camera device index (2 in this case)
device_index = 2

# Initialize video capture with the specified device
cap = cv2.VideoCapture(device_index)

if not cap.isOpened():
    print(f"Error: Could not open video device {device_index}")
    exit()

print("Press 'c' to capture and save the frame. Press 'q' to quit.")
img_name_to_save = "captured_image_4"
while True:
    # Capture a single frame
    ret, frame = cap.read()

    if not ret:
        print("Error: Could not read frame from video device")
        break

    # Display the captured frame
    cv2.imshow('Camera Feed', frame)

    # Wait for the user to press a key
    key = cv2.waitKey(1) & 0xFF

    if key == ord('c'):
        # Save the captured frame to a file
        cv2.imwrite(f'{img_name_to_save}.png', frame)
        print(f"Image saved as '{img_name_to_save}.png'")
    elif key == ord('q'):
        # Exit the loop if 'q' is pressed
        break

# Release the video capture object
cap.release()

# Close any OpenCV windows
cv2.destroyAllWindows()
