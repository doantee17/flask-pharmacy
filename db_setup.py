# db_setup.py
import mysql.connector
import os
from flask_bcrypt import Bcrypt # Đảm bảo bạn đã import Bcrypt ở đây

# Replace with your MySQL credentials
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
        print("✅ Kết nối database thành công.")
        return conn
    except mysql.connector.Error as err:
        print(f"❌ Lỗi khi kết nối database: {err}")
        return None


def create_database_if_not_exists():
    # Connect without specifying a database to create it
    temp_config = DB_CONFIG.copy()
    db_name = temp_config.pop('database') # Get the database name
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

def init_db():
    create_database_if_not_exists()
    conn = get_db_connection()
    if conn is None:
        print("Could not establish database connection for initialization.")
        return

    c = conn.cursor()

    try:
        # Bảng người dùng
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) UNIQUE NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                role VARCHAR(20) DEFAULT 'user', -- <<< ĐÃ THÊM CỘT ROLE
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        print("Bảng 'users' đã được tạo hoặc đã tồn tại.")

        # Thêm cột 'role' nếu nó chưa tồn tại (cho các DB cũ)
        try:
            c.execute("ALTER TABLE users ADD COLUMN role VARCHAR(20) DEFAULT 'user'")
            print("Cột 'role' đã được thêm vào bảng 'users'.")
        except mysql.connector.Error as err:
            if "Duplicate column name 'role'" in str(err):
                print("Cột 'role' đã tồn tại trong bảng 'users'.")
            else:
                print(f"Lỗi khi thêm cột 'role' vào bảng 'users': {err}")


        # Bảng sản phẩm
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
        print("Bảng 'products' đã được tạo hoặc đã tồn tại.")

                # Bảng đơn hàng
        c.execute('''CREATE TABLE IF NOT EXISTS orders (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            product_id INT,
            quantity INT NOT NULL,
            total_price DECIMAL(10, 2) NOT NULL,
            status VARCHAR(50) DEFAULT 'pending',
            full_name VARCHAR(255),
            phone VARCHAR(20),
            email VARCHAR(255),
            address TEXT,
            payment_method VARCHAR(50),
            notes TEXT,
            admin_notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
            FOREIGN KEY (product_id) REFERENCES products (id) ON DELETE CASCADE
        )''')

        print("Bảng 'orders' đã được tạo hoặc đã tồn tại.")

        # Thêm cột 'admin_notes' nếu chưa tồn tại (DB cũ)
        try:
            c.execute("ALTER TABLE orders ADD COLUMN admin_notes TEXT")
            print("Cột 'admin_notes' đã được thêm vào bảng 'orders'.")
        except mysql.connector.Error as err:
            if "Duplicate column name 'admin_notes'" in str(err):
                print("Cột 'admin_notes' đã tồn tại trong bảng 'orders'.")
            else:
                print(f"Lỗi khi thêm cột 'admin_notes': {err}")

        # Thêm cột 'city'
        try:
            c.execute("ALTER TABLE orders ADD COLUMN city VARCHAR(100)")
            print("Đã thêm cột 'city' vào bảng orders.")
        except mysql.connector.Error as err:
            if "Duplicate column name 'city'" in str(err):
                print("Cột 'city' đã tồn tại.")
            else:
                print(f"Lỗi khi thêm cột 'city': {err}")

        # Thêm cột 'district'
        try:
            c.execute("ALTER TABLE orders ADD COLUMN district VARCHAR(100)")
            print("Đã thêm cột 'district' vào bảng orders.")
        except mysql.connector.Error as err:
            if "Duplicate column name 'district'" in str(err):
                print("Cột 'district' đã tồn tại.")
            else:
                print(f"Lỗi khi thêm cột 'district': {err}")

        # Thêm các cột khách hàng còn thiếu (full_name, phone, email, address, payment_method, notes)
        columns_to_add = {
            "full_name": "VARCHAR(255)",
            "phone": "VARCHAR(20)",
            "email": "VARCHAR(255)",
            "address": "TEXT",
            "payment_method": "VARCHAR(50)",
            "notes": "TEXT"
        }

        for column, col_type in columns_to_add.items():
            try:
                c.execute(f"ALTER TABLE orders ADD COLUMN {column} {col_type}")
                print(f"Đã thêm cột '{column}' vào bảng orders.")
            except mysql.connector.Error as err:
                if f"Duplicate column name '{column}'" in str(err):
                    print(f"Cột '{column}' đã tồn tại.")
                else:
                    print(f"Lỗi khi thêm cột '{column}': {err}")

        

        # Bảng thông tin bệnh
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
        print("Bảng 'diseases' đã được tạo hoặc đã tồn tại.")

        # Thêm tài khoản admin
        bcrypt_instance = Bcrypt() # Khởi tạo Bcrypt instance
        admin_password = bcrypt_instance.generate_password_hash('admin123').decode('utf-8')
        
        # Kiểm tra xem tài khoản admin đã tồn tại chưa
        c.execute("SELECT id FROM users WHERE username = %s", ('admin',))
        existing_admin = c.fetchone()
        
        if not existing_admin:
            c.execute('''
                INSERT INTO users (username, email, password_hash, role)
                VALUES (%s, %s, %s, %s)
            ''', ('admin', 'admin@pharmacy.com', admin_password, 'admin'))
            conn.commit() # Commit ngay sau khi chèn admin để đảm bảo lưu
            print("Tài khoản admin 'admin@pharmacy.com' đã được tạo.")
        else:
            print("Tài khoản admin đã tồn tại. Bỏ qua chèn.")

        # Thêm dữ liệu mẫu sản phẩm
        sample_products = [
            ('Vitamin C 500mg', 'thuc_pham_cn', 150000.00, 'Tăng cường đề kháng, chống oxy hóa', 'https://via.placeholder.com/200x200/FF6B35/FFFFFF?text=VitC', 50),
            ('Omega 3-6-9', 'thuc_pham_cn', 320000.00, 'Bổ não, tốt cho tim mạch', 'https://via.placeholder.com/200x200/32CD32/FFFFFF?text=Omega', 30),
            ('Canxi + D3', 'thuc_pham_cn', 250000.00, 'Tăng cường xương khớp', 'https://via.placeholder.com/200x200/4169E1/FFFFFF?text=CaD3', 40),
            ('Sắt + Acid Folic', 'thuc_pham_cn', 180000.00, 'Bổ máu, chống thiếu máu', 'https://via.placeholder.com/200x200/FF1493/FFFFFF?text=Iron', 35),
            ('Coenzyme Q10', 'thuc_pham_cn', 450000.00, 'Tăng cường năng lượng tim mạch', 'https://via.placeholder.com/200x200/9932CC/FFFFFF?text=Q10', 25),
            ('Kem chống nắng SPF50', 'duoc_my_pham', 280000.00, 'Bảo vệ da khỏi tia UV', 'https://via.placeholder.com/200x200/87CEEB/FFFFFF?text=SPF50', 25),
            ('Serum Vitamin E', 'duoc_my_pham', 350000.00, 'Dưỡng ẩm, chống lão hóa', 'https://via.placeholder.com/200x200/DDA0DD/FFFFFF?text=VitE', 20),
            ('Sữa rửa mặt dịu nhẹ', 'duoc_my_pham', 120000.00, 'Làm sạch da không gây khô', 'https://via.placeholder.com/200x200/98FB98/FFFFFF?text=Face', 45),
            ('Kem dưỡng ẩm ban đêm', 'duoc_my_pham', 390000.00, 'Phục hồi da ban đêm', 'https://via.placeholder.com/200x200/FFB6C1/FFFFFF?text=Night', 15),
            ('Nhiệt kế điện tử', 'dung_cu_yt', 85000.00, 'Đo nhiệt độ chính xác', 'https://via.placeholder.com/200x200/FFD700/FFFFFF?text=Temp', 60),
            ('Máy đo huyết áp', 'dung_cu_yt', 450000.00, 'Theo dõi huyết áp tại nhà', 'https://via.placeholder.com/200x200/FF69B4/FFFFFF?text=BP', 15),
            ('Que thử đường huyết', 'dung_cu_yt', 25000.00, 'Kiểm tra đường huyết nhanh', 'https://via.placeholder.com/200x200/20B2AA/FFFFFF?text=Test', 100),
            ('Máy xông mũi họng', 'dung_cu_yt', 320000.00, 'Điều trị viêm đường hô hấp', 'https://via.placeholder.com/200x200/4169E1/FFFFFF?text=Neb', 8),
            ('Paracetamol 500mg', 'thuoc', 45000.00, 'Giảm đau, hạ sốt', 'https://via.placeholder.com/200x200/DC143C/FFFFFF?text=Para', 80),
            ('Amoxicillin 250mg', 'thuoc', 65000.00, 'Kháng sinh điều trị nhiễm khuẩn', 'https://via.placeholder.com/200x200/228B22/FFFFFF?text=Amox', 60),
            ('Ibuprofen 400mg', 'thuoc', 55000.00, 'Chống viêm, giảm đau', 'https://via.placeholder.com/200x200/4682B4/FFFFFF?text=Ibu', 70),
            ('Omeprazole 20mg', 'thuoc', 85000.00, 'Điều trị viêm loét dạ dày', 'https://via.placeholder.com/200x200/8B008B/FFFFFF?text=Ome', 45)
        ]

        for product in sample_products:
            try:
                # Kiểm tra xem sản phẩm đã tồn tại chưa trước khi chèn
                c.execute("SELECT id FROM products WHERE name = %s", (product[0],))
                existing_product = c.fetchone()
                if not existing_product:
                    c.execute('INSERT INTO products (name, category, price, description, image_url, stock_quantity) VALUES (%s, %s, %s, %s, %s, %s)', product)
                    print(f"Sản phẩm '{product[0]}' đã được thêm.")
                else:
                    print(f"Sản phẩm '{product[0]}' đã tồn tại. Bỏ qua chèn.")
            except mysql.connector.Error as err:
                print(f"Lỗi khi chèn sản phẩm '{product[0]}': {err}")
                conn.rollback() # Rollback nếu có lỗi

        # Thêm dữ liệu bệnh mẫu
        sample_diseases = [
            ('Cảm cúm', 'Bệnh nhiễm trùng đường hô hấp do virus gây ra, thường xảy ra vào mùa lạnh', 'Sốt cao, ho khan hoặc có đờm, chảy nước mũi, nghẹt mũi, đau đầu, đau họng, mệt mỏi toàn thân', 'Nghỉ ngơi đầy đủ, uống nhiều nước ấm, dùng thuốc hạ sốt, giảm đau. Có thể dùng thuốc kháng virus nếu cần thiết', 'https://via.placeholder.com/300x200/FF6B6B/FFFFFF?text=Flu', 'respiratory'),
            ('Đau dạ dày', 'Tình trạng viêm niêm mạc dạ dày gây đau và khó chịu vùng thượng vị', 'Đau bụng trên, buồn nôn, nôn, ợ hơi, cảm giác đầy bụng, ăn không ngon miệng', 'Ăn uống điều độ, tránh thức ăn cay nóng, dùng thuốc kháng acid, thuốc bảo vệ niêm mạc dạ dày', 'https://via.placeholder.com/300x200/4ECDC4/FFFFFF?text=Stomach', 'digestive'),
            ('Cao huyết áp', 'Tình trạng huyết áp cao kéo dài, có thể gây biến chứng tim mạch nghiêm trọng', 'Đau đầu, hoa mắt, chóng mặt, mệt mệt, đau ngực, khó thở khi gắng sức', 'Ăn ít muối, tập thể dục đều đặn, kiểm soát cân nặng, dùng thuốc hạ áp theo chỉ định bác sĩ', 'https://via.placeholder.com/300x200/45B7D1/FFFFFF?text=BP', 'cardiovascular'),
            ('Tiểu đường', 'Rối loạn chuyển hóa đường do thiếu insulin hoặc insulin không hoạt động hiệu quả', 'Khát nước nhiều, tiểu nhiều và nhiều lần, ăn nhiều nhưng sút cân, mệt mỏi, nhìn mờ', 'Chế độ ăn kiêng đường, tập thể dục thường xuyên, thuốc hạ đường huyết, kiểm soát đường huyết', 'https://via.placeholder.com/300x200/F7DC6F/FFFFFF?text=DM', 'endocrine'),
            ('Viêm khớp', 'Tình trạng viêm các khớp xương gây đau và hạn chế vận động', 'Đau khớp, sưng khớp, cứng khớp buổi sáng, khó vận động, có thể sốt nhẹ', 'Nghỉ ngơi khớp bị viêm, vật lý trị liệu, thuốc chống viêm, massage nhẹ nhàng', 'https://via.placeholder.com/300x200/BB8FCE/FFFFFF?text=Joint', 'musculoskeletal'),
            ('Viêm họng', 'Viêm nhiễm ở vùng họng do virus hoặc vi khuẩn', 'Đau họng, khó nuốt, họng đỏ, có thể sốt, ho khan', 'Berkumur nước muối ấm, uống nhiều nước, thuốc giảm đau, kháng sinh nếu do vi khuẩn', 'https://via.placeholder.com/300x200/FF7F50/FFFFFF?text=Throat', 'respiratory'),
            ('Táo bón', 'Tình trạng đi đại tiện khó khăn, ít lần hoặc phân cứng', 'Đại tiện ít hơn 3 lần/tuần, phân cứng, rặn nhiều khi đi đại tiện, đau bụng', 'Ăn nhiều rau xanh, uống nhiều nước, tập thể dục, thuốc nhuận tràng nhẹ', 'https://via.placeholder.com/300x200/32CD32/FFFFFF?text=Consti', 'digestive'),
            ('Mất ngủ', 'Rối loạn giấc ngủ, khó ngủ hoặc ngủ không sâu giấc', 'Khó ngủ, thức giấc nhiều lần, ngủ không sâu, mệt mỏi ban ngày, khó tập trung', 'Vệ sinh giấc ngủ tốt, tránh caffeine buổi tối, thư giãn trước khi ngủ, thuốc ngủ nếu cần', 'https://via.placeholder.com/300x200/6A5ACD/FFFFFF?text=Sleep', 'neurological')
        ]

        for disease in sample_diseases:
            try:
                c.execute("SELECT id FROM diseases WHERE name = %s", (disease[0],))
                existing_disease = c.fetchone()
                if not existing_disease:
                    c.execute('INSERT INTO diseases (name, description, symptoms, treatment, image_url, category) VALUES (%s, %s, %s, %s, %s, %s)', disease)
                    print(f"Bệnh '{disease[0]}' đã được thêm.")
                else:
                    print(f"Bệnh '{disease[0]}' đã tồn tại. Bỏ qua chèn.")
            except mysql.connector.Error as err:
                print(f"Lỗi khi chèn bệnh '{disease[0]}': {err}")
                conn.rollback() # Rollback nếu có lỗi

        conn.commit() # Commit tất cả các thay đổi sau khi chèn dữ liệu mẫu và bảng
        print("Database initialization complete.")

    except mysql.connector.Error as err:
        print(f"Lỗi trong quá trình khởi tạo cơ sở dữ liệu: {err}")
        conn.rollback() # Rollback nếu có lỗi lớn
    finally:
        if c:
            c.close()
        if conn:
            conn.close()

if __name__ == '__main__':
    # Bạn cần chạy tệp này một lần để thiết lập cơ sở dữ liệu MySQL của mình
    # python db_setup.py
    init_db()