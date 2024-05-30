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
                'coords': [int(coord) for coord in row[1:]]
            })
    return data

# Load CSV data
csv_file = '/home/hestabit/PROJECTS/image-stuff/point_projection/click_info.csv'  # Update with your CSV file path
image_data = load_csv_data(csv_file)

Camera_matrix = [[4.62927925e+03, 0.00000000e+00, 2.48378341e+02],
                          [0.00000000e+00, 4.39332184e+03, 1.67522215e+02],
                          [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]]
Distortion_coeff = [[5.17214751e-01, -1.31074218e+02, -1.62111916e-02,  2.50774333e-02, -1.09878530e+00]]

# Load the calibration data
camera_matrix = np.array(Camera_matrix)
dist_coeffs = np.array(Distortion_coeff)

output_file = 'camera_coordinates2.csv'  # Output CSV file path
with open(output_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Image', 'Sphere_Center_Camera_Coordinates'])  # Write header

    for data_entry in image_data:
        image_path = data_entry['img']
        image = cv2.imread(image_path)

        # Coordinates from CSV
        x, y, radius = data_entry['coords']

        # Define the real-world coordinates of the sphere center
        # Assuming the center of the sphere is the origin (0, 0, 0)
        # And the radius of the sphere is known
        # You can adjust the scale and position according to your real-world setup
        object_center = np.array([x, y, 0], dtype=np.float32)  # Sphere center in real-world coordinates

        # Image points corresponding to the sphere center
        image_center = np.array([[x, y]], dtype=np.float32)

        # Estimate the pose of the object (sphere)
        ret, rvec, tvec = cv2.solvePnP(object_center, image_center, camera_matrix, dist_coeffs)

        if ret:
            # Format the coordinates as a string
            coordinates_str = f"Center: {tvec.flatten().tolist()}, Radius: {radius}"

            # Write the image path and coordinates string to the CSV file
            writer.writerow([image_path, coordinates_str])
        else:
            print(f"Pose estimation failed for {image_path}.")
