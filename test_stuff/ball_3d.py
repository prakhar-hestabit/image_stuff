import numpy as np
import pandas as pd
import cv2
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

Camera_matrix = [[4.62927925e+03, 0.00000000e+00, 2.48378341e+02],
 [0.00000000e+00, 4.39332184e+03, 1.67522215e+02],
 [0.00000000e+00, 0.00000000e+00, 1.00000000e+00],]
Distortion_coeff = [[5.17214751e-01, -1.31074218e+02, -1.62111916e-02,  2.50774333e-02, -1.09878530e+00]]

# Define the camera matrix and distortion coefficients (replace with actual values)
fx = 4.62927925e+03  # example value, replace with actual value
fy = 4.39332184e+03  # example value, replace with actual value
cx = 2.48378341e+02   # example value, replace with actual value
cy = 1.67522215e+02  # example value, replace with actual value

camera_matrix = np.array(Camera_matrix)

dist_coeffs = np.array(Distortion_coeff)

# Known diameter of the ball (in meters)
known_diameter = 0.0726

# Load the CSV file
csv_file = '/home/hestabit/PROJECTS/image-stuff/point_projection/click_info.csv'  # replace with the actual path to your CSV file
data = pd.read_csv(csv_file)


def estimate_3d_position(pixel_coords, radius):
    undistorted_coords = cv2.undistortPoints(np.array([pixel_coords], dtype = np.float32), camera_matrix, dist_coeffs,
                                             P = camera_matrix)
    normalized_coords = np.array([[(undistorted_coords[0][0][0] - cx) / fx,
                                   (undistorted_coords[0][0][1] - cy) / fy]], dtype = np.float32)

    # Estimate depth (Z) using the known diameter of the ball
    # Z = (focal_length * real_diameter) / apparent_diameter
    Z = (fx * known_diameter) / (2 * radius)

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

# Plot the 3D path
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot the points and connect them with lines
ax.plot(path_3d[:, 0], path_3d[:, 1], path_3d[:, 2], marker='o')

# Label each point with the corresponding frame number
for i, frame in enumerate(frames):
    ax.text(path_3d[i, 0], path_3d[i, 1], path_3d[i, 2], str(frame), color='red')

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('3D Path of the Ball')

plt.show()
