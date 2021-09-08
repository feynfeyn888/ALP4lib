import numpy as np

ny=3
nx=4
pre_sampling=5
any = np.arange(nx*ny*pre_sampling).reshape(ny,nx,pre_sampling)
print(any)

print("inverse")
print(any[:,::-1,::-1])
# np.random.seed(0)

# # Input Matrix(pre_sampling,)
# Input_Matrix_2d = np.random.randint(low=0,high=2,size=(pre_sampling,ny*nx))
# print(Input_Matrix_2d)

# Input_Matrix_3d = np.random.randint(low=0,high=2,size=(pre_sampling,ny,nx))
# print(Input_Matrix_3d)
# print(Input_Matrix_3d.shape)
# # padding
# Padding_Input_Matrix=np.pad(Input_Matrix_3d,[(0,0),(2,2),(2,2)],'constant')
# print(Padding_Input_Matrix)
# print(Padding_Input_Matrix.flatten())

# # 入力行列
# print(Input_Matrix_3d.reshape(pre_sampling,ny*nx).T)

