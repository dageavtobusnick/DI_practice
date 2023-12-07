import json
import pickle
import os

text_var = 'products_92.pkl'
file_products = os.path.join(os.path.dirname(__file__), os.path.normpath(text_var))
text_var = 'price_info_92.json'
file_change = os.path.join(os.path.dirname(__file__), os.path.normpath(text_var))

result = os.path.join(os.path.dirname(__file__), os.path.normpath('result.pkl'))

def update_price(product, price_info):
    method = price_info["method"]
    if method == "sum":
        product["price"] += price_info["param"]
    elif method == "sub":
        product["price"] -= price_info["param"]
    elif method == "percent+":
        product["price"] *= (1 + price_info["param"])
    elif method == "percent-":
        product["price"] *= (1 - price_info["param"])
    product["price"] = round(product["price"], 2)



with open(file_products, "rb") as f:
    products = pickle.load(f)

with open(file_change) as f:
    price_info = json.load(f)


price_info_dict = dict() 

for item in price_info:
    price_info_dict[item["name"]] = item

for product in products:
    current_price_info = price_info_dict[product["name"]]
    update_price(product, current_price_info)

with open(result , "wb") as f:
    f.write(pickle.dumps(products))
