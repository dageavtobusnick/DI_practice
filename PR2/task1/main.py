import os
import numpy as np
import json

text_var = 'matrix_92.npy'
file = os.path.join(os.path.dirname(__file__), os.path.normpath(text_var))
result = os.path.join(os.path.dirname(__file__), os.path.normpath('result.txt'))
mat_norm = os.path.join(os.path.dirname(__file__), os.path.normpath('norm_matrix.npy'))

matrix = np.load(file)
matrix = matrix.astype('float')

matrix_inf = {}
def count_matrix_info(matrix):
    result={}
    result['sum'] = np.sum(matrix)
    result['avr'] = result.get('sum') / matrix.size
    result["sumMD"] = np.trace(matrix)
    result['avrMD'] = result.get('sumMD')/ matrix.shape[0]
    sumSD = 0
    k = matrix.shape[0] - 1
    for i in range(matrix.shape[0]):
        sumSD += matrix[i][k]
        k -= 1
    result["sumSD"] = sumSD
    result['avrSD'] =result.get('sumSD') / matrix.shape[0]
    result['max'] = matrix.max()
    result['min'] = matrix.min()
    
    return result

matrix_inf=count_matrix_info(matrix)

with open(result, 'w') as res:
    res.write(json.dumps(matrix_inf))

matrix_norm = matrix / matrix_inf.get('sum')

np.save(mat_norm, matrix_norm)