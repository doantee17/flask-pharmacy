# db_setup.py (sửa lỗi Commands out of sync)
import mysql.connector
from flask_bcrypt import Bcrypt

DB_CONFIG = {
    'host': 'crossover.proxy.rlwy.net',
    'port': 36164,
    'user': 'root',
    'password': 'bjcwCWhfUsOvSsHCJBsFiDKgCrnzvfHj',
    'database': 'railway'
}

def get_db_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        print("\u2705 Kết nối database thành công.")
        return conn
    except mysql.connector.Error as err:
        print(f"❌ Lỗi khi kết nối database: {err}")
        return None

def create_database_if_not_exists():
    temp_config = DB_CONFIG.copy()
    db_name = temp_config.pop('database')
    conn = None
    try:
        conn = mysql.connector.connect(**temp_config)
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        print(f"Database '{db_name}' ensured to exist.")
    except mysql.connector.Error as err:
        print(f"Error creating database: {err}")
    finally:
        if conn:
            conn.close()

def try_add_column(conn, table, column_def):
    try:
        with conn.cursor() as cur:
            cur.execute(f"ALTER TABLE {table} ADD COLUMN {column_def}")
            print(f"\u2705 Đã thêm cột '{column_def}' vào bảng {table}.")
    except mysql.connector.Error as err:
        if "Duplicate column name" in str(err):
            print(f"Cột '{column_def.split()[0]}' đã tồn tại.")
        else:
            print(f"❌ Lỗi khi thêm cột '{column_def}': {err}")

def init_db():
    create_database_if_not_exists()
    conn = get_db_connection()
    if conn is None:
        print("Could not establish database connection for initialization.")
        return
    
    c = conn.cursor()
    try:
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) UNIQUE NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                role VARCHAR(20) DEFAULT 'user',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        c.execute('''CREATE TABLE IF NOT EXISTS products (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            category VARCHAR(255) NOT NULL,
            price DECIMAL(10, 2) NOT NULL,
            description TEXT,
            image_url VARCHAR(255),
            stock_quantity INT DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')

        c.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                status VARCHAR(50) DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
            )
        ''')

        c.execute('''
            CREATE TABLE IF NOT EXISTS order_items (
                id INT AUTO_INCREMENT PRIMARY KEY,
                order_id INT,
                product_id INT,
                quantity INT NOT NULL,
                unit_price DECIMAL(10, 2) NOT NULL,
                FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
                FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
            )
        ''')

        # Thêm các cột mở rộng cho bảng orders
        extra_columns = [
            "admin_notes TEXT",
            "city VARCHAR(100)",
            "district VARCHAR(100)",
            "full_name VARCHAR(255)",
            "phone VARCHAR(20)",
            "email VARCHAR(255)",
            "address TEXT",
            "payment_method VARCHAR(50)",
            "notes TEXT"
        ]
        for col in extra_columns:
            try_add_column(conn, 'orders', col)
            
        # Kiểm tra và xoá cột 'quantity' sai nếu tồn tại trong bảng orders
        try:
            with conn.cursor() as c_check:
                c_check.execute("SHOW COLUMNS FROM orders")
                columns = [row[0] for row in c_check.fetchall()]
                print("📋 Các cột hiện tại trong 'orders':", columns)
                if "quantity" in columns:
                    c_check.execute("ALTER TABLE orders DROP COLUMN quantity")
                    print("✅ Đã xoá cột 'quantity' khỏi bảng orders.")
        except mysql.connector.Error as err:
            print(f"❌ Lỗi khi kiểm tra hoặc xoá cột 'quantity': {err}")


        # Bảng diseases (giữ nguyên)
        c.execute('''CREATE TABLE IF NOT EXISTS diseases (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            description TEXT,
            symptoms TEXT,
            treatment TEXT,
            image_url VARCHAR(255),
            category VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')

        conn.commit()
        print("\u2705 Database initialization completed successfully.")

    except mysql.connector.Error as err:
        print(f"❌ Lỗi trong quá trình khởi tạo cơ sở dữ liệu: {err}")
        conn.rollback()
    finally:
        conn.close()
        
def delete_orders_before_id(threshold=83):
    conn = get_db_connection()
    if conn is None:
        print("❌ Không kết nối được CSDL.")
        return
    try:
        with conn.cursor() as c:
            c.execute("DELETE FROM orders WHERE id < %s", (threshold,))
            conn.commit()
            print(f"✅ Đã xoá {c.rowcount} đơn hàng có id < {threshold}.")
    finally:
        conn.close()


if __name__ == '__main__':
    init_db()
    delete_orders_before_id()  # Thay vì delete_old_orders()
