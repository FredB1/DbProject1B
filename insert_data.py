import sqlite3
import random
from faker import Faker
import datetime

def create_connection(db_file):
    """Create a database connection to the SQLite database specified by db_file"""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)
    return conn


def insert_member_data(conn, data):
    """Insert member data into the Member table"""
    sql = """ INSERT INTO Member(M_ID, SSN, Name, Camp_Addr, Home_Addr, Phone, Photo, Card_Exp, Borrowed_Count, Member_Type) VALUES(?,?,?,?,?,?,?,?,?,?) """
    cur = conn.cursor()
    cur.executemany(sql, data)
    conn.commit()


def generate_member_data(count=16000):
    """Generate member data using Faker"""
    fake = Faker()
    members = []
    for i in range(count):
        member = (
            i + 1,  # M_ID, unique for each member
            fake.ssn(),  # SSN
            fake.name(),  # Name
            fake.address(),  # Camp_Addr
            fake.address(),  # Home_Addr
            fake.phone_number(),  # Phone
            "path/to/photo.jpg",  # Photo
            fake.date_between(
                start_date="-5y", end_date="today"
            ).isoformat(),  # Card_Exp
            random.randint(0, 100),  # Borrowed_Count
            random.choice(["Regular", "Professor"]),  # Member_Type
        )
        members.append(member)
    return members


def insert_book_data(conn, data):
    """Insert book data into the Book table"""
    sql = """ INSERT INTO Book(ISBN, Title, Author, Sub_Area, Desc, Lang, Binding) VALUES(?,?,?,?,?,?,?) """
    cur = conn.cursor()
    cur.executemany(sql, data)
    conn.commit()


def generate_book_data( count=100000):  # Adjust the count as needed
    """Generate book data using Faker"""
    fake = Faker()
    books = []
    generated_isbns = set()  # Keep track of generated ISBNs
    subject_areas = [
        "Computer Science", "Biology", "History", "Mathematics",
        "Physics", "Literature", "Economics", "Psychology",
        "Engineering", "Art"
    ]

    while len(books) < count:
        isbn = fake.isbn13()
        if isbn not in generated_isbns:
            generated_isbns.add(isbn)
            book = (
                isbn,  # ISBN
                fake.sentence(nb_words=4),  # Title
                fake.name(),  # Author
                random.choice(subject_areas),  # Sub_Area
                fake.text(max_nb_chars=200),  # Description
                fake.language_name(),  # Language
                random.choice(["Hardcover", "Paperback", "Ebook"])  # Binding
            )
            books.append(book)

    return books


def insert_copy_data(conn, data):
    """Insert copy data into the Copy table"""
    sql = """ INSERT INTO Copy(Copy_Num, ISBN, Condition) VALUES(?,?,?) """
    cur = conn.cursor()
    cur.executemany(sql, data)
    conn.commit()


def generate_copy_data(conn, avg_copies_per_book=2.5):
    """Generate copy data for each book in the Book table"""
    cur = conn.cursor()
    cur.execute("SELECT ISBN FROM Book")
    books = cur.fetchall()

    copies = []
    conditions = ["New", "Good", "Fair", "Worn"]
    for isbn in books:
        num_copies = round(avg_copies_per_book + random.uniform(-0.5, 0.5))
        for copy_num in range(1, num_copies + 1):
            copy = (
                copy_num,  # Copy_Num
                isbn[0],  # ISBN
                random.choice(conditions),  # Condition
            )
            copies.append(copy)
    return copies

def insert_loan_data(conn, data):
    """ Insert loan data into the Loan table """
    sql = ''' INSERT INTO Loan(Loan_ID, M_ID, ISBN, Copy_Num, ChkOut_Date, Due_Date, Ret_Date) VALUES(?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.executemany(sql, data)
    conn.commit()

def generate_loan_data(conn, count=50000):  # Adjust count as needed
    """ Generate loan data """
    fake = Faker()
    loans = []

    # Fetch member IDs
    cur = conn.cursor()
    cur.execute("SELECT M_ID FROM Member")
    members = [row[0] for row in cur.fetchall()]

    # Fetch book copies
    cur.execute("SELECT ISBN, Copy_Num FROM Copy")
    copies = cur.fetchall()

    for i in range(count):
        member_id = random.choice(members)
        isbn, copy_num = random.choice(copies)
        chkout_date = fake.date_between(start_date="-2y", end_date="today")
        due_date = chkout_date + datetime.timedelta(days=21)  # 21 days from checkout
        ret_date = due_date + datetime.timedelta(days=random.randint(-7, 14))  # Return within -7 to +14 days from due date

        loan = (
            i + 1,              # Loan_ID
            member_id,          # M_ID
            isbn,               # ISBN
            copy_num,           # Copy_Num
            chkout_date,        # ChkOut_Date
            due_date,           # Due_Date
            ret_date if random.random() < 0.95 else None  # Ret_Date (5% chance of not returned)
        )
        loans.append(loan)

    return loans
def insert_reference_material_data(conn, data):
    """ Insert reference material data into the Reference Material table """
    sql = ''' INSERT INTO Reference_Material(Ref_Mat_ID, ISBN) VALUES(?,?) '''
    cur = conn.cursor()
    cur.executemany(sql, data)
    conn.commit()

def generate_reference_material_data(conn, count=1000):  # Adjust count as needed
    """ Generate reference material data """
    cur = conn.cursor()
    cur.execute("SELECT ISBN FROM Book")
    all_isbns = [row[0] for row in cur.fetchall()]

    # Randomly select a subset of ISBNs for reference materials
    selected_isbns = random.sample(all_isbns, min(count, len(all_isbns)))

    reference_materials = [(i + 1, isbn) for i, isbn in enumerate(selected_isbns)]
    return reference_materials
def insert_wish_list_data(conn, data):
    """ Insert wish list data into the Wish List table """
    sql = ''' INSERT INTO Wish_List(WL_ID, Title, Author, Interest_Reason) VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.executemany(sql, data)
    conn.commit()

def generate_wish_list_data(count=500):  # Adjust count as needed
    """ Generate wish list data """
    fake = Faker()
    wish_list = []
    interest_reasons = ['Rare', 'Out-of-Print', 'Lost', 'Destroyed']

    for i in range(count):
        wish_item = (
            i + 1,                          # WL_ID
            fake.sentence(nb_words=3),      # Title
            fake.name(),                    # Author
            random.choice(interest_reasons) # Interest_Reason
        )
        wish_list.append(wish_item)

    return wish_list

# In your main function, call these to generate and insert wish list data

def main():
    database = "pythonsqlite.db"
    conn = create_connection(database)

    if conn is not None:
        member_data = generate_member_data()
        insert_member_data(conn, member_data)

        book_data = generate_book_data()
        insert_book_data(conn, book_data)

        copy_data = generate_copy_data(conn)
        insert_copy_data(conn, copy_data)

        loan_data = generate_loan_data(conn)
        insert_loan_data(conn, loan_data)

        ref_material_data = generate_reference_material_data(conn)
        insert_reference_material_data(conn, ref_material_data)

        wish_list_data =generate_wish_list_data()
        insert_wish_list_data(conn, wish_list_data)
    else:
        print("Error! cannot create the database connection.")


if __name__ == "__main__":
    main()
