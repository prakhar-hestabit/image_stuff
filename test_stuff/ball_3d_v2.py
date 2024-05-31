import numpy as np
import pandas as pd
import cv2
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Camera matrix
camera_matrix = np.array([[4.62927925e+03, 0.00000000e+00, 2.48378341e+02],
                          [0.00000000e+00, 4.39332184e+03, 1.67522215e+02],
                          [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])

# Distortion coefficients
dist_coeffs = np.array([[5.17214751e-01, -1.31074218e+02, -1.62111916e-02, 2.50774333e-02, -1.09878530e+00]])

# Known diameter of the ball (in meters)
known_diameter = 0.2

# Load the CSV file
csv_file = '/home/hestabit/PROJECTS/image-stuff/point_projection/click_info.csv'  # replace with the actual path to your CSV file
data = pd.read_csv(csv_file)


def estimate_3d_position(pixel_coords, radius):
    undistorted_coords = cv2.undistortPoints(np.array([pixel_coords], dtype = np.float32), camera_matrix, dist_coeffs,
                                             P = camera_matrix)
    normalized_coords = np.array([[(undistorted_coords[0][0][0]),
                                   (undistorted_coords[0][0][1])]], dtype = np.float32)

    # Estimate depth (Z) using the known diameter of the ball
    # Z = (focal_length * real_diameter) / apparent_diameter
    Z = (camera_matrix[0][0] * known_diameter) / (2 * radius)

    # Compute the real-world coordinates
    X = normalized_coords[0][0] * Z
    Y = normalized_coords[0][1] * Z

    return np.array([X, Y, Z], dtype = np.float32)


# List to store the 3D path
path_3d = []
frames = []

for index, row in data.iterrows():
    frame_number = row['Image']
    pixel_coords = (row['Center_X'], row['Center_Y'])
    radius = row['Radius']

    position_3d = estimate_3d_position(pixel_coords, radius)
    path_3d.append(position_3d)
    frames.append(frame_number)

# Convert the 3D path to a numpy array for further processing
path_3d = np.array(path_3d)

# Plot the 3D path from the camera's POV
fig = plt.figure()
ax = fig.add_subplot(111, projection = '3d')

# Plot the points and connect them with lines
ax.plot(path_3d[:, 0], path_3d[:, 1], path_3d[:, 2], marker = 'o')

# Label each point with the corresponding frame number
for i, frame in enumerate(frames):
    ax.text(path_3d[i, 0], path_3d[i, 1], path_3d[i, 2], str(frame), color = 'red')

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('3D Path of the Ball (Camera POV)')

# Set the aspect ratio of the plot to be equal
ax.set_box_aspect([1, 1, 1])

# Invert the y-axis to match the camera's POV
ax.invert_yaxis()

plt.show()
