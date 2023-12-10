import os
import msgpack
import sqlite3
import csv
import json

data_file_1 = os.path.join(os.path.dirname(__file__), os.path.normpath('Patient_Profile.csv'))
data_file_2 = os.path.join(os.path.dirname(__file__), os.path.normpath('Health_Camp_Detail.json'))
data_file_3 = os.path.join(os.path.dirname(__file__), os.path.normpath('Health_Camp_Attended.msgpack'))
res_file_charact_score = os.path.join(os.path.dirname(__file__), os.path.normpath('res_charact_score.json'))
res_file_popul_Category2 = os.path.join(os.path.dirname(__file__), os.path.normpath("res_popul_Category2.json"))
res_file_top_Age = os.path.join(os.path.dirname(__file__), os.path.normpath("res_top_Age.json"))
res_file_top_Category3 = os.path.join(os.path.dirname(__file__), os.path.normpath("res_top_Category3.json"))
res_file_Donation = os.path.join(os.path.dirname(__file__), os.path.normpath("res_Donation.json"))
res_file_Health_Score = os.path.join(os.path.dirname(__file__), os.path.normpath("res_Health_Score.json"))
res_file_Health_Camp= os.path.join(os.path.dirname(__file__), os.path.normpath("res_Health_Camp.json"))
db_file=os.path.join(os.path.dirname(__file__), os.path.normpath('db'))

def read_first(file_name):
    items = []
    with open(file_name, 'r', encoding='utf-8') as file:
        data = csv.reader(file, delimiter=',')
        data.__next__()
        
        for row in data:
            if len(row) == 0: 
                continue
            item = dict()
            item['Patient_ID'] = int(row[0])
            item['Online_Follower'] = int(row[1])
            item['LinkedIn_Shared'] = bool(row[2])
            item['Twitter_Shared'] = bool(row[3])
            item['Facebook_Shared'] = bool(row[4])
            if row[5] != 'None':
                item['Income'] = int(row[5])
            else:
                item['Income']=None
            if row[6] != 'None':
                item['Education_Score'] = float(row[6])
            else:
                item['Education_Score']=None
            if row[7] != 'None':
                item['Age'] = int(row[7])
            else:
                item['Age']=None
            if row[5] != '':
                item['First_Interaction'] = row[8]
            else:
                item['First_Interaction']=None
            if row[5] != '':
                item['City_Type'] = row[9]
            else:
                item['City_Type']=None
            if row[5] != '':
                item['Employer_Category'] = row[10]
            else:
                item['Employer_Category']=None
            items.append(item)
    return items

def read_second(file_name):
    with open(file_name, 'rb') as file:
        data=json.loads(file.read())
        return data

def read_third(file_name):
    with open(file_name, 'rb') as file:
        content = file.read()
        data = msgpack.unpackb(content)
        return data

def create_first_table(db):
    cursor = db.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS patients(
   Patient_ID INTEGER PRIMARY KEY,
   Online_Follower INTEGER,
   LinkedIn_Shared INTEGER,
   Twitter_Shared INTEGER,
   Facebook_Shared INTEGER,
   Income INTEGER DEFAULT NULL,
   Education_Score REAL DEFAULT NULL,
   Age INTEGER DEFAULT NULL,
   First_Interaction TEXT DEFAULT NULL,
   City_Type TEXT DEFAULT NULL,
   Employer_Category TEXT DEFAULT NULL);
""")
    db.commit()

def create_second_table(db):
    cursor = db.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS camps(
   Health_Camp_ID INTEGER PRIMARY KEY,
   Camp_Start_Date TEXT,
   Camp_End_Date TEXT,
   Category1 TEXT,
   Category2 TEXT,
   Category3 INTEGER);
""")
    db.commit()

def create_third_table(db):
    cursor = db.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS attended(
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   Patient_ID INTEGER,
   Health_Camp_ID INTEGER,
   Donation INTEGER,
   Health_Score REAL,
   FOREIGN KEY (Patient_ID)  REFERENCES patients (Patient_ID),
   FOREIGN KEY (Health_Camp_ID)  REFERENCES camps (Health_Camp_ID));
""")
    db.commit()
    
def connect_to_db(file_name):
    connection = sqlite3.connect(file_name)
    connection.row_factory = sqlite3.Row
    return connection

def insert_first_data(db, data):
    cursor = db.cursor()
    cursor.executemany("""
        INSERT INTO patients (Patient_ID, Online_Follower, LinkedIn_Shared, Twitter_Shared, Facebook_Shared, Income, Education_Score,Age,First_Interaction,City_Type,Employer_Category) 
        VALUES(:Patient_ID, :Online_Follower, :LinkedIn_Shared, :Twitter_Shared, :Facebook_Shared, :Income, :Education_Score,:Age,:First_Interaction,:City_Type,:Employer_Category)""", data)
    db.commit()

def insert_second_data(db, data):
    cursor = db.cursor()
    cursor.executemany("""
        INSERT INTO camps (Health_Camp_ID, Camp_Start_Date, Camp_End_Date, Category1, Category2, Category3) 
        VALUES(:Health_Camp_ID, :Camp_Start_Date, :Camp_End_Date, :Category1, :Category2, :Category3)""", data)
    db.commit()
    
def insert_third_data(db, data):
    cursor = db.cursor()
    cursor.executemany("""
        INSERT INTO attended (Patient_ID, Health_Camp_ID, Donation, Health_Score) 
        VALUES(:Patient_ID, :Health_Camp_ID, :Donation, :Health_Score)""", data)
    db.commit()
    
def top_Age(db, limit,value):
    cursor = db.cursor()
    res = cursor.execute("SELECT * FROM patients WHERE City_Type=?  ORDER BY Age DESC LIMIT ?", [value,limit])
    items = []
    for row in res.fetchall():
        item = dict(row)
        items.append(item)
    cursor.close()
    return items

def top_Category3(db, limit,value):
    cursor = db.cursor()
    res = cursor.execute("SELECT * FROM camps WHERE Category1=? ORDER BY Category3 DESC LIMIT ?", [value,limit])
    items = []
    for row in res.fetchall():
        item = dict(row)
        items.append(item)
    cursor.close()
    return items
    
def charact_score(db):
    cursor = db.cursor()
    items = []
    res = cursor.execute("""
        SELECT 
            SUM(Education_Score) as sum,
            AVG(Education_Score) as avg,
            MIN(Education_Score) as min, 
            MAX(Education_Score) as max
        FROM patients
                        """)
    for row in res.fetchall():
        items.append(dict(row))
    cursor.close()
    return items

def popul_Category2(db):
    cursor = db.cursor()
    items = []
    res = cursor.execute("""
        SELECT 
            CAST(COUNT(*) as REAL) / (SELECT COUNT(*) FROM camps) as count,
            Category2
        FROM camps
        GROUP BY Category2
                        """)
    for row in res.fetchall():
        items.append(dict(row))
    return items

def group_Donation(db):
    cursor = db.cursor()
    items = []
    res = cursor.execute("""
        SELECT 
            *
        FROM attended
        JOIN camps ON attended.Health_Camp_ID= camps.Health_Camp_ID
        GROUP BY Donation
                        """)
    for row in res.fetchall():
        items.append(dict(row))
    return items

def group_Health_Score(db):
    cursor = db.cursor()
    items = []
    res = cursor.execute("""
        SELECT 
            *
        FROM attended
        JOIN patients ON attended.Patient_ID = patients.Patient_ID
        GROUP BY Health_Score
                        """)
    for row in res.fetchall():
        items.append(dict(row))
    return items

def group_Health_Camp(db):
    cursor = db.cursor()
    items = []
    res = cursor.execute("""
        SELECT 
            *
        FROM attended
        JOIN patients ON attended.Patient_ID = patients.Patient_ID
        JOIN camps ON attended.Health_Camp_ID= camps.Health_Camp_ID
        WHERE Donation>(SELECT AVG(Donation) FROM attended)
        GROUP BY Employer_Category
                        """)
    for row in res.fetchall():
        items.append(dict(row))
    return items

# first_data=read_first(data_file_1)
# second_data=read_second(data_file_2)
# third_data=read_third(data_file_3)

db = connect_to_db(db_file)

# create_first_table(db)
# insert_first_data(db,first_data)
# create_second_table(db)
# insert_second_data(db,second_data)
# create_third_table(db)
# insert_third_data(db,third_data)

top_Age_data=top_Age(db,10,'I')
top_Age_Category3_data=top_Category3(db,5,'Second')
charact_score_data=charact_score(db)
popul_Category2_data=popul_Category2(db)
group_Health_Score_data=group_Health_Score(db)
group_Donation_data=group_Donation(db)
group_Health_Camp_data=group_Health_Camp(db)
with open(res_file_top_Age, 'w', encoding='utf-8') as f:
    f.write(json.dumps(top_Age_data, ensure_ascii=False))
with open(res_file_top_Category3, 'w', encoding='utf-8') as f:
    f.write(json.dumps(top_Age_Category3_data, ensure_ascii=False))
with open(res_file_charact_score, 'w', encoding='utf-8') as f:
    f.write(json.dumps(charact_score_data, ensure_ascii=False))
with open(res_file_popul_Category2, 'w', encoding='utf-8') as f:
    f.write(json.dumps(popul_Category2_data, ensure_ascii=False))
with open(res_file_Donation, 'w', encoding='utf-8') as f:
    f.write(json.dumps(group_Donation_data, ensure_ascii=False))
with open(res_file_Health_Score, 'w', encoding='utf-8') as f:
    f.write(json.dumps(group_Health_Score_data, ensure_ascii=False))
with open(res_file_Health_Camp, 'w', encoding='utf-8') as f:
    f.write(json.dumps(group_Health_Camp_data, ensure_ascii=False))