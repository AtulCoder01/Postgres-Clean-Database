import psycopg2
from texttable import Texttable

creds = {
    "db_name": "postgres",
    "db_user": "postgres",
    "db_password": "password",
    "db_host": "postgresql",
    "db_port": "5432",
    "no_of_column": 3,
    "table_max_width": 160,
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

def execute_query(conn, query):
    cursor = conn.cursor()
    cursor.execute(f"{query}")
    conn.commit()
    data = cursor.fetchall()
    if len(data) > 0:
        columns = [desc[0] for desc in cursor.description]
        for col in columns:
            print('*'+str(col)+'*', end="\t")
        print()
        for dt in list(data):
            for d in dt:
                print(str(d), end="\t")
            print()
    else:
        print("no records found.")

def find_left_table(columns, max_length_tb):
    tmp = columns
    while True:
        if tmp >= max_length_tb:
            return tmp-max_length_tb
        else:
            tmp += columns

def show_tables(tables, columns, max_length_tb):
    new_table = [ f"{i+1}. {tb}" for i, tb in enumerate(tables)]
    left_table = find_left_table(columns, max_length_tb)
    i = 0
    while i < left_table:
        new_table.append("")
        i += 1
    new_max_length_tb = len(new_table)
    t = Texttable(max_width= creds["table_max_width"])
    
    col_head = []
    for k in range(columns):
        col_head.append(f"Column {k+1}")
    tem = [col_head]
    i = 0
    j = columns
    while j <= new_max_length_tb:
        tem.append(new_table[i:j])
        i += columns
        j += columns

    t.add_rows(tem)
    print(t.draw())

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
columns = creds["no_of_column"]
max_length_tb += 30
copy_tables = tables.copy()


print("\nAll Tables:\n")
show_tables(tables, columns, max_length_tb)

while True:
    print("\n0. For exit")
    print("1. Search the tables")
    print("2. Reset serach tables")
    print("3. Show tables")
    print("4. Enter table number for make empty e.g 0 for all / 1, 2, 3,4...")
    print("5. Execute Query\n")
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
    elif i == "5":
        query = None
        while query not in ["exit", "exit()"]:
            if query is None:
                cursor = conn.cursor()
                cursor.execute('SELECT version()')
                data = cursor.fetchone()
                conn.commit()
                print(data[0])
                print()

            query = input("sql\> ")

            if query == "exit":
                break

            try:
                execute_query(conn, query)
                print()
            except Exception as e:
                print(e)
    else:
        print("Wrong option. please try again")
    

#Closing the connection
conn.close()
