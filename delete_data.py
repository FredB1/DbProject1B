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

def delete_record(conn, table, column, value):
    """ Generic function to delete a record from a table """
    sql = f'DELETE FROM {table} WHERE {column} = ?'
    cur = conn.cursor()
    cur.execute(sql, (value,))
    conn.commit()

def main():
    database = "pythonsqlite.db"
    conn = create_connection(database)

    if conn is not None:
        table = input("Enter the table name to delete from: ")
        column = input(f"Enter the column name in {table} to match: ")
        value = input(f"Enter the value of {column} to delete: ")
        delete_record(conn, table, column, value)

    else:
        print("Error! cannot create the database connection.")

if __name__ == '__main__':
    main()
