import sqlite3
import pandas as pd

'''
     _______
    |       |
    |       |
    |       |
    |       |
    |_______|

    _______
   |       |
   |       |
   |       |
   |_______|

  __________
 /         \
|          |
 \_________/

  __________
 /         \
|          |
 \_________/

  __________
 /         \
|          |
 \_________/

  _______
 /       \
|        |
 \______/
'''

connection = sqlite3.connect("hh.db")

cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS vacancies (
        id INTEGER, 
        name TEXT, 
        education TEXT, 
        salary_min INTEGER, 
        salary_max INTEGER, 
        experience_min DATE, 
        employer TEXT
    );""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS vacancy_skills (
        id INTEGER, 
        skill TEXT
    );""")

df = pd.read_excel("exl/filtr_for_id_all.xlsx")


for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO vacancies (id, name, salary_min, salary_max, experience_min, employer) 
        VALUES (?, ?, ?, ?, ?, ?);
    """, (
        row["id"], 
        row["name"], 
        row["salary_min"], 
        row["salary_max"], 
        row["experience_min"], 
        row["employer"]
    ))

    if type(row["skills"]) is not str:
        continue

    for skill in row["skills"][1:-1].split(', '): 
        cursor.execute("""
            INSERT INTO vacancy_skills (id, skill) 
            VALUES (?, ?);
        """, (
            row["id"], 
            skill,
        ))



# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

df = pd.read_excel("exl/MRSK+PCBK_new_sills.xlsx")

for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO vacancies (id, name, education, experience_min) 
        VALUES (?, ?, ?, ?);
    """, (
        row["id"], 
        row["name"], 
        row["education"], 
        row["experience_min"], 
    ))
    
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

df = pd.read_excel("exl/MRSK+PCBK_id_skills.xlsx")
for _, row in df.iterrows():
    cursor.execute("""
                INSERT INTO vacancy_skills (id, skill) 
                VALUES (?, ?);
            """, (
                row["id"], 
                row["skills"],
            ))



connection.commit()
connection.close()