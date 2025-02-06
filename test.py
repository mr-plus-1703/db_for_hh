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

df = pd.read_excel("filtr_for_id_all.xlsx")


print(df.columns)

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


# Сохранение изменений и закрытие соединения
connection.commit()
connection.close()