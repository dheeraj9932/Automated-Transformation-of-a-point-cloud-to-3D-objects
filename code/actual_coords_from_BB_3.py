# have (w1,h1), and (w2,h2) from yolo

import numpy as np
import os



def original_coords(img_bounding_box, sliced_pointcloud, height, width, y_range, z_range, image_name):
    # np.savetxt("delete_this" + image_name + ".csv", sliced_pointcloud, delimiter=",")
    X_values = []
    #
    # if y1_coord < y2_coord:
    #     y_coord_min = y1_coord;        y_coord_max = y2_coord
    # else:
    #     y_coord_min = y2_coord;        y_coord_max = y1_coord
    #
    # if z1_coord < z2_coord:
    #     z_coord_min = z1_coord;        z_coord_max = z2_coord
    # else:
    #     z_coord_min = z2_coord;        z_coord_max = z1_coord
    cropped_point_cloud = []
    total_number_of_points = sliced_pointcloud.shape[0]

    # width x height = 1000 x 500
    # w1, w2 are horizontal locations of bounding box corners
    Z_max = max(sliced_pointcloud[:, 2])  # highest Z value of all points
    w1 = img_bounding_box[0];
    h1 = img_bounding_box[1];
    w2 = img_bounding_box[2];
    h2 = img_bounding_box[3];

    y1_coord = (w1 * y_range) / width  # where y_range is Ymax-Ymin
    z1_coord = Z_max - (h1 * z_range) / height  # use Z_max because image_height and Z
    # are inversely proportional, Unlike Y and X

    y2_coord = (w2 * y_range) / width
    z2_coord = Z_max - (h2 * z_range) / height
    for i in range(total_number_of_points):
        x = (sliced_pointcloud[:, 0][i])  # assigning values of current point to-
        y = (sliced_pointcloud[:, 1][i])  # local variables
        z = (sliced_pointcloud[:, 2][i])
        r = (sliced_pointcloud[:, 3][i])
        g = (sliced_pointcloud[:, 4][i])
        b = (sliced_pointcloud[:, 5][i])

        if (y1_coord) <= y <= (y2_coord):
            if (z1_coord) >= z >= (z2_coord):
                X_values.append(x)
                cropped_point_cloud.append([x, y, z, r, g, b])

    x1y1z1_x2y2z2 = [min(X_values), y1_coord, z1_coord,
                     max(X_values), y2_coord, z2_coord]

    # print("\t unique z's " + str(np.unique(np.round(sliced_pointcloud[:, 2], 1)))+str(sliced_pointcloud[:,1:2]))
    # print("\t unique z's " + str(sliced_pointcloud))
    print("\t\t y1,z1,y2,z2 are " + str(y1_coord) + ", " + str(z1_coord) + ", " + str(y2_coord) + ", " + str(z2_coord))
    # print("\t\t len of x_value_after_filtering is " + str(len(x_value_after_filtering)))
    print("\t\t " + str(img_bounding_box))
    cropped_point_cloud = np.asarray(cropped_point_cloud)
    size = str(len(cropped_point_cloud))
    execution_path = os.getcwd()

    np.savetxt(execution_path + "\\cropped_pcds\\" + image_name +"_"+size+ ".csv", cropped_point_cloud, delimiter=",")
    # np.savetxt("delete_this"+image_name+".csv", sliced_pointcloud, delimiter=",")

    return x1y1z1_x2y2z2

# from temp_pcd_np, extract range of X values (max and min) given point's y and z are inside (y1, z1) and (y2, z2)
