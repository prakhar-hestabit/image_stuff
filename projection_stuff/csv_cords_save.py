import cv2
import numpy as np
import csv
def load_csv_data(csv_file):
    data = []
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            # Print each row to check if it's correctly parsed
            print(row)
            data.append({
                'img': row[0],
                'coords': [int(coord) for coord in row[1:]]
            })
    return data

# Load CSV data
csv_file = '/home/hestabit/PROJECTS/image-stuff/projection_stuff/ball_box_cords.csv'  # Update with your CSV file path
image_data = load_csv_data(csv_file)


Camera_matrix = [[2.05712194e+03, 0.00000000e+00, 3.00991431e+02],
                 [0.00000000e+00, 1.94815701e+03, 1.59432241e+02],
                 [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]]
Distortion_coeff = [[1.43317465e+00, -4.10515995e+01, -4.62217722e-02, -7.13175349e-03,
                     -7.38811063e-01]]

# Load the calibration data
camera_matrix = np.array(Camera_matrix)
dist_coeffs = np.array(Distortion_coeff)

output_file = 'camera_coordinates3.csv'  # Output CSV file path
with open(output_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Image', 'Box_Corners_Camera_Coordinates'])  # Write header

    for data_entry in image_data:
        image_path = data_entry['img']
        image = cv2.imread(image_path)

        # Coordinates from CSV
        coords = data_entry['coords']
        x1, y1, x2, y2, x3, y3, x4, y4 = coords

        # Define the real-world coordinates of the box corners (assuming a known size)
        object_points = np.array([
            [0, 0, 0],          # Bottom-left corner
            [1, 0, 0],          # Bottom-right corner
            [1, 1, 0],          # Top-right corner
            [0, 1, 0]           # Top-left corner
        ], dtype=np.float32)

        # Image points corresponding to the box corners
        image_points = np.array([
            [x1, y1],  # Bottom-left corner
            [x2, y2],  # Bottom-right corner
            [x3, y3],  # Top-right corner
            [x4, y4]   # Top-left corner
        ], dtype=np.float32)

        # Estimate the pose of the object
        ret, rvec, tvec = cv2.solvePnP(object_points, image_points, camera_matrix, dist_coeffs)

        if ret:
            # Convert rotation vector to rotation matrix
            R, _ = cv2.Rodrigues(rvec)

            # Transform the object points to the camera's coordinate system
            object_points_camera = R @ object_points.T + tvec

            # Format the coordinates as a string
            coordinates_str = str(object_points_camera.T.tolist())

            # Write the image path and coordinates string to the CSV file
            writer.writerow([image_path, coordinates_str])
        else:
            print(f"Pose estimation failed for {image_path}.")
