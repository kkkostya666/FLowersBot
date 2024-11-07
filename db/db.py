import sqlite3
import datetime


class Db:
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.connection.isolation_level = None
        self.cursor = self.connection.cursor()
        self.connection.execute('pragma foreign_keys=ON')
        # self.create_table_users()
        # self.create_table_categories_models()
        # self.create_table_models()
        # self.create_table_support_requests()
        # self.create_requisite_table()
        # self.create_table_order_model_user()
        # self.add_method_column_to_order_model_user()

    def create_table_users(self):
        with self.connection:
            self.cursor.execute("""
                  CREATE TABLE IF NOT EXISTS users (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      user_id INTEGER UNIQUE,
                      is_bot BOOLEAN,                 
                      first_name TEXT,               
                      last_name TEXT,                 
                      username TEXT,           
                      language_code VARCHAR(5),     
                      is_premium BOOLEAN,
                      city TEXT,
                      currency TEXT,
                      date_of_create DATE
                  );
              """)
            print("[INFO] Table users created successfully")

    def create_table_categories_models(self):
        with self.connection:
            self.cursor.execute("""
                  CREATE TABLE IF NOT EXISTS categories (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      name TEXT NOT NULL UNIQUE
                  );
              """)
            print("[INFO] Table categories created successfully")

    def create_table_models(self):
        with self.connection:
            self.cursor.execute("""
                  CREATE TABLE IF NOT EXISTS models (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      name TEXT NOT NULL,
                      description TEXT,
                      price INT,
                      image TEXT,
                      category_id INTEGER,
                      city TEXT,
                      FOREIGN KEY (category_id) REFERENCES categories (id) ON DELETE CASCADE
                  );
              """)
            print("[INFO] Table models created successfully")

    def create_table_support_requests(self):
        with self.connection:
            self.cursor.execute("""
                  CREATE TABLE IF NOT EXISTS support_requests (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      user_id INTEGER,
                      message TEXT,
                      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                      response TEXT,
                      status TEXT,
                      FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
                  );
              """)
            print("[INFO] Table support_requests created successfully")

    def create_requisite_table(self):
        with self.connection:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS requisites_methods (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    method_name TEXT UNIQUE NOT NULL,
                    address TEXT NOT NULL                 
                );
            """)
            print("[INFO] Table requisites_methods created successfully")

    def create_table_order_model_user(self):
        with self.connection:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS order_model_user (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    payment_id TEXT NOT NULL,
                    user_id INTEGER NOT NULL,
                    model_id INTEGER NOT NULL,
                    price INT NOT NULL, 
                    status TEXT NOT NULL, 
                    created_at DATE,
                    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
                    FOREIGN KEY (model_id) REFERENCES models (id) ON DELETE CASCADE
                );
            """)
            print("[INFO] Table order_model_user created successfully")

    def get_orders_by_user_id(self, user_id):
        with self.connection:
            self.cursor.execute("""
                SELECT * FROM order_model_user 
                WHERE user_id = ?
                ORDER BY created_at ASC
                LIMIT 7;
            """, (user_id,))
            return self.cursor.fetchall()

    def count_orders_by_user_id(self, user_id):
        query = """
            SELECT 
                COUNT(*) 
            FROM 
                order_model_user 
            WHERE 
                user_id = ?
        """

        self.cursor.execute(query, (user_id,))
        return self.cursor.fetchone()[0]

    def get_all_users(self):
        with self.connection:
            self.cursor.execute("SELECT * FROM users;")
            return self.cursor.fetchall()

    def insert_order_model_user(self, payment_id, user_id, model_id, price, status, date, method):
        with self.connection:
            self.cursor.execute("""
                INSERT INTO order_model_user (payment_id ,user_id, model_id, price, status, created_at,method)
                VALUES (?, ?, ?, ?, ? , ?, ?);
            """, (payment_id, user_id, model_id, price, status, date, method))
            print("[INFO] New order_model_user record inserted successfully")

    def add_method_column_to_order_model_user(self):
        with self.connection:
            self.cursor.execute("""
                ALTER TABLE order_model_user 
                ADD COLUMN method TEXT;
            """)
            print("[INFO] Column 'method' added to order_model_user successfully")

    def user_exists(self, user_id):
        with self.connection:
            self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
            return self.cursor.fetchone() is not None

    def add_user(self, user, city, date_of_create):
        with self.connection:
            self.cursor.execute("""
                   INSERT INTO users (user_id, is_bot, first_name, last_name, username, language_code, is_premium, city, currency, date_of_create)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
               """, (
                user.id, user.is_bot, user.first_name, user.last_name, user.username,
                user.language_code, user.is_premium, city, None, date_of_create
            ))
            print(f"[INFO] User {user.id} added to the database")

    def add_model(self, name, description, price, image, category_id, city):
        with self.connection:
            self.cursor.execute("""
                INSERT INTO models (name, description, price, image, category_id, city)
                VALUES (?, ?, ?, ?, ?, ?);
            """, (name, description, price, image, category_id, city))
            self.connection.commit()
            print(f"[INFO] Model '{name}' added successfully")

    def delete_user(self, user_id):
        """Удаляет пользователя по user_id из базы данных."""
        if self.user_exists(user_id):
            with self.connection:
                self.cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
                print(f"[INFO] User {user_id} deleted from the database")
        else:
            print(f"[WARNING] User {user_id} does not exist")

    def get_user_by_id(self, user_id):
        with self.connection:
            self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
            return self.cursor.fetchone()

    def update_user_city(self, user_id, city):
        with self.connection:
            self.cursor.execute("""
                UPDATE users
                SET city = ?
                WHERE user_id = ?
            """, (city, user_id))
            print(f"[INFO] User {user_id} city updated to {city}")

    def update_user_currency(self, user_id, currency):
        with self.connection:
            self.cursor.execute("""
                UPDATE users
                SET currency = ?
                WHERE user_id = ?
            """, (currency, user_id))
            print(f"[INFO] User {user_id} city updated to {currency}")

    def get_users_count(self):
        with self.connection:
            self.cursor.execute("SELECT COUNT(*) FROM users;")
            count = self.cursor.fetchone()[0]
            print(f"[INFO] Total users count: {count}")
            return count

    def get_models_count(self):
        with self.connection:
            self.cursor.execute("SELECT COUNT(*) FROM models;")
            count = self.cursor.fetchone()[0]
            print(f"[INFO] Total users count: {count}")
            return count

    def insert_category(self, name):
        with self.connection:
            self.cursor.execute("INSERT INTO categories (name) VALUES (?);", (name,))
            print(f"[INFO] Category '{name}' inserted successfully")

    def select_all_categories(self):
        with self.connection:
            self.cursor.execute("SELECT * FROM categories")
            categories = self.cursor.fetchall()
            return categories

    def delete_category(self, category_id=None, category_name=None):
        with self.connection:
            if category_id:
                self.cursor.execute("DELETE FROM categories WHERE id = ?", (category_id,))
            elif category_name:
                self.cursor.execute("DELETE FROM categories WHERE name = ?", (category_name,))
            else:
                raise ValueError("You must provide either category_id or category_name")
            self.connection.commit()
            print(
                f"[INFO] Category with {'ID' if category_id else 'Name'} {'deleted' if self.cursor.rowcount > 0 else 'not found'}")

    def count_users_today(self):
        today = datetime.date.today()
        query = """
            SELECT COUNT(*) FROM users
            WHERE date_of_create = ?
        """
        with self.connection:
            self.cursor.execute(query, (today,))
            count = self.cursor.fetchone()[0]
        return count

    def get_categories_count(self):
        with self.connection:
            self.cursor.execute("SELECT COUNT(*) FROM categories;")
            count = self.cursor.fetchone()[0]
            print(f"[INFO] Total categories count: {count}")
            return count

    def add_support_request(self, user_id: int, message: str):
        with self.connection:
            self.cursor.execute("""
                INSERT INTO support_requests (user_id, message, status)
                VALUES (?, ?, ?);
            """, (user_id, message, '👀 На рассмотрении'))
            print("[INFO] Support request added successfully")

    def get_latest_support_request(self, user_id: int):
        self.cursor.execute("""
            SELECT *
            FROM support_requests
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT 1;
        """, (user_id,))
        return self.cursor.fetchone()

    def update_support_request_response(self, support_id, response, status):
        with self.connection:
            self.cursor.execute("""
                UPDATE support_requests
                SET response = ?, status = ?
                WHERE id = ?
            """, (response, status, support_id,))
            self.connection.commit()
            print(f"[INFO] Заявка с ID бновлена успешно")

    def get_models_by_category(self, category_id):
        with self.connection:
            self.cursor.execute("""
                SELECT * FROM models WHERE category_id = ?;
            """, (category_id,))
            return self.cursor.fetchall()

    def add_city_column_to_models(self):
        with self.connection:
            self.cursor.execute("""
                ALTER TABLE models
                ADD COLUMN city TEXT;
            """)
            print("[INFO] Column 'city' added to 'models' table successfully")

    def get_models_with_cities(self, category_id, user_city):
        query = """
            SELECT 
                m.id,
                m.name,
                m.description,
                m.city,
                u.city AS user_city
            FROM 
                models AS m
            LEFT JOIN 
                users AS u ON m.city = u.city
            WHERE 
                m.city = ?  
        """

        params = [user_city]

        if category_id is not None:
            query += " AND m.category_id = ?"
            params.append(category_id)

        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def count_models_with_city(self, user_city):
        query = """
            SELECT 
                COUNT(*) 
            FROM 
                models AS m
            WHERE 
                m.city = ?
        """

        self.cursor.execute(query, (user_city,))
        return self.cursor.fetchone()[0]

    def get_model_by_id(self, model_id):
        query = """
            SELECT 
                id, 
                name, 
                description, 
                price, 
                image, 
                category_id,
                city
            FROM 
                models 
            WHERE 
                id = ?;
        """
        self.cursor.execute(query, (model_id,))
        return self.cursor.fetchone()

    def insert_requisite(self, method_name, address):
        with self.connection:
            self.cursor.execute("""
                INSERT INTO requisites_methods (method_name, address) 
                VALUES (?, ?);
            """, (method_name, address))
            print("[INFO] New requisite method added successfully")

    def get_requisites(self):
        with self.connection:
            self.cursor.execute("""
                SELECT * FROM requisites_methods;
            """)
            return self.cursor.fetchall()

    def get_requisites_by_id(self, method_name):
        with self.connection:
            self.cursor.execute("""
                SELECT address FROM requisites_methods WHERE method_name = ?;
            """, (method_name,))
            return self.cursor.fetchall()

    def update_order_status(self, payment_id, new_status):
        with self.connection:
            self.cursor.execute("""
                UPDATE order_model_user
                SET status = ?
                WHERE payment_id = ?;
            """, (new_status, payment_id))
            print(f"[INFO] Status of order ID {payment_id} updated to '{new_status}'")

# db = Db('freelance.db')
# db.update_support_request_response(7, 'etetete', 'good')
# # db.delete_user(1383157406)
# # db.delete_user(790389235)
