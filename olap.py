import mysql.connector
import psycopg2

mysql_conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123",
    database="shopeasy",
    auth_plugin="mysql_native_password"
)
-
mysql_cursor = mysql_conn.cursor()

pg_conn = psycopg2.connect(
    dbname="shopeasy_dw",
    user="postgres",
    password="123",
    host="localhost"
)
pg_cursor = pg_conn.cursor()


mysql_cursor.execute("SELECT user_id, name, email, address FROM users")
users = mysql_cursor.fetchall()

mysql_cursor.execute("SELECT product_id, product_name, category, price FROM products")
products = mysql_cursor.fetchall()

mysql_cursor.execute("SELECT order_id, user_id, product_id, quantity, total_price, order_date FROM orders")
orders = mysql_cursor.fetchall()

#category insertion
category_map = {}
for product in products:
    category = product[2] #product table 2nd column is category
    
    if category not in category_map:
        pg_cursor.execute("SELECT category_id FROM dim_categories WHERE category = %s", (category,))
        existing_category = pg_cursor.fetchone()

        if existing_category:
            category_map[category] = existing_category[0]
        else:
            pg_cursor.execute("INSERT INTO dim_categories (category) VALUES (%s) RETURNING category_id", (category,))
            category_map[category] = pg_cursor.fetchone()[0]

#  Insert Users 
for user in users:
    pg_cursor.execute("""
        INSERT INTO dim_users (user_id, name, email, address)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (user_id) DO NOTHING
    """, user)

# Insert Products
for product in products:
    product_id, product_name, category, price = product
    category_id = category_map[category]
    
    pg_cursor.execute("""
        INSERT INTO dim_products (product_id, product_name, category_id, price)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (product_id) DO NOTHING
    """, (product_id, product_name, category_id, price))

#  Insert Date 
date_map = {}
for order in orders:
    order_date = order[5]
    day_of_week = order_date.strftime("%A") #converts the date into full weekdays
    day_type = "Weekend" if order_date.weekday() >= 5 else "Weekday"

    if order_date not in date_map:
        pg_cursor.execute("SELECT date_id FROM dim_dates WHERE order_date = %s", (order_date,))
        existing_date = pg_cursor.fetchone()

        if existing_date:
            date_map[order_date] = existing_date[0]
        else:
            pg_cursor.execute("""
                INSERT INTO dim_dates (order_date, day_of_week, day_type)
                VALUES (%s, %s, %s) RETURNING date_id
            """, (order_date, day_of_week, day_type))
            date_map[order_date] = pg_cursor.fetchone()[0]

#  Fact Sales 
for order in orders:
    order_id, user_id, product_id, quantity, total_price, order_date = order
    date_id = date_map[order_date]
    category_id = category_map[products[product_id - 1][2]]  #[2] extract the category name from the product tuple nd -1 y is it assumes it is starting by 1 
    
    
    pg_cursor.execute("""
        INSERT INTO fact_sales (sale_id, user_id, product_id, category_id, date_id, quantity, total_price)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (sale_id) 
        DO UPDATE SET 
            quantity = EXCLUDED.quantity, 
            total_price = EXCLUDED.total_price
    """, (order_id, user_id, product_id, category_id, date_id, quantity, total_price))


pg_conn.commit()
mysql_conn.close()
pg_conn.close()

print("ETL Process Completed Successfully!")