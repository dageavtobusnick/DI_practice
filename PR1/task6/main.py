from bs4 import BeautifulSoup
import json
import os

str_json = ''
text_var = 'text_6_var_92'
file = os.path.join(os.path.dirname(__file__), os.path.normpath(text_var))
result = os.path.join(os.path.dirname(__file__), os.path.normpath('result.html'))
with open(file, encoding='utf-8') as file:
    lines = file.readlines()
    for line in lines:
        str_json += line

data = json.loads(str_json)
data = data['items']

soup = BeautifulSoup("""<table>

 </table>""", "html.parser")
table = soup.contents[0]
first_line=data[0]["quote"]
tr = soup.new_tag("tr")
for key,value in first_line.items():
    th = soup.new_tag("th")
    th.string=key
    tr.append(th)
table.append(tr)
for tick in data:
    tick=tick["quote"]
    tr = soup.new_tag("tr")
    for key, value in tick.items():
        td = soup.new_tag("td")
        print(key)
        print(value)
        if key=="tags":
            td.string=", ".join(list(value))
        else:
            td.string = str(value)
        tr.append(td)
    table.append(tr)

with open(result, 'w') as result:
    result.write(soup.prettify())
    result.write('\n')