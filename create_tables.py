import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """Create a database connection to the SQLite database specified by db_file"""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """Create a table from the create_table_sql statement"""
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def main():
    database = "pythonsqlite.db"

    sql_create_member_table = """ CREATE TABLE IF NOT EXISTS Member (
                                        M_ID integer PRIMARY KEY,
                                        SSN text NOT NULL,
                                        Name text NOT NULL,
                                        Camp_Addr text,
                                        Home_Addr text,
                                        Phone text,
                                        Photo text,
                                        Card_Exp text,
                                        Borrowed_Count integer,
                                        Member_Type text
                                    ); """

    sql_create_book_table = """CREATE TABLE IF NOT EXISTS Book (
                                    ISBN text PRIMARY KEY,
                                    Title text NOT NULL,
                                    Author text NOT NULL,
                                    Sub_Area text,
                                    Desc text,
                                    Lang text,
                                    Binding text
                                );"""

    sql_create_copy_table = """CREATE TABLE IF NOT EXISTS Copy (
                                    Copy_Num integer,
                                    ISBN text NOT NULL,
                                    Condition text,
                                    Status text,
                                    PRIMARY KEY (Copy_Num, ISBN),
                                    FOREIGN KEY (ISBN) REFERENCES Book (ISBN)
                               );"""

    sql_create_loan_table = """CREATE TABLE IF NOT EXISTS Loan (
                                    Loan_ID integer PRIMARY KEY,
                                    M_ID integer NOT NULL,
                                    ISBN text NOT NULL,
                                    Copy_Num integer NOT NULL,
                                    ChkOut_Date text,
                                    Due_Date text,
                                    Ret_Date text,
                                    FOREIGN KEY (M_ID) REFERENCES Member (M_ID),
                                    FOREIGN KEY (ISBN, Copy_Num) REFERENCES Copy (ISBN, Copy_Num)
                               );"""

    sql_create_reference_material_table = """CREATE TABLE IF NOT EXISTS Reference_Material (
                                                Ref_Mat_ID integer PRIMARY KEY,
                                                ISBN text NOT NULL,
                                                FOREIGN KEY (ISBN) REFERENCES Book (ISBN)
                                            );"""

    sql_create_wish_list_table = """CREATE TABLE IF NOT EXISTS Wish_List (
                                        WL_ID integer PRIMARY KEY,
                                        Title text NOT NULL,
                                        Author text NOT NULL,
                                        Interest_Reason text
                                    );"""

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        create_table(conn, sql_create_member_table)
        create_table(conn, sql_create_book_table)
        create_table(conn, sql_create_copy_table)
        create_table(conn, sql_create_loan_table)
        create_table(conn, sql_create_reference_material_table)
        create_table(conn, sql_create_wish_list_table)
    else:
        print("Error! cannot create the database connection.")


if __name__ == "__main__":
    main()
