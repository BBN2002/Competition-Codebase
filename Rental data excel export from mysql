import pandas as pd
import pymysql
import time

# MySQL database connection configuration
db_config = {
    'host': '123.57.92.58',
    'port': 3306,
    'user': '租房数据',
    'password': 'Kingho325',
    'database': '租房数据',
    'charset': 'utf8'
}

# Connect to a MySQL database
conn = pymysql.connect(**db_config)

# Read data from the database
query = "SELECT * FROM 租房数据"
df = pd.read_sql(query, conn)

# Save the data to an Excel file
excel_file = "Rental Data.xlsx"
df.to_excel(excel_file, index=False)

# Close the database connection
conn.close()

print("The data has been successfully exported to an Excel file:", excel_file)

# Set up a scheduled task
delay = 3600
time.sleep(delay)
print('Next')
