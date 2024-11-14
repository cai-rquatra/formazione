import mysql.connector
from mysql.connector import Error

def create_connection():
    """Establishes a connection to the MySQL database."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="user",
            password="user_password",
            database="example_db",
            port="8881"
        )
        if connection.is_connected():
            print("Connection successful!")
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

def insert_data(connection, name, age):
    """Inserts a new row into the users table."""
    try:
        cursor = connection.cursor()
        sql_insert_query = """
        INSERT INTO users (name, age) 
        VALUES (%s, %s)
        """
        cursor.execute(sql_insert_query, (name, age))
        connection.commit()
        print("Data inserted successfully!")
    except Error as e:
        print(f"Error: {e}")

def read_data(connection):
    """Fetches all rows from the users table."""
    try:
        cursor = connection.cursor()
        sql_select_query = "SELECT * FROM users"
        cursor.execute(sql_select_query)
        rows = cursor.fetchall()
        print("Data fetched successfully!")
        for row in rows:
            print(f"ID: {row[0]}, Name: {row[1]}, Age: {row[2]}")
    except Error as e:
        print(f"Error: {e}")

def main():
    # Create a database connection
    connection = create_connection()
    
    # Insert data into the database
    if connection:
        insert_data(connection, "Alice", 25)
        insert_data(connection, "Bob", 30)

        # Read data from the database
        read_data(connection)

        # Close the connection
        connection.close()

if __name__ == "__main__":
    main()
