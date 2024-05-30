import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import csv

# Initialize an empty list to store boxes
boxes = []

# Create 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

def plot_boxes():
    ax.clear()
    # Generate dynamic colors based on the number of boxes
    num_boxes = len(boxes)
    colors = plt.cm.viridis(np.linspace(0, 1, num_boxes))

    # Plot each box
    for i, (box, color) in enumerate(zip(boxes, colors)):
        x = box[:, 0]
        y = box[:, 1]
        z = box[:, 2]
        ax.plot(x[[0, 1, 2, 3, 0]], y[[0, 1, 2, 3, 0]], zs=z[[0, 1, 2, 3, 0]], color=color)
        ax.plot(x[[0, 1]], y[[0, 1]], zs=z[[0, 1]], color=color)
        ax.plot(x[[1, 2]], y[[1, 2]], zs=z[[1, 2]], color=color)
        ax.plot(x[[2, 3]], y[[2, 3]], zs=z[[2, 3]], color=color)
        ax.plot(x[[3, 0]], y[[3, 0]], zs=z[[3, 0]], color=color)

        # Add index label
        ax.text(np.mean(x), np.mean(y), np.mean(z), str(i), color='black')

    # Label axes
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    # Find the maximum and minimum coordinates of all boxes
    all_x = [point[0] for box in boxes for point in box]
    all_y = [point[1] for box in boxes for point in box]
    all_z = [point[2] for box in boxes for point in box]
    max_x, min_x = max(all_x), min(all_x)
    max_y, min_y = max(all_y), min(all_y)
    max_z, min_z = max(all_z), min(all_z)

    # Set plot limits based on maximum and minimum coordinates with some padding
    padding = 0.1
    ax.set_xlim(min_x - padding, max_x + padding)
    ax.set_ylim(min_y - padding, max_y + padding)
    ax.set_zlim(min_z - padding, max_z + padding)

    # Show plot
    plt.draw()
    plt.pause(0.001)

# Function to add a new box
def add_box(box):
    boxes.append(box)
    plot_boxes()

def read_csv(csv_file):
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            coordinates_str = row[1]
            coordinates = np.array(eval(coordinates_str))
            add_box(coordinates)

# Read CSV data
csv_file = '/home/hestabit/PROJECTS/image-stuff/projection_stuff/camera_coordinates3.csv'  # Update with your CSV file path
data = read_csv(csv_file)

# Keep the plot open until 'q' is pressed
while True:
    if plt.waitforbuttonpress():
        if plt.get_current_fig_manager().toolbar.mode == '':
            key = plt.get_current_fig_manager().window.key
            if key == 'q':
                plt.close()
                break
