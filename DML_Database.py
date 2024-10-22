import mysql.connector
from mysql.connector import Error
import datetime

# Creating/Checking the connection to SQL server
def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            password=user_password,
            database=db_name
        )
        if connection.is_connected():
            print("Connection to MySQL database was successful!")
    except Error as e:
        print(f"The error '{e}' occurred")
    
    return connection

# Function to Execute an INSERT, DELETE, or UPDATE query
def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
        print(f"Number of rows affected: {cursor.rowcount}")
    except Error as e:
        print(f"The error '{e}' occurred")
    finally:
        cursor.close()

# funtion for SELECT queries, prints the rows and then displays the number of rows retrieved.
def execute_select_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        rows = cursor.fetchall()

        for row in rows:
            formatted_row = list(row)  # Convert tuple to list for manipulation
            for i, col in enumerate(formatted_row):
                if isinstance(col, datetime.date):  # Check if the column is a date
                    formatted_row[i] = col.strftime("%Y-%m-%d")  # Format the date to 'YYYY-MM-DD'
            print(tuple(formatted_row))  # Convert list back to tuple and print

        print(f"Number of rows retrieved: {cursor.rowcount}")
    except Error as e:
        print(f"The error '{e}' occurred")
    finally:
        cursor.close()


# Function to show tables and their values
def show_tables_or_values(connection, show_input):
    try:
        cursor = connection.cursor()
        if show_input == "Table names":
            query = "SHOW TABLES"
            cursor.execute(query)
            tables = cursor.fetchall()
            for table in tables:
                print(table[0])
        elif show_input == "Table values":
            table_name = input("Enter your table name: ")
            query = f"DESCRIBE {table_name}"  # Shows column names for the required table
            cursor.execute(query)
            columns = cursor.fetchall()
            print("Columns:", [col[0] for col in columns])

            table_cond = input("Enter the condition for selection (e.g., id=1) or leave blank to select all: ")
            if table_cond:
                query = f"SELECT * FROM {table_name} WHERE {table_cond}"
            else:
                query = f"SELECT * FROM {table_name}"  # Select all records if no condition is provided
            execute_select_query(connection, query)
        else:
            print("Invalid option, please select either 'Table names' or 'Table values'")
    except Error as e:
        print(f"The error '{e}' occurred")
    finally:
        cursor.close()


# Function to delete rows or all rows from a table
def delete_tables_or_values(connection, delete_input):
    try:
        if delete_input == "Table names":
            table_name = input("Enter the table name to delete all rows from: ")
            query = f"DELETE FROM {table_name}"
            execute_query(connection, query)
        elif delete_input == "Table values":
            table_name = input("Enter the table name: ")
            query = f"DESCRIBE {table_name}"  # Shows column names for required table
            cursor = connection.cursor()
            cursor.execute(query)
            columns = cursor.fetchall()
            print("Columns:", [col[0] for col in columns])

            table_cond = input("Enter the condition for deletion (e.g., id=1): ")
            query = f"DELETE FROM {table_name} WHERE {table_cond}"
            execute_query(connection, query)
        else:
            print("Invalid option, please select either 'Table names' or 'Table values'")
    except Error as e:
        print(f"The error '{e}' occurred")


# Function to update values in a table
def update_tables_or_values(connection):
    try:
        table_name = input("Enter the table name to update: ")
        query = f"DESCRIBE {table_name}"  # Shows column names for the required table
        cursor = connection.cursor()
        cursor.execute(query)
        columns = cursor.fetchall()
        print("Columns:", [col[0] for col in columns])

        set_clause = input("Enter the values to update (e.g., name='John'): ")
        table_cond = input("Enter the condition for updating (e.g., id=1): ")
        query = f"UPDATE {table_name} SET {set_clause} WHERE {table_cond}"
        execute_query(connection, query)
    except Error as e:
        print(f"The error '{e}' occurred")


# Function to insert values into a table
def insert_values(connection):
    try:
        table_name = input("Enter the table name to insert: ")
        # Collect user inputs
        id = input("Enter ID: ")
        name = input("Enter Name: ")
        passport_number = input("Enter Passport Number: ")
        expiry_date = input("Enter Expiry Date (YYYY-MM-DD): ")
        status = input("Enter Status (Active/Expired): ")

        # Create the SQL query using placeholders to prevent SQL injection
        query = f"""
        INSERT INTO {table_name} (id, name, passport_number, expiry_date, status) 
        VALUES (%s, %s, %s, %s, %s)
        """

        cursor = connection.cursor()
        cursor.execute(query, (id, name, passport_number, expiry_date, status))
        connection.commit()
        print(f"Values inserted into {table_name}.")
        print(f"Number of rows affected: {cursor.rowcount}")
    except Error as e:
        print(f"The error '{e}' occurred")
    finally:
        cursor.close()


# Function to repeatedly ask for user commands until 'exit' is chosen
def user_operations(connection):
    while True:
        operation = input("Select an operation (Insert, Update, Delete, Show) or type 'exit' to quit: ").capitalize()
        if operation == "Show":
            show_input = input("Select the module to show (Table names/Table values): ").capitalize()
            show_tables_or_values(connection, show_input)
        elif operation == "Delete":
            delete_input = input("Select the module to delete (Table names/Table values): ").capitalize()
            delete_tables_or_values(connection, delete_input)
        elif operation == "Update":
            update_tables_or_values(connection)
        elif operation == "Insert":
            insert_values(connection)
        elif operation == "Exit":
            print("Exiting the program...")
            break
        else:
            print("Invalid option selected")


# Establishing the connection
host = "localhost"  # My server's IP address
user = "root"       # My MySQL Workbench username
password = "root"   # My MySQL Workbench password
database = "passport_details"  # My target database
connection = create_connection(host, user, password, database)

# Start the user operations loop
if connection:
    user_operations(connection)

# Close the connection when done
if connection.is_connected():
    connection.close()
    print("MySQL connection closed")
