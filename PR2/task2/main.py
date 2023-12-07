import os
import numpy as np

text_var = 'matrix_92_2.npy'
my_file = os.path.join(os.path.dirname(__file__), os.path.normpath(text_var))
result = os.path.join(os.path.dirname(__file__), os.path.normpath('points.npz'))
res_zip = os.path.join(os.path.dirname(__file__), os.path.normpath('points_zip.npz'))

var = 92 

matrix = np.load(my_file)
matrix = matrix.astype('float')
def fill_arrays(x,y,z,matrix,filt): 
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            if matrix[i][j] > filt:
                x.append(i)
                y.append(j)
                z.append(matrix[i][j])

x = []
y = []
z = []

filt = 500 + var
fill_arrays(x,y,z,matrix,filt)

np.savez(result, x=x, y=y, z=z)
np.savez_compressed(res_zip, x=x, y=y, z=z)

print(f'points     = {os.path.getsize(result)}')
print(f'points_zip = {os.path.getsize(res_zip)}')
print(f'минимум = {min(os.path.getsize(res_zip),os.path.getsize(result))}')