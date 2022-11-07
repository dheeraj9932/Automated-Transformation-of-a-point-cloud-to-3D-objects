import trimesh
import numpy as np
import pandas as pd

scale_list = pd.read_csv('unique.csv')
np = np.asarray(scale_list.values)
print(np)

for i, value in enumerate(np):
    volume = (value[4]-value[1])*(value[5]-value[2])*(value[3]-value[6])
    name = str((scale_list.iloc[i].values)[0])
    bb= (scale_list.iloc[i].values)[1:]
    corner_1 = bb[0:3]
    corner_2 = bb[3:]
    test = scale_list.iloc[i].values
    # volume1 = (test[4]-test[1])*(test[5]-test[2])*(test[3]-test[6]); print(volume1)
    center = [((test[4]+test[1])/2), ((test[5]+test[2])/2),((test[3]+test[6])/2)]; print("center is = "+ str(center))
    print('\n')
    transformation = [[1,0,0,center[0]],[0,1,0,center[1]],[0,0,1,center[2]],[0,0,0,0]]
    extent = [abs(corner_2[0]-corner_1[0]), abs(corner_2[1]-corner_1[1]), abs(corner_2[2]-corner_1[2])]
    template = trimesh.creation.box(extent, transformation)
    # template.visual.face_colors = [20, 200, 20]
    template.show()
    ply_file_content = trimesh.exchange.ply.export_ply(template, encoding='ascii', vertex_normal=None, include_attributes=True)
    name_of_file = str(name)+str("_")+str(i)
    f = open(name_of_file + ".ply", "wb")
    f.write(ply_file_content)
    f.close()
