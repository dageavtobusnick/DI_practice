import os

var = 92
text_var = 'text_3_var_92'
file = os.path.join(os.path.dirname(__file__), os.path.normpath(text_var))
result = os.path.join(os.path.dirname(__file__), os.path.normpath('result.txt'))

with open(file) as f:
    text = f.readlines()

def filter_values(data):
    result=[]
    for line in data:
        n = line.split(',')
        numbers = []
        for i in range(len(n)):
            if n[i] == 'NA':
                temp = (int(n[i - 1]) + int(n[i + 1])) / 2
                if temp ** 2 >= (50 + var) ** 2:
                    numbers.append(str(temp))
                else:
                    temp = int(n[i])
                    if temp ** 2 >= (50 + var) ** 2:
                        numbers.append(str(temp))
        result.append(numbers)
    return result

filter_str = filter_values(text)

with open(result, 'w') as res:
    for value in filter_str:
        s = ', '.join(value)
        res.write(s + '\n')