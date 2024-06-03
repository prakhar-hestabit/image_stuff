import cv2

def save_video():
    vid_dev = "http://10.10.1.253:4747/video"
    cap = cv2.VideoCapture(vid_dev)

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = None
    recording = False
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow('Save Video', frame)

        # Start/stop recording when 's' key is pressed
        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):
            if recording:
                out.release()
                print("Recording stopped")
                recording = False
            else:
                out = cv2.VideoWriter(f'recorded_video_{frame_count}.avi', fourcc, 20.0, (frame.shape[1], frame.shape[0]))
                print("Recording started")
                recording = True
        elif key == ord('q') or key == 27:  # Press 'q' or ESC to exit
            break

        if recording:
            out.write(frame)
            frame_count += 1

    cap.release()
    cv2.destroyAllWindows()

# Main function to call the save_video function
if __name__ == "__main__":
    save_video()
