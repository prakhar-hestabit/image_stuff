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
                'img': row[0],
                'center': (int(row[1]), int(row[2])),  # Center coordinates (x, y)
                'radius': float(row[3])  # Radius
            })
    return data

# Load CSV data
csv_file = '/home/hestabit/PROJECTS/image-stuff/point_projection/click_info.csv'  # Update with your CSV file path
image_data = load_csv_data(csv_file)

# Camera calibration parameters
camera_matrix = np.array([[4.62927925e+03, 0.00000000e+00, 2.48378341e+02],
                          [0.00000000e+00, 4.39332184e+03, 1.67522215e+02],
                          [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])
dist_coeffs = np.array([[5.17214751e-01, -1.31074218e+02, -1.62111916e-02,  2.50774333e-02, -1.09878530e+00]])

output_file = 'camera_coordinates3d.csv'  # Output CSV file path
with open(output_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Image', 'X', 'Y', 'Z'])  # Write header

    for data_entry in image_data:
        image_path = data_entry['img']
        image = cv2.imread(image_path)

        # Center and radius from CSV
        center = data_entry['center']

        x_center, y_center = center

        # Define the real-world coordinates of the reference point
        # Modify these values based on your real-world scene
        reference_point_world = np.array([[0], [0], [0]])

        # Image points corresponding to the reference point
        image_points = np.array([[x_center, y_center]], dtype=np.float32)

        # Estimate the pose of the camera relative to the reference point
        ret, rvec, tvec = cv2.solvePnP(reference_point_world, image_points, camera_matrix, dist_coeffs)

        if ret:
            # Write the image path and real-world coordinates to the CSV file
            writer.writerow([image_path, tvec[0][0], tvec[1][0], tvec[2][0]])
        else:
            print(f"Pose estimation failed for {image_path}.")
