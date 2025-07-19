import sqlite3

# Connect to SQLite (replace with your own DB connection for PostgreSQL/MySQL etc.)
conn = sqlite3.connect('training.db')

cursor = conn.cursor()


#Select records from table trainings -------------------------------------------------------------------------------------------------

# cursor.execute("Select * from trainings")

# rows = cursor.fetchall()
# for row in rows:
#     print(row)


#-------------------------------------------------------------------------------------------------
import json
# Load JSON data
with open('employee.json', 'r') as file:
    employees = json.load(file)

# Convert JSON data to tuple format for SQLite
employee_data = [
    (
        emp['employee_id'],
        emp['employee_no'],
        emp['employee_name'],
        emp['emailid'],
        emp['manager_id'],
        emp['team_id'],
        emp['grade_id'],
        emp['discontinued'],
        emp['password'],
        emp['training_team']
    ) for emp in employees
]

# Insert query
insert_query = '''
    INSERT INTO employee (
        employee_id, employee_no, employee_name, emailid,
        manager_id, team_id, grade_id, discontinued, password, training_team
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
'''

print(employee_data)
cursor.executemany(insert_query, employee_data)


















# Commit and close
conn.commit()
conn.close()
