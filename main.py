import csv
import ast

def calculate_center(box_corners):
    x_values = [point[0] for point in box_corners]
    y_values = [point[1] for point in box_corners]
    z_values = [point[2] for point in box_corners]
    center_x = sum(x_values) / len(x_values)
    center_y = sum(y_values) / len(y_values)
    center_z = sum(z_values) / len(z_values)
    return center_x, center_y, center_z

def main():
    with open('/home/hestabit/PROJECTS/image-stuff/projection_stuff/pose_estimation_results.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            image = row['Image']
            box_corners_str = row['Box_Corners_Camera_Coordinates']
            box_corners = ast.literal_eval(box_corners_str)
            center_x, center_y, center_z = calculate_center(box_corners)
            print(f"Image {image} center: ({center_x}, {center_y}, {center_z})")

if __name__ == "__main__":
    main()
