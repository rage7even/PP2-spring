import psycopg2
import csv

conn = psycopg2.connect(
    host="localhost",
    database="pydatabases",
    user="postgres",
    password="rage7even"
)
cur = conn.cursor()

def insert_from_console():
    username = input("Enter name: ")
    phone = input("Enter phone: ")
    cur.execute("INSERT INTO phonebookpy (username, phone) VALUES (%s, %s)", (username, phone))
    conn.commit()
    print(" Contact saved!")

def insert_from_csv(filename):
    with open(filename, 'r', encoding='utf-8-sig', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            username = row["username"]
            phone = row["phone"]
            cur.execute("INSERT INTO phonebookpy (username, phone) VALUES (%s, %s)", (username, phone))
        conn.commit()
        print(" Data from CSV added!")

def update_user(old_name, new_name=None, new_phone=None):
    if new_name:
        cur.execute("UPDATE phonebookpy SET username = %s WHERE username = %s", (new_name, old_name))
    if new_phone:
        cur.execute("UPDATE phonebookpy SET phone = %s WHERE username = %s", (new_phone, old_name))
    conn.commit()
    print(" Data updated!")

def delete_by_username(username):
    cur.execute("DELETE FROM phonebookpy WHERE username = %s", (username,))
    conn.commit()
    print("Contact deleted!")

def query_all():
    cur.execute("SELECT * FROM phonebookpy")
    rows = cur.fetchall()
    if rows:
        print(" All contacts:")
        for row in rows:
            print(f"Username {row[1]} — Phone num {row[2]}")
    else:
        print(" No contacts found.")

def search_data():
    print("Find by:")
    choice = input("1 - Username, 2 - Phone: ")

    if choice == '1':
        name = input("Username: ")
        cur.execute("SELECT * FROM phonebookpy WHERE username ILIKE %s", ('%' + name + '%',))
    elif choice == '2':
        phone = input("Phone: ")
        cur.execute("SELECT * FROM phonebookpy WHERE phone LIKE %s", ('%' + phone + '%',))
    else:
        print(" Wrong choice.")
        return

    rows = cur.fetchall()
    if rows:
        for row in rows:
            print(f"Username {row[1]} — Phone num {row[2]}")
    else:
        print("Nothing was found.")

while True:
    print("\n📱 PhoneBook Menu:")
    print("1. Insert from console")
    print("2. Insert from CSV")
    print("3. Update user")
    print("4. Query all contacts")
    print("5. Delete by username")
    print("6. Search")
    print("7. Exit")

    choice = input("Choose option: ")

    if choice == '1':
        insert_from_console()
    elif choice == '2':
        insert_from_csv(r"D:\PP2spring\py lab 10\contactpy.csv")
    elif choice == '3':
        old = input("Old name: ")
        new = input("New name (or press Enter to skip): ")
        phone = input("New phone (or press Enter to skip): ")
        update_user(old, new if new else None, phone if phone else None)
    elif choice == '4':
        query_all()
    elif choice == '5':
        username = input("Enter username to delete: ")
        delete_by_username(username)
    elif choice == '6':
        search_data()
    elif choice == '7':
        print(" Goodbye!")
        break
    else:
        print(" Invalid option. Try again.")


cur.close()
conn.close()
