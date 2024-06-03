import cv2

def extract_frames(video_path, output_folder, target_fps):
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_skip = int(round(fps / target_fps))

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % frame_skip == 0:
            frame_path = f'{output_folder}/frame_{frame_count}.jpg'
            cv2.imwrite(frame_path, frame)
            print(f"Frame {frame_count} saved as {frame_path}")
        frame_count += 1

    cap.release()

# Example usage:
video_path = "/home/hestabit/PROJECTS/image-stuff/test_stuff/recorded_video_0.avi"
output_folder = "/home/hestabit/PROJECTS/image-stuff/test_stuff/frames_ball"
target_fps = 14
extract_frames(video_path, output_folder, target_fps)
