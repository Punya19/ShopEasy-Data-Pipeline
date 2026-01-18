# import mysql.connector
# import random
# from faker import Faker

# # Initialize Faker
# faker = Faker()
# faker.unique.clear()

# db_config = {
#     'host': 'localhost',
#     'user': 'root',
#     'password': 'Punya19@2003',
#     'database': 'shopeasy',
#     'auth_plugin': 'mysql_native_password'  # Ensuring correct authentication plugin
# }


# try:
#     conn = mysql.connector.connect(**db_config)
#     cursor = conn.cursor()
#     print("Database connection successful!")
# except mysql.connector.Error as err:
#     print(f" Error: {err}")
#     exit()


# unique_emails = set()
# users = []

# while len(users) < 1000:
#     email = faker.email()---
#     if email not in unique_emails:
#         unique_emails.add(email)
#         users.append((faker.name(), email, faker.address().replace("\n", " ")))

# insert_users_query = "INSERT INTO users (name, email, address) VALUES (%s, %s, %s)"
# cursor.executemany(insert_users_query, users)
# conn.commit()
# print("Unique Users Inserted Successfully!")


# categories = ["Electronics", "Clothing", "Home & Kitchen", "Books", "Toys"]
# products = [(faker.word().capitalize() + " " + random.choice(["Pro", "Plus", "X", "Max"]),
#              random.choice(categories),
#              round(random.uniform(10, 500), 2))
#             for _ in range(1000)]

# insert_products_query = "INSERT INTO products (name, category, price) VALUES (%s, %s, %s)"
# cursor.executemany(insert_products_query, products)
# conn.commit()
# print(" Products Inserted Successfully!")

# orders = [(random.randint(1, 1000),  # user_id 
#            random.randint(1, 1000),  # product_id 
#            random.randint(1, 5),  # quantity
#            round(random.uniform(10, 500), 2))  # total_price
#           for _ in range(10000)]

# insert_orders_query = "INSERT INTO orders (user_id, product_id, quantity, total_price) VALUES (%s, %s, %s, %s)"
# cursor.executemany(insert_orders_query, orders)
# conn.commit()
# print(" Orders Inserted Successfully!")


# cursor.execute("SELECT order_id FROM orders")
# orders = cursor.fetchall()

# status_choices = ["Pending", "Shipped", "Delivered", "Cancelled"]
# updated_orders = [(random.choice(status_choices), order_id) for order_id, in orders]


# cursor.close()
# conn.close()
# print("Database connection closed.")

import mysql.connector
import pandas as pd
import random
from faker import Faker

faker = Faker()
faker.unique.clear()

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '123',
    'database': 'shopeasy',
    'auth_plugin': 'mysql_native_password'  # Ensuring correct authentication plugin
}


# Connect to MySQL and create database
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS shopeasy")
cursor.execute("USE shopeasy")

# Create tables
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255),
        email VARCHAR(255) UNIQUE,
        address TEXT
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        product_id INT AUTO_INCREMENT PRIMARY KEY,
        product_name VARCHAR(255),
        category VARCHAR(100),
        price DECIMAL(10,2)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        order_id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT,
        product_id INT,
        quantity INT,
        total_price DECIMAL(10,2),
        order_date DATE DEFAULT (CURRENT_DATE),
        FOREIGN KEY (user_id) REFERENCES users(user_id),
        FOREIGN KEY (product_id) REFERENCES products(product_id)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS date_info (
        date_id INT AUTO_INCREMENT PRIMARY KEY,
        product_id INT,
        order_date DATE,
        day_type ENUM('Weekday', 'Weekend'),
        FOREIGN KEY (product_id) REFERENCES products(product_id)
    )
""")

conn.commit()
print("Database and Tables Created Successfully!")

# Insert Users
unique_emails = set()
users = []

while len(users) < 1000:
    email = faker.email()
    if email not in unique_emails:
        unique_emails.add(email)
        users.append((faker.name(), email, faker.address().replace("\n", " ")))

insert_users_query = "INSERT IGNORE INTO users (name, email, address) VALUES (%s, %s, %s)"
cursor.executemany(insert_users_query, users)
conn.commit()
print("Unique Users Inserted Successfully!")

# Insert Products
categories = ["Electronics", "Clothing", "Beauty & Personal Care", "Books", "Toys","makeup","Home & Kitchen","Sports & Fitness","Books & Stationery"
              ,"Health & Wellness","Grocery & Food"]
products = [(faker.word().capitalize() + " " + random.choice(["Pro", "Plus", "X", "Max"]),
             random.choice(categories),
             round(random.uniform(10, 500), 2))
            for _ in range(1000)]

insert_products_query = "INSERT INTO products (product_name, category, price) VALUES (%s, %s, %s)"
cursor.executemany(insert_products_query, products)
conn.commit()
print("Products Inserted Successfully!")

# Insert Orders with random dates
orders = [(random.randint(1, 1000),
           random.randint(1, 1000),
           random.randint(1, 5),
           round(random.uniform(10, 500), 2),
           faker.date_between(start_date='-1y', end_date='today'))  # Generates only date (YYYY-MM-DD)
          for _ in range(10000)]

insert_orders_query = "INSERT INTO orders (user_id, product_id, quantity, total_price, order_date) VALUES (%s, %s, %s, %s, %s)"
cursor.executemany(insert_orders_query, orders)
conn.commit()
print("Orders Inserted Successfully!")

#  classify Weekday/Weekend
cursor.execute("""
    INSERT INTO date_info (product_id,  order_date, day_type)
    SELECT 
        o.product_id, 
        o.order_date, 
        CASE 
            WHEN DAYOFWEEK(o.order_date) IN (1, 7) THEN 'Weekend'  #day of week autometically get the days
            ELSE 'Weekday' 
        END AS day_type
    FROM orders o
    JOIN products p ON o.product_id = p.product_id
""")
conn.commit()
print("Date Info Inserted Successfully!")

# Close connection
cursor.close()
conn.close()
print("Database connection closed.")
