import numpy as np

def isolate_parent(parent_np, unique_detections):
    list = []
    for i in range(unique_detections.shape[0]):
        mask_x = np.logical_and(float(unique_detections[i][4]) > parent_np[:,0] , parent_np[:,0] > float(unique_detections[i][1]))
        mask_y = np.logical_and(float(unique_detections[i][5]) > parent_np[:,1] , parent_np[:,1] > float(unique_detections[i][2]))
        mask_z = np.logical_and(float(unique_detections[i][6]) < parent_np[:,2] , parent_np[:,2] < float(unique_detections[i][3]))
        mask = np.logical_and(np.logical_and(mask_x, mask_y), mask_z)
        list.append(mask)
    temp = list # temp = [[1,0,0,0,1,1,...1,0,1],[1,0,0,0,1,1,...1,0,1]...[1,0,0,0,1,1,...1,0,1]]
    new_array = (np.where(temp[0])[0]) # indexes where 0's are there in temp[0]
    for i, value in enumerate(temp):
        if i != 0:
            new_array = np.unique(np.concatenate((new_array, (np.where(temp[i])[0])), axis=0)) # new_array = indexes of all 0's given all conditions
    temp_np = np.delete(parent_np, obj=new_array, axis=0) # the zero indexes represent the points inside the Bounding Box
    return temp_np
