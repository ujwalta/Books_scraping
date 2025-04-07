# import sqlite3

# def create_database():
#     """
#     Creates a SQLite database with a table to store book information.
#     """
#     conn = sqlite3.connect("books_store.db")
#     print("Database created succesfully")
#     cursor = conn.cursor()
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS books (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             book_title TEXT NOT NULL,
#             author TEXT NOT NULL,
#             price TEXT,
#             add_to_basket_url TEXT
#         )
#     ''')
#     conn.commit()
#     conn.close()
# if __name__ == "__main__":
#     create_database()

# def insert_book_data(book_title, author, price, add_to_basket_url):
#     """
#     Inserts book data into the database.
#     """
#     conn = sqlite3.connect("books_store.db")
#     cursor = conn.cursor()

#     cursor.execute('''
#         SELECT COUNT(*) FROM books WHERE book_title = ? AND author = ?
#     ''', (book_title, author))

#     result = cursor.fetchone()
#     if result[0] > 0:
#         print(f"Book already exists: {book_title} by {author}")
#         return

#     cursor.execute('''
#         INSERT INTO books (book_title, author, price, add_to_basket_url)
#         VALUES (?, ?, ?, ?)
#     ''', (book_title, author, price, add_to_basket_url))
    
#     conn.commit()
#     conn.close()
#     print(f"Inserted: {book_title} by {author}")
# insert_book_data(book_title,author,price,add_to_basket_url)
import sqlite3
import pandas as pd

def create_database():
    conn = sqlite3.connect("books.db")
    cursor = conn.cursor()
    
    # Create the table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_title TEXT NOT NULL UNIQUE,
            author TEXT,
            price TEXT,
            stock TEXT,
            link TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

def insert_books_from_csv(csv_file):
    conn = sqlite3.connect("books.db")
    cursor = conn.cursor()

    df = pd.read_csv(csv_file)
    print(df.head())  # Debugging step: Check if CSV is loaded properly

    for _, row in df.iterrows():
        book_title = row["Title"]
        price = row["Price"]
        stock = row["Stock"]
        link = row["Link"]
        author = row["Author"] if "Author" in df.columns else "Unknown"

        cursor.execute('SELECT COUNT(*) FROM books WHERE book_title = ?', (book_title,))
        result = cursor.fetchone()
        if result[0] > 0:
            print(f'Skipping (already exists): {book_title}')
            continue

        try:
            cursor.execute('''
                INSERT INTO books (book_title, author, price, stock, link)
                VALUES (?, ?, ?, ?, ?)
            ''', (book_title, author, price, stock, link))
            print(f"Inserted: {book_title}")
        except sqlite3.IntegrityError as e:
            print(f"Skipping {book_title} - Error: {e}")

    conn.commit()
    conn.close()
    print("All books inserted successfully.")

# Run the functions
create_database()
insert_books_from_csv("books.csv")
