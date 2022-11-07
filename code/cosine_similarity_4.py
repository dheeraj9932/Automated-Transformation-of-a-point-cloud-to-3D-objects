import math
import pandas as pd
import numpy as np
import re
import os

all_unique_objects = []
all_unique_object_names = []
real_coords = []


def square_rooted(x):
    return round(math.sqrt(sum([a * a for a in x])), 5)


def cosine_similarity(x, y):
    numerator = sum(a * b for a, b in zip(x, y))
    denominator = square_rooted(x) * square_rooted(y)
    return round(numerator / float(denominator), 5)

names = []
temp_names = []
def wt_avg(indexes, selected_obj):
    # print("in 'wt_avg' definition - indexes are :")
    # print(indexes)
    # print("in 'wt_avg' definition - selected_obj are :")
    # print(selected_obj)
    temp_indexes = indexes
    # if len(indexes) != 1:
    #     for i in range(len(indexes)):
    #         s = selected_obj[indexes[i][0]][8]
    #         smallest = re.search('x_sized_(\d+)', s, re.IGNORECASE)
    #         smallest_one = int(smallest.group(1))
    #         # smallest = int(list(filter(str.isdigit, s))[0])
    #         # print("smallest is : " + str(smallest_one))
    #         # print("also: " + str(re.search('x_sized_(\d+)', s, re.IGNORECASE)))
    #         limit = (smallest_one + 1000) - ((smallest_one + 1000)%1000) # 100 or 1000? how to know if it works?
    #         for j in range(len(indexes[i])):
    #             if len(indexes[i]) == 1:
    #                 break
    #             else:
    #                 s = selected_obj[indexes[i][j]][8]
    #                 current_thing = int(re.search('x_sized_(\d+)', s, re.IGNORECASE).group(1))
    #                 if current_thing >= limit:
    #                     temp_indexes[i] = np.delete(temp_indexes[i], j)
    #                     # temp_indexes[i].pop(j)
    #         middle = int(len(temp_indexes[i]) / 2)
    #         temp_indexes[i] = [temp_indexes[i][middle]]
    # else:
    #     None
    # print("temp_indexes after isolating smallest and middle detections")
    # print(temp_indexes)
    for i in range(len(indexes)):
        sum_y1 = 0;
        sum_z1 = 0;
        sum_y2 = 0;
        sum_z2 = 0;
        vals_y1 = 0;
        vals_z1 = 0;
        vals_y2 = 0;
        vals_z2 = 0;
        if len(indexes[i]) == 1:
            sum_y1 = 1; vals_y1 = selected_obj[indexes[i][0]][2];
            sum_z1 = 1; vals_z1 = selected_obj[indexes[i][0]][3];
            sum_y2 = 1; vals_y2 = selected_obj[indexes[i][0]][5];
            sum_z2 = 1; vals_z2 = selected_obj[indexes[i][0]][6];
            object_name = selected_obj[indexes[i][0]][0]
        else:
            print("len(indexes[i]): " + str(len(indexes[i])))
            for j in range(len(indexes[i])):
                object_name = selected_obj[indexes[i][j]][0]
                sum_y1 = sum_y1 + selected_obj[indexes[i][j]][2]
                sum_z1 = sum_z1 + selected_obj[indexes[i][j]][3]
                sum_y2 = sum_y2 + selected_obj[indexes[i][j]][5]
                sum_z2 = sum_z2 + selected_obj[indexes[i][j]][6]
                vals_y1 = vals_y1 + (selected_obj[indexes[i][j]][2] ** 2)
                vals_z1 = vals_z1 + (selected_obj[indexes[i][j]][3] ** 2)
                vals_y2 = vals_y2 + (selected_obj[indexes[i][j]][5] ** 2)
                vals_z2 = vals_z2 + (selected_obj[indexes[i][j]][6] ** 2)
        vals_x1 = selected_obj[temp_indexes[i][0]][1]  # Here we take the x values of middle most of the smallest slice size(smallest of 20,30,40,50)
        vals_x2 = selected_obj[temp_indexes[i][0]][4]
        vals_y1 = vals_y1 / sum_y1; # were doing average of all the values here.
        vals_z1 = vals_z1 / sum_z1; # weightage for each instance is based on its contribution to the total sum
        vals_y2 = vals_y2 / sum_y2;
        vals_z2 = vals_z2 / sum_z2;
        real_coords.append([float(0.0), float(vals_x1), float(vals_y1), float(vals_z1)
                               , float(vals_x2), float(vals_y2), float(vals_z2)])
        all_unique_object_names.append([object_name])
    all_unique_objects.append(real_coords)
    # return all_unique_objects
    return real_coords, all_unique_object_names


# def cosine_similarity_filter(detected_objects_list):
#     data = pd.DataFrame(detected_objects_list,
#                           columns=['object_name', 'x1', 'y1', 'z1', 'x2', 'y2', 'z2', 'confidence', 'image_name'])
#
#     # data = pd.read_csv('detected_data_all.csv')
#     print('this is data')
#     print(data)
#     objects_detected = data.object_name.unique()
#
#     for obj_name in objects_detected:
#         selected_obj = data.loc[data['object_name'] == obj_name].to_numpy()
#         match = []
#         detection_matrix = []
#         for i in range(selected_obj.shape[0]):
#             for j in range(selected_obj.shape[0]):
#                 if cosine_similarity(list(selected_obj[:, 1:7][i]), list(selected_obj[:, 1:7][j])) >= 0.95:
#                     match.append(cosine_similarity(list(selected_obj[:, 1:7][i]), list(selected_obj[:, 1:7][j])))
#                 else:
#                     match.append(int(0))
#             detection_matrix.append(match)
#             match = []
#         detection_matrix = np.asarray(detection_matrix)
#         # print("########detection_matrix###########")
#         # print(np.asarray(detection_matrix))
#         indexes = []
#         count = 0
#         for i in range(detection_matrix.shape[0]):
#             if count == selected_obj.shape[0]:
#                 break
#             else:
#                 temp_indexes = np.nonzero(detection_matrix[i])
#                 indexes.append(temp_indexes[0].tolist())
#                 count = count + len(indexes[i])
#         real_coords = []
#         # print("########objects_and_coords###########")
#         unique = wt_avg(indexes, selected_obj)
#         # print(unique)
#         print('\n')
#         flat_list = [item for sublist in unique for item in sublist]
#         print(np.asarray(flat_list))
#         return flat_list
#

# data = pd.DataFrame(list, columns=['object_name', 'x1', 'y1', 'z1', 'x2', 'y2', 'z2', 'confidence', 'image_name'])

def catch_unique(list_in):
   unq_list = []
   for x in list_in:
      if x not in unq_list:
         unq_list.append(x)
   return unq_list


def cosine_filter(detected_data_all):
    # execution_path = os.getcwd()
    # data = pd.read_csv(execution_path + '\\output\\'+ filename + '.csv')
    data = detected_data_all # detected_data_all is a pandas dataframe
    # print('this is data')
    # print(data)
    objects_detected = data.object_name.unique()
    print("object classes detected are: ")
    print(objects_detected)
    unique = 0
    for obj_name in objects_detected:
        selected_obj = data.loc[data['object_name'] == obj_name].to_numpy()
        print("selected_obj = " + str(selected_obj))
        match = []
        detection_matrix = []
        for i in range(selected_obj.shape[0]):
            for j in range(selected_obj.shape[0]):
                if cosine_similarity(selected_obj[:, 1:7][i].tolist(), selected_obj[:, 1:7][j].tolist()) >= 0.95:
                    # match.append(cosine_similarity(selected_obj[:, 1:7][i].tolist(), selected_obj[:, 1:7][j].tolist()))
                    match.append(int(1))
                else:
                    match.append(int(0))
            detection_matrix.append(match)
            match = []
        detection_matrix = np.asarray(detection_matrix)
        print("########detection_matrix###########")
        print(obj_name)
        print(np.asarray(detection_matrix))
        indexes = []
        for i in range(detection_matrix.shape[0]):
            count = 0
            # count = count + len(np.nonzero(detection_matrix[i])[0].tolist())
            if count <= selected_obj.shape[0]:
                temporary_holder = np.nonzero(detection_matrix[i])
                print("len of temporary holder is : " + str(len(temporary_holder[0].tolist())))
                indexes.append(temporary_holder[0].tolist())
                print("indexes inside the loop is: " + str(indexes))
                len_before_unique = len(indexes)
                indexes = catch_unique(indexes)
                len_after_unique = len(indexes)
                # myset = set(indexes)
                # indexes = list(myset)
                print("unique vals in indexes : " + str(indexes))
                # print(type(indexes), type(indexes[0]))
                # print(i)
                # print(len(indexes)); print(len(indexes[i]))
                # print(selected_obj.shape)
                if len_before_unique != len_after_unique:
                    last_added = len(indexes) - 1
                    count = count + int(len(indexes[last_added]))
                    print(count)
                # if len(temporary_holder.tolist()) == selected_obj.shape[0]:
                #     indexes = list([indexes])
                # indexes = np.arange(selected_obj.shape[0]).tolist() #i shouldn't have done this

            else:
                break

        real_coords = []
        # print("######## objects_and_coords ################### objects_and_coords ################### objects_and_coords ###########")
        # indexes = np.unique(indexes)
        # print('indexes before no.asarray :')
        print(indexes)
        print(type(indexes), type(indexes[0]))
        # for i, value in enumerate(indexes):
        #     indexes[i] = np.asarray(value)
        # print('indexes after np.asarray :')
        # print(indexes)
        # if type(indexes[0]) != list:
        #     indexes = np.array((indexes.tolist))
        # print('indexes 3')
        # print(indexes)
        unique, names = wt_avg(indexes, selected_obj)
        print(names)
        # print("######## objects_and_coords ################### objects_and_coords ################### objects_and_coords ###########")
        # print('\n')
    # flat_list = [item for sublist in unique for item in sublist]
    # print(unique)
    # print(np.asarray(flat_list))
    return np.asarray(unique), np.asarray(names)

# import csv
#
# with open('detected_data_all.csv', newline='') as f:
#     reader = csv.reader(f)
#     list = [tuple(row) for row in reader]
# print(list)
# print(list[1:])
# list = list[1:]
# # list = cosine_similarity_filter(data)
# flat_l = game(list)
# print(flat_l)
