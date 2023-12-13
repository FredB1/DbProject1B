import sqlite3

def create_connection(db_file):
    """Create a database connection to the SQLite database specified by db_file"""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

def update_record(conn, table, column_to_update, new_value, key_column, key_value):
    """ Generic function to update a record in a table """
    sql = f'UPDATE {table} SET {column_to_update} = ? WHERE {key_column} = ?'
    cur = conn.cursor()
    cur.execute(sql, (new_value, key_value))
    conn.commit()

def main():
    database = "pythonsqlite.db"
    conn = create_connection(database)

    if conn is not None:
        table = input("Enter the table name to update: ")
        column_to_update = input(f"Enter the column name in {table} to update: ")
        new_value = input(f"Enter the new value for {column_to_update}: ")
        key_column = input(f"Enter the key column name in {table} to match: ")
        key_value = input(f"Enter the value of {key_column} to update: ")
        update_record(conn, table, column_to_update, new_value, key_column, key_value)

    else:
        print("Error! cannot create the database connection.")

if __name__ == '__main__':
    main()
