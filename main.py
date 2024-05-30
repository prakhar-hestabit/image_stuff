import csv
import ast

def calculate_center_point(box_corners):
    x_sum = 0
    y_sum = 0
    z_sum = 0

    for corner in box_corners:
        x_sum += corner[0]
        y_sum += corner[1]
        z_sum += corner[2]

    num_corners = len(box_corners)
    center_x = x_sum / num_corners
    center_y = y_sum / num_corners
    center_z = z_sum / num_corners

    return center_x, center_y, center_z

def main():
    with open('/home/hestabit/PROJECTS/image-stuff/projection_stuff/camera_coordinates3.csv', 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        
        for row in csv_reader:
            image = row['Image']
            box_corners_str = row['Box_Corners_Camera_Coordinates']
            box_corners = ast.literal_eval(box_corners_str)
            
            center_point = calculate_center_point(box_corners)
            print(f"{center_point}")

if __name__ == "__main__":
    main()
