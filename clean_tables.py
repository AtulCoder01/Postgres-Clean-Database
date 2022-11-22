import psycopg2
from copy import deepcopy

creds = {
    "db_name": "postgres",
    "db_user": "postgres",
    "db_password": "password",
    "db_host": "postgresql",
    "db_port": "5432",
}

def empty_table(conn, tables, num_list):
    cursor = conn.cursor()
    for n_l in num_list:
        if int(n_l) == 0:
            confirm = input("Do you want to truncate all the tables?[y|N] ")
            if confirm.lower() in ["y", "yes"]:
                t = 1
                print()
                for tb in tables:
                    cursor.execute(f"TRUNCATE TABLE {tb} CASCADE")
                    conn.commit()
                    print(f"Table {t}. {tb} is cleared... Done!")
                    t += 1
                print(f"All Tables are cleared... Done!")
                break
        else:
            tb = tables[int(n_l)-1]
            cursor.execute(f"TRUNCATE TABLE {tb} CASCADE")
            conn.commit()
            print(f"Table {n_l}. {tb} is cleared... Done!")

def show_tables(tables, columns, max_length_tb):
    n = 1
    if len(tables) == 1:
        for first in zip(tables[::columns]):
            first = f"{n}. {first[0]}"
            n+=1
            print(f'{first}')      
    elif len(tables) == 2: 
        for first, second in zip(tables[::columns], tables[1::columns]):
            first = f"{n}. {first}"
            n+=1
            second = f"{n}. {second}"
            n+=1
            print(f'{first: <{max_length_tb}}{second}')       
    else: 
        for first, second, third in zip(tables[::columns], tables[1::columns], tables[2::columns]):
            first = f"{n}. {first}"
            n+=1
            second = f"{n}. {second}"
            n+=1
            third = f"{n}. {third}"
            n+=1
            print(f'{first: <{max_length_tb}}{second: <{max_length_tb}}{third}')       

#establishing the connection
conn = psycopg2.connect(database = creds["db_name"], user = creds["db_user"], password = creds["db_password"], host = creds["db_host"], port = creds["db_port"])
#Creating a cursor object using the cursor() method
cursor = conn.cursor()

#Executing an MYSQL function using the execute() method
cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
# Fetch a single row using fetchone() method.
all_tables = cursor.fetchall()
max_length_tb = 0
tables = []
for table in all_tables:
    tables.append(table[0])
    if len(table[0]) > 0:
        max_length_tb = len(table[0])
columns = 3
max_length_tb += 30
copy_tables = deepcopy(tables)


print("\nAll Tables:\n")
show_tables(tables, columns, max_length_tb)

while True:
    print("\n0. For exit")
    print("1. Search the tables")
    print("2. Reset serach tables")
    print("3. Show tables")
    print("4. Enter table number for make empty e.g 0 for all / 1, 2, 3,4...\n")
    i = input("Choose one option:> ")
    if i == "0":
        break
    elif i == "1":
        search = input("Enter the search key:> ")
        tables = [ c_t for c_t in tables if search in c_t ]
        print()
        show_tables(tables, columns, max_length_tb)
    elif i == "2":
        tables = copy_tables
        show_tables(tables, columns, max_length_tb)
    elif i == "3":
        show_tables(tables, columns, max_length_tb)
    elif i == "4":
        num = input("Enter table number:> ")
        print()
        num_list = num.split(",")
        empty_table(conn, tables, num_list)
    else:
        print("Wrong option. please try again")
    

#Closing the connection
conn.close()
