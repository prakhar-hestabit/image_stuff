import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import LinearSegmentedColormap
import csv

# Initialize an empty list to store boxes
boxes = []

# Define colors for each box
colors = ['r', 'g', 'b', 'y', 'c']

# Create 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

def plot_boxes():
    ax.clear()
    # Plot each box
    for i, box in enumerate(boxes):
        x = box[:, 0]
        y = box[:, 1]
        z = box[:, 2]
        ax.plot(x[[0, 1, 2, 3, 0]], y[[0, 1, 2, 3, 0]], zs=z[[0, 1, 2, 3, 0]], color=colors[i])
        ax.plot(x[[0, 1]], y[[0, 1]], zs=z[[0, 1]], color=colors[i])
        ax.plot(x[[1, 2]], y[[1, 2]], zs=z[[1, 2]], color=colors[i])
        ax.plot(x[[2, 3]], y[[2, 3]], zs=z[[2, 3]], color=colors[i])
        ax.plot(x[[3, 0]], y[[3, 0]], zs=z[[3, 0]], color=colors[i])

    # Label axes
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    # Set plot limits
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_zlim(0, 20)

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
csv_file = '/home/hestabit/PROJECTS/image-stuff/projection_stuff/camera_coordinates2.csv'  # Update with your CSV file path
data = read_csv(csv_file)


# Keep the plot open until 'q' is pressed
while True:
    if plt.waitforbuttonpress():
        if plt.get_current_fig_manager().toolbar.mode == '':
            key = plt.get_current_fig_manager().window.key
            if key == 'q':
                plt.close()
                break