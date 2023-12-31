import sqlite3
import datetime
def create_connection(db_file):
    """Create a database connection to the SQLite database specified by db_file"""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def list_books_borrowed_by_individual(conn, member_id):
    """ List of all books borrowed by an individual """
    sql = '''
    SELECT b.Title, b.Author, l.ChkOut_Date, l.Due_Date
    FROM Book b
    JOIN Copy c ON b.ISBN = c.ISBN
    JOIN Loan l ON c.ISBN = l.ISBN AND c.Copy_Num = l.Copy_Num
    JOIN Member m ON l.M_ID = m.M_ID
    WHERE m.M_ID = ?
    '''
    cur = conn.cursor()
    cur.execute(sql, (member_id,))
    books = cur.fetchall()
    for book in books:
        print(book)

def report_overdue_books(conn):
    """ Report of overdue books """
    sql = '''
    SELECT m.Name, b.Title, l.Due_Date
    FROM Loan l
    JOIN Member m ON l.M_ID = m.M_ID
    JOIN Copy c ON l.ISBN = c.ISBN AND l.Copy_Num = c.Copy_Num
    JOIN Book b ON c.ISBN = b.ISBN
    WHERE l.Ret_Date IS NULL AND l.Due_Date < CURRENT_DATE
    '''
    cur = conn.cursor()
    cur.execute(sql)
    overdue_books = cur.fetchall()
    for book in overdue_books:
        print(book)

def total_books_loaned_out_by_category(conn):
    """ Total number of books loaned out by category """
    sql = '''
    SELECT b.Sub_Area, COUNT(*) as TotalLoans
    FROM Loan l
    JOIN Copy c ON l.ISBN = c.ISBN AND l.Copy_Num = c.Copy_Num
    JOIN Book b ON c.ISBN = b.ISBN
    WHERE l.Ret_Date IS NULL
    GROUP BY b.Sub_Area
    '''
    cur = conn.cursor()
    cur.execute(sql)
    loans_by_category = cur.fetchall()
    for category in loans_by_category:
        print(category)

def list_inactive_members(conn):
    """ List of inactive members """
    sql = '''
    SELECT m.M_ID, m.Name
    FROM Member m
    LEFT JOIN Loan l ON m.M_ID = l.M_ID
    WHERE l.Loan_ID IS NULL
    '''
    cur = conn.cursor()
    cur.execute(sql)
    inactive_members = cur.fetchall()
    for member in inactive_members:
        print(member)

def most_popular_books(conn):
    """ Query to find the most popular books """
    sql = '''
    SELECT b.Title, b.Author, COUNT(l.Loan_ID) as TotalLoans
    FROM Loan l
    JOIN Copy c ON l.ISBN = c.ISBN AND l.Copy_Num = c.Copy_Num
    JOIN Book b ON c.ISBN = b.ISBN
    GROUP BY b.Title, b.Author
    ORDER BY COUNT(l.Loan_ID) DESC
    LIMIT 10
    '''
    cur = conn.cursor()
    cur.execute(sql)
    books = cur.fetchall()
    for book in books:
        print(book)

def members_with_long_overdue_books(conn):
    """ Query to identify members who have not returned books for over 60 days """
    sql = '''
    SELECT m.M_ID, m.Name, b.Title, l.Due_Date, 
           (julianday(CURRENT_DATE) - julianday(l.Due_Date)) as DaysOverdue
    FROM Loan l
    JOIN Copy c ON l.ISBN = c.ISBN AND l.Copy_Num = c.Copy_Num
    JOIN Book b ON c.ISBN = b.ISBN
    JOIN Member m ON l.M_ID = m.M_ID
    WHERE l.Ret_Date IS NULL AND (julianday(CURRENT_DATE) - julianday(l.Due_Date)) > 60
    '''
    cur = conn.cursor()
    cur.execute(sql)
    overdue_loans = cur.fetchall()
    for loan in overdue_loans:
        print(loan)
def checkout_book(conn, m_id, isbn, copy_num):
    """ Function to manually check out a book """
    sql = '''
    INSERT INTO Loan (M_ID, ISBN, Copy_Num, ChkOut_Date, Due_Date)
    VALUES (?, ?, ?, ?, ?)
    '''
    chkout_date = datetime.date.today()
    due_date = chkout_date + datetime.timedelta(days=21) 

    cur = conn.cursor()
    cur.execute(sql, (m_id, isbn, copy_num, chkout_date, due_date))
    conn.commit()
    print(f"Book with ISBN {isbn} checked out to member {m_id}. Due date: {due_date}")

def update_record(conn, table, column_to_update, new_value, key_column, key_value):
    """ Generic function to update a record in a table """
    sql = f'UPDATE {table} SET {column_to_update} = ? WHERE {key_column} = ?'
    cur = conn.cursor()
    cur.execute(sql, (new_value, key_value))
    conn.commit()

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
        while True:
            print("\nDatabase Reports Menu:")
            print("1. List of All Books Borrowed by an Individual")
            print("2. Report of Overdue Books")
            print("3. Total Number of Books Loaned Out by Category")
            print("4. List of Inactive Members")
            print("5. Most Popular Books")
            print("6. Members With Long Overdue Books")
            print("7. Checkout a book")
            print("8. Update a record")
            print("9. Delete a record")
            print("0. Exit")
            choice = input("Enter your choice (1-8): ")

            if choice == '1':
                member_id = input("Enter Member ID: ")
                list_books_borrowed_by_individual(conn, member_id)
            elif choice == '2':
                report_overdue_books(conn)
            elif choice == '3':
                total_books_loaned_out_by_category(conn)
            elif choice == '4':
                list_inactive_members(conn)
            elif choice == '5':
                most_popular_books(conn)
            elif choice == '6':
                members_with_long_overdue_books(conn)
            elif choice == '7':
                m_id = input("Enter Member ID: ")
                isbn = input("Enter Book ISBN: ")
                copy_num = input("Enter Copy Number: ")
                checkout_book(conn, m_id, isbn, copy_num)
            elif choice == '8':
                table = input("Enter the table name to update: ")
                column_to_update = input(f"Enter the column name in {table} to update: ")
                new_value = input(f"Enter the new value for {column_to_update}: ")
                key_column = input(f"Enter the key column name in {table} to match: ")
                key_value = input(f"Enter the value of {key_column} to update: ")
                update_record(conn, table, column_to_update, new_value, key_column, key_value)
            elif choice == '9':
                table = input("Enter the table name to delete from: ")
                column = input(f"Enter the column name in {table} to match: ")
                value = input(f"Enter the value of {column} to delete: ")
                delete_record(conn, table, column, value)
            elif choice == '0':
                print("Exiting the program.")
                break
            else:
                print("Invalid choice. Please try again.")

    else:
        print("Error! cannot create the database connection.")

if __name__ == '__main__':
    main()
