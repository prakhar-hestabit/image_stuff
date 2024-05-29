import cv2
import numpy as np

# Load the image
image_path = '/home/hestabit/PROJECTS/image-stuff/projection_stuff/captured_image.png'
image = cv2.imread(image_path)

Camera_matrix= [
    [1.26451838e+03, 0.00000000e+00, 3.73516559e+02],
    [0.00000000e+00, 1.23406649e+03, 3.36590322e+02],
    [0.00000000e+00, 0.00000000e+00, 1.00000000e+00],
]
Distortion_coeff=[
    [ 0.46028522, -1.27183038,  0.02666947,  0.01650489, -2.01807043]
]
# Load the calibration data
camera_matrix = np.array(Camera_matrix)
dist_coeffs = np.array(Distortion_coeff)

# Coordinates of the box in the image (you'll need to manually find these)
# For the purpose of this example, let's say these are the coordinates
x1, y1 = 497, 326  # Bottom-left corner
x2, y2 = 566, 330  # Bottom-right corner
x3, y3 = 567, 262  # Top-right corner
x4, y4 = 503, 260  # Top-left corner

# Define the real-world coordinates of the box corners (assuming a known size)
# Example: A box of size 1x1 cm
object_points = np.array([
    [0, 0, 1],          # Bottom-left corner
    [1, 0, 1],          # Bottom-right corner
    [1, 1, 1],          # Top-right corner
    [0, 1, 1]           # Top-left corner
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
    
    # Print the coordinates of the box corners in the camera's coordinate system
    print("Coordinates of the box corners in the camera's coordinate system:")
    print(object_points_camera.T)
else:
    print("Pose estimation failed.")