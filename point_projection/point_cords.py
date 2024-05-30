import cv2
import numpy as np
import csv

def load_csv_data(csv_file):
    data = []
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            data.append({
                'img': f"frame_{row[0]}.jpg",  # Assuming image names follow a pattern like frame_1.jpg, frame_2.jpg, etc.
                'center': (int(row[1]), int(row[2]))  # Center coordinates (x, y)
            })
    return data

# Load CSV data
csv_file = '/home/hestabit/PROJECTS/image-stuff/point_projection/click_info.csv'  # Update with your CSV file path
image_data = load_csv_data(csv_file)

Camera_matrix = [[4.62927925e+03, 0.00000000e+00, 2.48378341e+02],
 [0.00000000e+00, 4.39332184e+03, 1.67522215e+02],
 [0.00000000e+00, 0.00000000e+00, 1.00000000e+00],]
Distortion_coeff = [[ 5.17214751e-01, -1.31074218e+02, -1.62111916e-02,  2.50774333e-02,
  -1.09878530e+00]]

# Load the calibration data
camera_matrix = np.array(Camera_matrix)
dist_coeffs = np.array(Distortion_coeff)

output_file = 'camera_coordinates.csv'  # Output CSV file path
with open(output_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Image', 'Center_Camera_Coordinates'])  # Write header

    for data_entry in image_data:
        image_path = data_entry['img']
        image = cv2.imread(image_path)

        # Center from CSV
        center = data_entry['center']

        x_center, y_center = center

        # Define the real-world coordinates of the circle's center
        object_points = np.array([
            [0, 0, 0]  # Center of the circle
        ], dtype=np.float32)

        # Image points corresponding to the circle's center
        image_points = np.array([
            [x_center, y_center]  # Center of the circle
        ], dtype=np.float32)

        # Estimate the pose of the object
        ret, rvec, tvec = cv2.solvePnP(object_points, image_points, camera_matrix, dist_coeffs)

        if ret:
            # Convert rotation vector to rotation matrix
            R, _ = cv2.Rodrigues(rvec)

            # Transform the object point to the camera's coordinate system
            object_point_camera = R @ object_points.T + tvec

            # Format the coordinates as a string
            center_camera_coordinates_str = str(object_point_camera.T[0].tolist())

            # Write the image path and center coordinates to the CSV file
            writer.writerow([image_path, center_camera_coordinates_str])
        else:
            print(f"Pose estimation failed for {image_path}.")
