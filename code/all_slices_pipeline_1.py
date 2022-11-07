import open3d as o3d
import numpy as np
import pandas as pd
import os
from PIL import Image
import image_ai_BB_generator_2
import actual_coords_from_BB_3
import cosine_similarity_4
import parent_isolator_5
import mesh_reconstruction_6
import image_filter_7
import time
from datetime import datetime

def pipeline(pcd_filename):
    execution_path = os.getcwd()
    t = time.localtime();    current_time = time.strftime("%H:%M:%S", t);   print(current_time)
    print(pcd_filename)


    pcd = o3d.io.read_point_cloud(execution_path + '\\input\\'+ pcd_filename + '.pcd')
    # o3d.visualization.draw_geometries([pcd])
    #
    # voxel_down_pcd = pcd.voxel_down_sample(voxel_size=.02)
    # o3d.visualization.draw_geometries([voxel_down_pcd])
    #
    # voxel_down_pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.2, max_nn=15))
    # voxel_down_pcd.orient_normals_consistent_tangent_plane(k=15)
    #
    # voxel_down_pcd.remove_statistical_outlier(nb_neighbors=20, std_ratio=2.0)
    # o3d.visualization.draw_geometries([voxel_down_pcd])
    #
    # pcd = voxel_down_pcd

    pcd_np = np.hstack((np.asarray(pcd.points), np.asarray(pcd.colors)))

    x_values = pcd_np[:, 0];
    # r_values = pcd_np[:, 3];
    y_values = pcd_np[:, 1];
    # g_values = pcd_np[:, 4];
    z_values = pcd_np[:, 2];
    # b_values = pcd_np[:, 5];
    xmax = np.max(x_values);    xmin = np.min(x_values);    x_range = xmax - xmin
    ymax = np.max(y_values);    ymin = np.min(y_values);    y_range = ymax - ymin
    zmax = np.max(z_values);    zmin = np.min(z_values);    z_range = zmax - zmin

    x_sized_20 = [[xmin, 0.2 * x_range + xmin], [0.1 * x_range + xmin, 0.3 * x_range + xmin],
                  [0.2 * x_range + xmin, 0.4 * x_range + xmin],
                  [0.3 * x_range + xmin, 0.5 * x_range + xmin], [0.4 * x_range + xmin, 0.6 * x_range + xmin],
                  [0.5 * x_range + xmin, 0.7 * x_range + xmin], [0.6 * x_range + xmin, 0.8 * x_range + xmin],
                  [0.7 * x_range + xmin, 0.9 * x_range + xmin], [0.8 * x_range + xmin, x_range + xmin]]
    x_sized_30 = [[xmin, 0.3 * x_range + xmin], [0.15 * x_range + xmin, 0.45 * x_range + xmin],
                  [0.3 * x_range + xmin, 0.6 * x_range + xmin]
        , [0.45 * x_range + xmin, 0.75 * x_range + xmin], [0.6 * x_range + xmin, 0.9 * x_range + xmin],
                  [0.7 * x_range + xmin, x_range + xmin]]
    x_sized_40 = [[xmin, 0.4 * x_range + xmin], [0.2 * x_range + xmin, 0.6 * x_range + xmin],
                  [0.4 * x_range + xmin, 0.8 * x_range + xmin]
        , [0.6 * x_range + xmin, x_range + xmin]]
    x_sized_50 = [[xmin, 0.5 * x_range + xmin], [0.25 * x_range + xmin, 0.75 * x_range + xmin],
                  [0.5 * x_range + xmin, x_range + xmin]]

    sized_slice_locs = [x_sized_20, x_sized_30, x_sized_40, x_sized_50]

    output = pd.DataFrame()
    image_output_loc = execution_path + '\images_without_bb' + "\\"
    detected_object_data_all = []

    for k in range(len(sized_slice_locs)):
        print(" slice sizes " + str(k + 1) + " of " + str(len(sized_slice_locs)) )
        print("\n")
        for j in range(len(sized_slice_locs[k])):
            print(' slice locations ' + str(j + 1) + " of " + str(len(sized_slice_locs[k])))
            print(detected_object_data_all)

            something = (sized_slice_locs[k][j][1] - sized_slice_locs[k][j][0]) / x_range
            if something == 0.2:
                name = "x_sized_20"
            elif something == 0.3:
                name = "x_sized_30"
            elif something == 0.4:
                name = "x_sized_40"
            elif something == 0.5:
                name = "x_sized_50"
            sliced_pcd = pcd_np
            indexes = []
            print("\t slice location is at : " + str(sized_slice_locs[k][j]))
            for i in range(pcd_np.shape[0]):
                mask_x = np.logical_or(  sized_slice_locs[k][j][0] >= pcd_np[:, 0][i], pcd_np[:, 0][i] >= sized_slice_locs[k][j][1]  )
                if sized_slice_locs[k][j][0] >= pcd_np[:, 0][i] or pcd_np[:, 0][i] >= sized_slice_locs[k][j][1]:
                    indexes.append(i)
            sliced_pcd = np.delete(sliced_pcd, indexes, axis=0)
            # x_min_temp = np.min(sliced_pcd[:, 0]); x_max_temp = np.max(sliced_pcd[:, 0])
            image_name = name + '%s' % str(j)

            height = 500
            width = 1000

            # temp = np.zeros([height, width, 1], dtype=np.uint8)
            image_array = np.zeros([height, width, 3], dtype=np.uint8)  # empty image sized array
            temp = np.full((height, width, 1), xmin)  # used to check if the bin/pixel is already taken
            for i in range(sliced_pcd.shape[0]):  # iterating through all points of sliced pcd->(x,y,z,r,g,b)
                w = int(abs(sliced_pcd[:, 1][i] * (width / y_range)))  # mapping point's Y to image's width
                h = int(abs(sliced_pcd[:, 2][i] * (height / z_range)))  # mapping point's Z to image's height
                if temp[h][w][0] < (sliced_pcd[:, 0][i]):
                    image_array[h][w][0] = 255 * (sliced_pcd[:, 3][i])  # image's R
                    image_array[h][w][1] = 255 * (sliced_pcd[:, 4][i])  # image's G
                    image_array[h][w][2] = 255 * (sliced_pcd[:, 5][i])  # image's B
                    temp[h][w][0] = (sliced_pcd[:, 0][i])
                else:
                    continue

            # updated_image = image_filter_7.image_filter(image_array, 3)
            updated_image = image_array
            img = Image.fromarray(updated_image)
            img = img.rotate(180)
            img = img.transpose(Image.FLIP_LEFT_RIGHT)
            img.save(image_output_loc + image_name + '.jpg')
            # img = cv.imread(image_output_loc + image_name + '.jpg')
            # img = cv.medianBlur(img, 3)
            # cv.imwrite(image_output_loc + image_name + '.jpg', img)
            # print("Time before object detection =", datetime.now().strftime("%H:%M:%S"))
            objects_detected = image_ai_BB_generator_2.imageai(image_name)
            print("\t " + str(len(objects_detected)) + " objects detected in " + str(image_name + '.jpg'))
            count = 0
            # np.savetxt("delete_this" + image_name + ".csv", sliced_pcd, delimiter=",")
            if len(objects_detected) != 0:
                for eachObject in objects_detected:
                    print("\t object_detected_is : " + eachObject["name"])
                    original_coords = actual_coords_from_BB_3.original_coords(eachObject["box_points"], sliced_pcd, height,
                                                                              width, y_range, z_range, image_name)
                    detected_object_data = original_coords
                    detected_object_data.insert(0, eachObject["name"])
                    detected_object_data.append(eachObject["percentage_probability"])
                    detected_object_data.append(image_name + str(count))
                    detected_object_data_all.append(detected_object_data)
                    output = output.append(detected_object_data, ignore_index=True)
                    count += 1
                    print("\t\t " + str(detected_object_data) + "\n")
            else:
                print("\t\t no objects in this one: " + image_name + ".jpg")
        df = pd.DataFrame(detected_object_data_all, columns=['object_name', 'x1', 'y1', 'z1', 'x2', 'y2', 'z2', 'confidence', 'image_name'])
        print(df)
    execution_path = os.getcwd()
    print('final dataframe')
    print(df)
    df.to_csv(execution_path + '\\output\\detected_data_all.csv', index=False)

    t = time.localtime();    current_time = time.strftime("%H:%M:%S", t);   print(current_time)

    unique_detections, unique_detection_names = cosine_similarity_4.cosine_filter(df)
    print("lengths of unique and names " + str(len(unique_detections)) + " and " + str(len(unique_detection_names)))

    unique_detections = np.hstack((unique_detection_names, unique_detections[:,1:]))
    unique_df = pd.DataFrame(unique_detections)
    print("unique detections")
    print(unique_detections)
    unique_df.to_csv(execution_path+'\\output\\unique_of_all_detections.csv', index = False)

    parent_pcd_wo_objects_np = parent_isolator_5.isolate_parent(pcd_np, unique_detections)
    print("parent_pcd_isolated length is " + str(parent_pcd_wo_objects_np.shape))

    parent_pcd_wo_objects = o3d.geometry.PointCloud()
    parent_pcd_wo_objects.points = o3d.utility.Vector3dVector(parent_pcd_wo_objects_np[:,0:3])
    parent_pcd_wo_objects.colors = o3d.utility.Vector3dVector(parent_pcd_wo_objects_np[:,3:])
    o3d.io.write_point_cloud(execution_path+"\output\detected_objs_removed_pcd.pcd", parent_pcd_wo_objects)

    mesh = mesh_reconstruction_6.poisson_mesh(parent_pcd_wo_objects)
    print(mesh)
    # o3d.visualization.draw_geometries([mesh], mesh_show_back_face=True)
    o3d.io.write_triangle_mesh(execution_path+'\\output\\poisson_reconstruction_wo_objs.ply', mesh, write_ascii=True)
    o3d.io.write_triangle_mesh(execution_path+'\\output\\poisson_reconstruction_wo_objs_obj.obj', mesh, write_ascii=True)

    t = time.localtime();    current_time = time.strftime("%H:%M:%S", t);   print(current_time)
    return None