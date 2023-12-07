import os
text_var = 'text_2_var_92'
file = os.path.join(os.path.dirname(__file__), os.path.normpath(text_var))
result = os.path.join(os.path.dirname(__file__), os.path.normpath('result.txt'))

with open(file) as f:
    text = f.readlines()

def count_sum(data):
    average = []
    for line in data:
        n = line.split(',')
        sum_n = 0
        for i in n:
            sum_n += int(i)
        average.append(sum_n)
    return average
    
sums=count_sum(text)
with open(result, 'w') as res:
    for value in sums:
        res.write(str(value) + '\n')