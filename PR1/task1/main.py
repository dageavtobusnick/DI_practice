import os

text_var = 'text_1_var_92'
file = os.path.join(os.path.dirname(__file__), os.path.normpath(text_var))
result = os.path.join(os.path.dirname(__file__), os.path.normpath('result.txt'))


with open(file) as f:
    text = f.readlines()
text = ' '.join(text)

def remove_signs(line):
    mask = '!?,.'
    mask_2 = '\n'
    for i in mask:
        line = line.replace(i, ' ')
    line = line.replace(mask_2, ' ')
    while "  " in line:
        line = line.replace('  ', ' ')
    line = line.lower()
    return line.split()

def count_frequency(data):
    result = {}
    for i in data:
        if i in result:
                result[i] += 1
        else:
                result[i] = 1
    return result

lines = remove_signs(text)

words_dict=count_frequency(lines)

words_dict_sort = dict(sorted(words_dict.items(), reverse=True, key=lambda x: x[1]))

with open(result, 'w') as res:
    for key, value in words_dict_sort.items():
        res.write(key + ':' + str(value) + '\n')