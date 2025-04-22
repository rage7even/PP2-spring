import psycopg2

# Соединение с базой данных PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="pydatabases",
    user="postgres",
    password="rage7even"
)

cur = conn.cursor()

def search_contacts_by_pattern(pattern):
    """Функция для поиска пользователей по имени или телефону"""
    cur.execute("SELECT * FROM search_contacts_by_pattern(%s)", (pattern,))
    rows = cur.fetchall()
    if rows:
        for row in rows:
            print(f"ID: {row[0]}, Name: {row[1]}, Phone: {row[2]}")
    else:
        print("No contacts found.")

def insert_or_update_user(username, phone):
    """Процедура для вставки или обновления пользователя"""
    cur.execute("CALL insert_or_update_user(%s, %s)", (username, phone))
    conn.commit()
    print("Data inserted/updated.")

def insert_many_users(names, phones):
    """Процедура для вставки нескольких пользователей"""
    cur.execute("SELECT insert_many_users(%s, %s)", (names, phones))
    conn.commit()
    print("Data inserted.")

def delete_by_username_or_phone(identifier):
    """Процедура для удаления пользователя по имени или телефону"""
    cur.execute("CALL delete_by_name_or_phone(%s)", (identifier,))
    conn.commit()
    print("Data deleted.")

# Взаимодействие с пользователем для различных операций
while True:
    print("\nPhoneBook Menu:")
    print("1. Search contacts")
    print("2. Insert or update user")
    print("3. Insert many users")
    print("4. Delete user by username or phone")
    print("5. Exit")

    choice = input("Choose an option: ")

    if choice == '1':
        pattern = input("Enter a name or phone number to search: ")
        search_contacts_by_pattern(pattern)
    
    elif choice == '2':
        username = input("Enter username: ")
        phone = input("Enter phone: ")
        insert_or_update_user(username, phone)
    
    elif choice == '3':
        # Пример для вставки нескольких пользователей
        names = input("Enter names separated by commas: ").split(",")
        phones = input("Enter corresponding phones separated by commas: ").split(",")
        insert_many_users(names, phones)
    
    elif choice == '4':
        identifier = input("Enter username or phone to delete: ")
        delete_by_username_or_phone(identifier)
    
    elif choice == '5':
        print("Goodbye!")
        break

    else:
        print("Invalid option. Try again.")

# Закрытие соединения
cur.close()
conn.close()
