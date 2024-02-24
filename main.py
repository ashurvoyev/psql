import psycopg2
from psycopg2 import sql

# Ma'lumotlar bazasiga ulanish
def connect():
    try:
        connection = psycopg2.connect(
            dbname='dorixona',
            user='postgres',
            password='postgres',
            host='localhost',
            port=5432
        )
        return connection
    except psycopg2.Error as e:
        print("Xatolik yuz berdi:", e)

# Ma'lumot qo'shish
def insert_data(table, columns, values):
    try:
        connection = connect()
        cursor = connection.cursor()
        query = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
            sql.Identifier(table),
            sql.SQL(', ').join(map(sql.Identifier, columns)),
            sql.SQL(', ').join(sql.Placeholder() * len(values))
        )
        cursor.execute(query, values)
        connection.commit()
        print("Ma'lumot qo'shildi")
    except psycopg2.Error as e:
        print("Xatolik yuz berdi:", e)
    finally:
        cursor.close()
        connection.close()

# Ma'lumot o'qish
def select_data(table):
    try:
        connection = connect()
        cursor = connection.cursor()
        query = sql.SQL("SELECT * FROM {}").format(sql.Identifier(table))
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            print(row)
    except psycopg2.Error as e:
        print("Xatolik yuz berdi:", e)
    finally:
        cursor.close()
        connection.close()

# Ma'lumotlarni o'chirish
def delete_data(table, condition):
    try:
        connection = connect()
        cursor = connection.cursor()
        query = sql.SQL("DELETE FROM {} WHERE {}").format(
            sql.Identifier(table),
            sql.SQL(condition)
        )
        cursor.execute(query)
        connection.commit()
        print("Ma'lumot o'chirildi")
    except psycopg2.Error as e:
        print("Xatolik yuz berdi:", e)
    finally:
        cursor.close()
        connection.close()

# Dorixona kichik bazasini yaratish
def create_database():
    try:
        connection = psycopg2.connect(
            dbname='postgres',
            user='postgres',
            password='postgres',
            host='localhost',
            port=5432
        )
        connection.autocommit = True
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE dorixona")
        print("Dorixona kichik bazasi yaratildi")
    except psycopg2.Error as e:
        print("Xatolik yuz berdi:", e)
    finally:
        cursor.close()
        connection.close()

# Dorixona kichik bazasini o'chirish
def drop_database():
    try:
        connection = psycopg2.connect(
            dbname='postgres',
            user='postgres',
            password='postgres',
            host='localhost',
            port=5432
        )
        connection.autocommit = True
        cursor = connection.cursor()
        cursor.execute("DROP DATABASE IF EXISTS dorixona")
        print("Dorixona kichik bazasi o'chirildi")
    except psycopg2.Error as e:
        print("Xatolik yuz berdi:", e)
    finally:
        cursor.close()
        connection.close()

# Ma'lumotlar bazasini yaratish
drop_database()
create_database()

# Foydalanuvchilar jadvali
create_table_users = """
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    age INT
);
"""
# Buyurtmalar jadvali
create_table_orders = """
CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    product_name VARCHAR(100),
    price DECIMAL(10, 2),
    user_id INT REFERENCES users(id)
);
"""

# Jadvalni yaratish
def create_tables():
    try:
        connection = connect()
        cursor = connection.cursor()
        cursor.execute(create_table_users)
        cursor.execute(create_table_orders)
        connection.commit()
        print("Jadvallar yaratildi")
    except psycopg2.Error as e:
        print("Xatolik yuz berdi:", e)
    finally:
        cursor.close()
        connection.close()

# Dasturni ishga tushirish
if __name__ == "__main__":
    create_tables()

    # Ma'lumot qo'shish
    insert_data("users", ["first_name", "last_name", "age"], ("John", "Doe", 30))
    insert_data("users", ["first_name", "last_name", "age"], ("Jane", "Smith", 25))
    insert_data("orders", ["product_name", "price", "user_id"], ("Laptop", 1500.00, 1))
    insert_data("orders", ["product_name", "price", "user_id"], ("Smartphone", 800.00, 2))

    # Ma'lumotlarni o'qish
    print("Foydalanuvchilar jadvali:")
    select_data("users")
    print("Buyurtmalar jadvali:")
    select_data("orders")

    # Ma'lumotlarni o'chirish
    delete_data("users", "age > 30")

