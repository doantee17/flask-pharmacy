from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_bcrypt import Bcrypt
import mysql.connector  # Import MySQL connector
from datetime import datetime
import pymysql  # Giữ nguyên import, nhưng khuyến nghị loại bỏ nếu không dùng
from functools import wraps
import os
import glob
from pytz import timezone, utc  # ← Dùng để chuyển timezone
from mysql.connector.conversion import MySQLConverter  # ← Dùng để ép kiểu datetime từ DB

# Cấu hình cơ sở dữ liệu
DB_CONFIG = {
    'host': 'crossover.proxy.rlwy.net',
    'port': 36164,
    'user': 'root',
    'password': 'bjcwCWhfUsOvSsHCJBsFiDKgCrnzvfHj',
    'database': 'railway'
}

app = Flask(__name__)
class CustomConverter(MySQLConverter):
    def _datetime_to_python(self, value, desc=None):
        return value  # Giữ nguyên kiểu datetime

# test connect git

app.secret_key = 'nha_thuoc_nhom14_secret_key'
bcrypt = Bcrypt(app)

# Thêm bộ lọc format_number
def format_number(value):
    try:
        return "{:,.0f}".format(float(value))
    except (ValueError, TypeError):
        return value
app.jinja_env.filters['format_number'] = format_number

# Định nghĩa filter format_datetime cho Jinja2
def format_datetime(value, format="%d/%m/%Y %H:%M"):
    if isinstance(value, datetime):
        value = value.replace(tzinfo=utc).astimezone(timezone('Asia/Ho_Chi_Minh'))
        return value.strftime(format)
    return value


app.jinja_env.filters['format_datetime'] = format_datetime



# Helper function to get a database connection
def get_db_connection():
    try:
        config_with_converter = DB_CONFIG.copy()
        config_with_converter['converter_class'] = CustomConverter
        conn = mysql.connector.connect(**config_with_converter)
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        flash('Database connection error!', 'error')
        return None
    



def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Vui lòng đăng nhập để truy cập trang này.', 'error')
            return redirect(url_for('login'))
        
        conn = get_db_connection()
        if conn is None:
            flash('Không thể kết nối đến cơ sở dữ liệu để kiểm tra quyền.', 'error')
            return redirect(url_for('home'))
        
        try:
            with conn.cursor(dictionary=True) as c:  # Cải tiến: Sử dụng with để đảm bảo đóng cursor
                c.execute('SELECT role FROM users WHERE id = %s', (session['user_id'],))  # Sửa lỗi: ? → %s
                user = c.fetchone()
                if not user or user['role'] != 'admin':
                    flash('Bạn không có quyền truy cập trang quản trị viên.', 'error')
                    return redirect(url_for('home'))
        except mysql.connector.Error as err:
            print(f"Lỗi khi kiểm tra quyền người dùng: {err}")
            flash('Lỗi khi kiểm tra quyền truy cập.', 'error')
            return redirect(url_for('home'))
        finally:
            conn.close()
        return f(*args, **kwargs)
    return decorated_function

@app.context_processor
def inject_cart_count():
    cart_count = 0
    if 'cart' in session:
        cart_count = sum(session['cart'].values())
    return dict(cart_item_count=cart_count)


# Routes chính
@app.route('/')
def home():
    role = None
    if 'user_id' in session:
        conn = get_db_connection()
        if conn is None:
            return render_template('home.html', username=session.get('username'), role=None)
        try:
            with conn.cursor() as c:  # Cải tiến: Sử dụng with
                c.execute('SELECT role FROM users WHERE id = %s', (session['user_id'],))  # Sửa lỗi: ? → %s
                user = c.fetchone()
                role = user[0] if user else None
        finally:
            conn.close()
    return render_template('home.html', username=session.get('username'), role=role)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        missing_fields = []
        if 'email' not in request.form:
            missing_fields.append('email')
        if 'password' not in request.form:
            missing_fields.append('password')
        
        if missing_fields:
            flash(f'Thiếu các trường: {", ".join(missing_fields)}!', 'error')
            return redirect(url_for('login'))
        
        email = request.form['email'].strip()
        password = request.form['password'].strip()
        
        empty_fields = []
        if not email:
            empty_fields.append('email')
        if not password:
            empty_fields.append('password')
        
        if empty_fields:
            flash(f'Các trường không được để trống: {", ".join(empty_fields)}!', 'error')
            return redirect(url_for('login'))
        
        conn = get_db_connection()
        if conn is None:
            return redirect(url_for('login'))
        try:
            with conn.cursor() as c:  # Cải tiến: Sử dụng with
                c.execute('SELECT * FROM users WHERE email = %s', (email,))  # Sửa lỗi: ? → %s
                user = c.fetchone()
                if user and bcrypt.check_password_hash(user[3], password):
                    session['user_id'] = user[0]
                    session['username'] = user[1]
                    session['role'] = user[5]  # user[5] là cột role (theo thứ tự bạn tạo bảng)

                    flash('Đăng nhập thành công!', 'success')
                    return redirect(url_for('home'))
                else:
                    flash('Tên đăng nhập hoặc mật khẩu không đúng!', 'error')
        finally:
            conn.close()
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    print("Phương thức yêu cầu:", request.method)
    if request.method == 'POST':
        print("Dữ liệu gửi lên (register):", dict(request.form))
        print("Các trường có trong form:", list(request.form.keys()))
        print("Toàn bộ request:", request.form)
        
        missing_fields = []
        if 'username' not in request.form:
            missing_fields.append('username')
        if 'email' not in request.form:
            missing_fields.append('email')
        if 'password' not in request.form:
            missing_fields.append('password')
        
        if missing_fields:
            flash(f'Thiếu các trường: {", ".join(missing_fields)}!', 'error')
            return redirect(url_for('register'))
        
        username = request.form['username'].strip()
        email = request.form['email'].strip()
        password = request.form['password'].strip()
        
        empty_fields = []
        if not username:
            empty_fields.append('username')
        if not email:
            empty_fields.append('email')
        if not password:
            empty_fields.append('password')
        
        if empty_fields:
            flash(f'Các trường không được để trống: {", ".join(empty_fields)}!', 'error')
            return redirect(url_for('register'))
        
        conn = get_db_connection()
        if conn is None:
            return redirect(url_for('register'))
        try:
            with conn.cursor() as c:  # Cải tiến: Sử dụng with
                password_hash = bcrypt.generate_password_hash(password).decode('utf-8')  # Cải tiến: Đảm bảo password_hash là chuỗi
                c.execute('INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)',  # Sửa lỗi: ? → %s
                         (username, email, password_hash))
                conn.commit()
                flash('Đăng ký thành công! Vui lòng đăng nhập.', 'success')
                return redirect(url_for('login'))
        except mysql.connector.Error as err:
            if err.errno == 1062:  # Duplicate entry for unique key
                flash('Tên đăng nhập hoặc email đã tồn tại!', 'error')
            else:
                flash(f'Lỗi đăng ký: {err}', 'error')
        finally:
            conn.close()

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Đã đăng xuất thành công!', 'success')
    return redirect(url_for('home'))



# Admin Panel
@app.route('/admin')
def admin_panel():
    if 'user_id' not in session:
        flash('Vui lòng đăng nhập để truy cập Admin Panel!', 'error')
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    if conn is None:
        return redirect(url_for('home'))
    try:
        with conn.cursor() as c:  # Cải tiến: Sử dụng with
            c.execute('SELECT role FROM users WHERE id = %s', (session['user_id'],))  # Sửa lỗi: ? → %s
            user = c.fetchone()
            if not user or user[0] != 'admin':
                flash('Bạn không có quyền truy cập Admin Panel!', 'error')
                return redirect(url_for('home'))
            
            c.execute('SELECT COUNT(*) FROM products')
            total_products = c.fetchone()[0]
            
            c.execute('SELECT COUNT(*) FROM orders')
            total_orders = c.fetchone()[0]

            c.execute('SELECT COUNT(*) FROM orders WHERE status = %s', ('pending',))
            pending_orders = c.fetchone()[0]
            
            c.execute('SELECT COUNT(*) FROM users')
            total_users = c.fetchone()[0]
            
            c.execute('''SELECT o.id, u.username, p.name, o.quantity, o.total_price, o.status, o.created_at
                        FROM orders o
                        JOIN users u ON o.user_id = u.id
                        JOIN products p ON o.product_id = p.id
                        ORDER BY o.created_at DESC
                        LIMIT 10''')
            recent_orders = c.fetchall()
        
        stats = {
            'total_products': total_products,
            'total_orders': total_orders,
            'pending_orders': pending_orders,
            'total_users': total_users
        }
        
        return render_template('admin_panel_html/admin.html', 
                             stats=stats, 
                             recent_orders=recent_orders, 
                             username=session.get('username'))
    finally:
        conn.close()

@app.route('/admin/products')
def admin_products():
    if 'user_id' not in session:
        flash('Vui lòng đăng nhập để truy cập Admin Panel!', 'error')
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    if conn is None:
        return redirect(url_for('home'))
    
    try:
        with conn.cursor(dictionary=True) as c:
            c.execute('SELECT role FROM users WHERE id = %s', (session['user_id'],))
            user = c.fetchone()
            if not user or user['role'] != 'admin':
                flash('Bạn không có quyền truy cập Admin Panel!', 'error')
                return redirect(url_for('home'))
            
            # LẤY PARAMETER CATEGORY TỪ URL
            category_filter = request.args.get('category', '')
            
            # XÂY DỰNG QUERY DỰA TRÊN FILTER
            if category_filter and category_filter.strip():
                # Nếu có filter category, chỉ lấy sản phẩm thuộc category đó
                query = 'SELECT * FROM products WHERE category = %s ORDER BY name'
                c.execute(query, (category_filter,))
            else:
                # Nếu không có filter, lấy tất cả sản phẩm
                c.execute('SELECT * FROM products ORDER BY name')
            
            products = c.fetchall()
        
        # Đảm bảo mỗi sản phẩm đều là dict và có trường 'price'
        for product in products:
            if 'price' not in product or product['price'] is None:
                product['price'] = 0

        # TRUYỀN THÊM selected_category VÀO TEMPLATE
        return render_template('admin_panel_html/admin_products.html', 
                             products=products, 
                             username=session.get('username'),
                             selected_category=category_filter)  # Thêm dòng này
    finally:
        conn.close()

@app.route('/admin/product_detail/<int:product_id>', endpoint='product_detail')
@admin_required
def product_detail(product_id):
    product = get_product_by_id(product_id)
    if not product:
        flash('Sản phẩm không tồn tại!', 'error')
        return redirect(url_for('admin_products'))
    
    return render_template('product_detail.html', product=product)



@app.route('/admin/add_product', methods=['GET', 'POST'])
@admin_required
def add_product():
    if request.method == 'POST':
        # Kiểm tra các trường bắt buộc
        required_fields = ['name', 'category', 'price', 'description', 'image_url', 'stock_quantity']
        for field in required_fields:
            if field not in request.form or not request.form[field].strip():
                flash(f'Trường {field} là bắt buộc!', 'error')
                return render_template('add_product.html')

        name = request.form['name'].strip()
        category = request.form['category'].strip()
        description = request.form['description'].strip()
        image_url = request.form['image_url'].strip()
        
        # Xử lý price
        try:
            price = float(request.form['price'])  # Sửa lỗi: Xử lý đúng giá trị thập phân
            if price < 0:
                raise ValueError("Giá không được âm")
        except ValueError:
            flash('Giá không hợp lệ! Vui lòng nhập số hợp lệ (ví dụ: 1234.56)', 'error')
            return render_template('add_product.html')

        # Xử lý stock_quantity
        try:
            stock_quantity = int(request.form['stock_quantity'])
            if stock_quantity < 0:
                raise ValueError("Số lượng tồn kho không được âm")
        except ValueError:
            flash('Số lượng tồn kho không hợp lệ! Vui lòng nhập số nguyên', 'error')
            return render_template('add_product.html')

        conn = get_db_connection()
        if conn is None:
            flash('Lỗi kết nối CSDL.', 'error')
            return jsonify({'success': False, 'message': 'Lỗi kết nối CSDL.'})

        try:
            with conn.cursor() as c:
                sql = 'INSERT INTO products (name, category, price, description, image_url, stock_quantity) VALUES (%s, %s, %s, %s, %s, %s)'
                params = (name, category, price, description, image_url, stock_quantity)
                print(f"SQL: {sql}")  # Cải tiến: In câu lệnh SQL và tham số để debug
                print(f"Params: {params}")
                c.execute(sql, params)
                conn.commit()
            flash('Thêm sản phẩm thành công!', 'success')
            return redirect(url_for('admin_products'))
        except mysql.connector.Error as err:
            flash(f'Lỗi khi thêm sản phẩm: {err} (SQL: {c._executed})', 'error')
            print(f"Executed SQL: {c._executed}")  # Cải tiến: In câu lệnh thực tế
        finally:
            conn.close()
        # Lấy danh sách ảnh từ thư mục static/images/products
    image_folder = os.path.join(app.static_folder, 'images/products')
    image_files = []
    if os.path.exists(image_folder):
        image_files = [
            f'images/products/{f}'
            for f in os.listdir(image_folder)
            if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.gif'))
        ]
    return render_template('admin_panel_html/add_product.html', images=image_files)

@app.route('/admin/orders/<int:order_id>/status', methods=['POST'])
def update_order_status(order_id):
    if 'user_id' not in session or session.get('role') != 'admin':
        return jsonify({'success': False, 'message': 'Bạn không có quyền'}), 403

    data = request.get_json()
    new_status = data.get('status')
    admin_notes = data.get('admin_notes', None)

    if new_status not in ['pending', 'confirmed', 'shipped', 'cancelled']:
        return jsonify({'success': False, 'message': 'Trạng thái không hợp lệ'}), 400

    conn = get_db_connection()
    if conn is None:
        return jsonify({'success': False, 'message': 'Không thể kết nối CSDL'}), 500

    try:
        with conn.cursor() as c:
            sql = 'UPDATE orders SET status = %s'
            params = [new_status]

            if admin_notes:
                sql += ', admin_notes = %s'
                params.append(admin_notes)

            sql += ' WHERE id = %s'
            params.append(order_id)

            c.execute(sql, tuple(params))
            conn.commit()

        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        conn.close()
        
@app.route('/admin/orders/<int:order_id>/notes', methods=['POST'])
@admin_required
def update_admin_notes(order_id):
    data = request.get_json()
    notes = data.get('admin_notes')

    if not notes:
        return jsonify({'success': False, 'message': 'Ghi chú không được để trống'}), 400

    conn = get_db_connection()
    if conn is None:
        return jsonify({'success': False, 'message': 'Lỗi kết nối cơ sở dữ liệu'}), 500

    try:
        with conn.cursor() as c:
            c.execute('UPDATE orders SET admin_notes = %s WHERE id = %s', (notes, order_id))
            conn.commit()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        conn.close()



@app.route('/admin/diseases')
def admin_diseases():
    """Hiển thị danh sách tất cả bệnh"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Lấy tất cả bệnh từ database
        cursor.execute('''
            SELECT id, name, category, description, symptoms, treatment, image_url, created_at
            FROM diseases 
            ORDER BY created_at DESC
        ''')
        diseases = cursor.fetchall()
        conn.close()
        
        # Chuyển đổi category code sang tiếng Việt để hiển thị
        category_names = {
            'respiratory': 'Hô hấp',
            'cardiovascular': 'Tim mạch', 
            'digestive': 'Tiêu hóa',
            'neurological': 'Thần kinh',
            'dermatology': 'Da liễu',
            'endocrine': 'Nội tiết',
            'musculoskeletal': 'Xương khớp',
            'other': 'Khác'
        }
        
        # Chuyển đổi dữ liệu để hiển thị
        diseases_list = []
        for disease in diseases:
            disease_dict = {
                'id': disease[0],
                'name': disease[1],
                'category': category_names.get(disease[2], disease[2]),
                'description': disease[3],
                'symptoms': disease[4].split('; ') if disease[4] else [],
                'treatment': disease[5].split('; ') if disease[5] else [],
                'image_url': disease[6],
                'created_at': disease[7]
            }
            diseases_list.append(disease_dict)

        return render_template('admin_panel_html/admin_diseases.html', diseases=diseases_list)

    except Exception as e:
        flash(f'Có lỗi xảy ra: {str(e)}', 'error')
        return redirect(url_for('admin_panel_html/admin_panel'))
@app.route('/admin/add_disease', methods=['GET', 'POST'])
def add_disease():
    if request.method == 'POST':
        try:
            # Lấy dữ liệu từ form
            disease_name = request.form.get('disease_name')
            disease_category = request.form.get('disease_category')
            description = request.form.get('description')
            
            # Lấy danh sách triệu chứng và điều trị
            symptoms_list = request.form.getlist('symptoms[]')
            treatments_list = request.form.getlist('treatments[]')
            
            # Loại bỏ các item rỗng
            symptoms_list = [s.strip() for s in symptoms_list if s.strip()]
            treatments_list = [t.strip() for t in treatments_list if t.strip()]
            
            # Chuyển đổi danh sách thành chuỗi
            symptoms = '; '.join(symptoms_list)
            treatment = '; '.join(treatments_list)
            
            # Xử lý upload hình ảnh
            image_url = request.form.get('disease_image', '/static/images/default-disease.jpg')
            # Chuyển đổi category sang English để phù hợp với filter
            category_mapping = {
                'Hô hấp': 'respiratory',
                'Tim mạch': 'cardiovascular', 
                'Tiêu hóa': 'digestive',
                'Thần kinh': 'neurological',
                'Da liễu': 'dermatology',
                'Nội tiết': 'endocrine',
                'Xương khớp': 'musculoskeletal',
                'Khác': 'other'
            }
            category_code = category_mapping.get(disease_category, 'other')
            
            # Lưu vào database
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO diseases (name, category, description, symptoms, treatment, image_url, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            ''', (disease_name, category_code, description, symptoms, treatment, image_url, datetime.now()))
            
            conn.commit()
            conn.close()
            
            flash('Thêm bệnh mới thành công!', 'success')
            return redirect(url_for('admin_diseases'))

        except Exception as e:
            flash(f'Có lỗi xảy ra: {str(e)}', 'error')
            return redirect(url_for('admin_panel_html/add_disease'))

    # GET request - hiển thị form thêm bệnh
        # GET request - hiển thị form thêm bệnh với danh sách ảnh từ thư mục static
    image_folder = os.path.join(app.static_folder, 'images/diseases')
    image_files = [
        f'/static/images/diseases/{filename}'
        for filename in os.listdir(image_folder)
        if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.gif'))
    ]
    return render_template('admin_panel_html/admin_add_diseases.html', images=image_files)

@app.route('/admin/diseases/<int:disease_id>/delete', methods=['DELETE'])
def delete_disease(disease_id):
    conn = get_db_connection()
    if conn is None:
        return jsonify({'success': False, 'message': 'Lỗi kết nối cơ sở dữ liệu'}), 500
    try:
        with conn.cursor() as c:
            c.execute('DELETE FROM diseases WHERE id = %s', (disease_id,))
            
            if c.rowcount > 0:
                conn.commit()
                return jsonify({'success': True, 'message': 'Đã xóa bệnh thành công'})
            else:
                return jsonify({'success': False, 'message': 'Không tìm thấy bệnh'})
    except Exception as e:
        conn.rollback()
        return jsonify({'success': False, 'message': str(e)})
    finally:
        conn.close()
        

@app.route('/admin/diseases/<int:disease_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_disease(disease_id):
    conn = get_db_connection()
    if conn is None:
        flash('Không thể kết nối cơ sở dữ liệu', 'danger')
        return redirect(url_for('admin_diseases'))

    # ✅ Load danh sách ảnh trong static/images/diseases
    image_folder = os.path.join(app.static_folder, 'images', 'diseases')
    if os.path.exists(image_folder):
        image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.gif', '*.webp']
        images = []
        for ext in image_extensions:
            images.extend(glob.glob(os.path.join(image_folder, ext)))
            images.extend(glob.glob(os.path.join(image_folder, ext.upper())))

        # Chuyển absolute path → URL tĩnh
        images = [
            '/static/images/diseases/' + os.path.basename(img)
            for img in images
        ]
    else:
        images = []

    try:
        with conn.cursor(dictionary=True) as c:
            if request.method == 'POST':
                # Lấy dữ liệu từ form
                name = request.form.get('disease_name')
                category = request.form.get('disease_category')
                description = request.form.get('description')

                symptoms_list = request.form.getlist('symptoms[]')
                treatment_list = request.form.getlist('treatments[]')
                image_url = request.form.get('disease_image')

                # Làm sạch dữ liệu
                symptoms = '; '.join([s.strip() for s in symptoms_list if s.strip()])
                treatment = '; '.join([t.strip() for t in treatment_list if t.strip()])

                # Ánh xạ danh mục về dạng code (nếu cần)
                category_mapping = {
                    'Hô hấp': 'respiratory',
                    'Tim mạch': 'cardiovascular',
                    'Tiêu hóa': 'digestive',
                    'Nội tiết': 'endocrine',
                    'Xương khớp': 'musculoskeletal',
                    'Khác': 'other'
                }
                category_code = category_mapping.get(category, 'other')

                # Cập nhật DB
                c.execute('''
                    UPDATE diseases
                    SET name = %s,
                        category = %s,
                        description = %s,
                        symptoms = %s,
                        treatment = %s,
                        image_url = %s
                    WHERE id = %s
                ''', (name, category_code, description, symptoms, treatment, image_url, disease_id))
                conn.commit()

                flash('Cập nhật bệnh thành công!', 'success')
                return redirect(url_for('admin_diseases'))

            # GET: load dữ liệu cũ để hiển thị
            c.execute('SELECT * FROM diseases WHERE id = %s', (disease_id,))
            disease = c.fetchone()

            # Ánh xạ category từ code → tiếng Việt để hiển thị
            category_reverse = {
                'respiratory': 'Hô hấp',
                'cardiovascular': 'Tim mạch',
                'digestive': 'Tiêu hóa',
                'endocrine': 'Nội tiết',
                'musculoskeletal': 'Xương khớp',
                'other': 'Khác'
            }
            if disease:
                disease['category'] = category_reverse.get(disease['category'], disease['category'])
                return render_template('admin_panel_html/edit_disease.html', disease=disease, images=images)
            else:
                flash('Không tìm thấy bệnh cần sửa', 'danger')
                return redirect(url_for('admin_diseases'))

    except Exception as e:
        flash(f'Lỗi khi cập nhật: {str(e)}', 'danger')
        return redirect(url_for('admin_diseases'))
    finally:
        conn.close()




@app.route('/admin/orders/<int:order_id>/delete', methods=['DELETE'])
def delete_order(order_id):
    conn = get_db_connection()
    if conn is None:
        return jsonify({'success': False, 'message': 'Lỗi kết nối cơ sở dữ liệu'}), 500
    try:
        with conn.cursor() as c:
            # Không cần xóa order_items vì không tồn tại
            c.execute('DELETE FROM orders WHERE id = %s', (order_id,))
            
            if c.rowcount > 0:
                conn.commit()
                return jsonify({'success': True, 'message': 'Đã xóa đơn hàng thành công'})
            else:
                return jsonify({'success': False, 'message': 'Không tìm thấy đơn hàng'})
    except Exception as e:
        conn.rollback()
        return jsonify({'success': False, 'message': str(e)})
    finally:
        conn.close()



@app.route('/admin/edit_product/<int:product_id>', methods=['GET', 'POST'])
@admin_required
def edit_product(product_id):
    conn = get_db_connection()
    if conn is None:
        flash('Lỗi kết nối CSDL.', 'error')
        return redirect(url_for('admin_products'))

    try:
        with conn.cursor(dictionary=True) as c:
            c.execute('SELECT * FROM products WHERE id = %s', (product_id,))
            product = c.fetchone()
    except mysql.connector.Error as err:
        print(f"Lỗi khi lấy sản phẩm để sửa: {err}")
        flash('Lỗi khi tải thông tin sản phẩm.', 'error')
        return redirect(url_for('admin_products'))
    finally:
        conn.close()

    if not product:
        flash('Sản phẩm không tồn tại.', 'error')
        return redirect(url_for('admin_products'))

    # ✅ Load danh sách ảnh từ static/images/products
    image_folder = os.path.join(app.static_folder, 'images', 'products')
    image_files = []
    if os.path.exists(image_folder):
        image_files = [
            '/static/images/products/' + f
            for f in os.listdir(image_folder)
            if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.gif'))
        ]

    if request.method == 'POST':
        required_fields = ['name', 'category', 'price', 'description', 'image_url', 'stock_quantity']
        for field in required_fields:
            if field not in request.form or not request.form[field].strip():
                flash(f'Trường {field} là bắt buộc!', 'error')
                return render_template('admin_panel_html/edit_product.html', product=product, images=image_files)

        name = request.form['name'].strip()
        category = request.form['category'].strip()
        description = request.form['description'].strip()
        image_url = request.form['image_url'].strip()

        # Xử lý price
        try:
            price = float(request.form['price'])
            if price < 0:
                raise ValueError("Giá không được âm")
        except ValueError:
            flash('Giá không hợp lệ! Vui lòng nhập số hợp lệ (ví dụ: 1234.56)', 'error')
            return render_template('admin_panel_html/edit_product.html', product=product, images=image_files)

        # Xử lý stock_quantity
        try:
            stock_quantity = int(request.form['stock_quantity'])
            if stock_quantity < 0:
                raise ValueError("Số lượng tồn kho không được âm")
        except ValueError:
            flash('Số lượng tồn kho không hợp lệ! Vui lòng nhập số nguyên', 'error')
            return render_template('admin_panel_html/edit_product.html', product=product, images=image_files)

        conn = get_db_connection()
        if conn is None:
            flash('Lỗi kết nối CSDL.', 'error')
            return redirect(url_for('admin_products'))
        try:
            with conn.cursor() as c:
                sql = '''
                    UPDATE products
                    SET name = %s, category = %s, price = %s,
                        description = %s, image_url = %s, stock_quantity = %s
                    WHERE id = %s
                '''
                params = (name, category, price, description, image_url, stock_quantity, product_id)
                c.execute(sql, params)
                conn.commit()
            flash('Cập nhật sản phẩm thành công!', 'success')
            return redirect(url_for('admin_products'))
        except mysql.connector.Error as err:
            flash(f'Lỗi khi cập nhật sản phẩm: {err}', 'error')
        finally:
            conn.close()

    return render_template('admin_panel_html/edit_product.html', product=product, images=image_files)


@app.route('/admin/delete_product/<int:product_id>', methods=['POST'])
@admin_required
def delete_product(product_id):
    conn = get_db_connection()
    if conn is None:
        return jsonify({'success': False, 'message': 'Không thể kết nối đến cơ sở dữ liệu'})
    
    try:
        with conn.cursor() as c:
            c.execute('SELECT id FROM products WHERE id = %s', (product_id,))  # Sửa lỗi: ? → %s
            if not c.fetchone():
                return jsonify({'success': False, 'message': 'Sản phẩm không tồn tại'})
            
            c.execute('DELETE FROM products WHERE id = %s', (product_id,))  # Sửa lỗi: ? → %s
            conn.commit()
        return jsonify({'success': True, 'message': 'Xóa sản phẩm thành công'})
    except mysql.connector.Error as err:
        return jsonify({'success': False, 'message': f'Lỗi khi xóa sản phẩm: {str(err)}'})
    finally:
        conn.close()

@app.route('/admin/update_stock/<int:product_id>', methods=['POST'])
@admin_required
def update_stock(product_id):
    new_stock = request.json.get('new_stock')
    if new_stock is None or not isinstance(new_stock, int) or new_stock < 0:
        return jsonify({'success': False, 'message': 'Số lượng tồn kho không hợp lệ.'})

    conn = get_db_connection()
    if conn is None:
        return jsonify({'success': False, 'message': 'Lỗi kết nối CSDL.'})
    try:
        with conn.cursor() as c:
            c.execute('UPDATE products SET stock_quantity = %s WHERE id = %s', (new_stock, product_id))
            conn.commit()
        return jsonify({'success': True, 'message': 'Cập nhật tồn kho thành công.'})
    except mysql.connector.Error as err:
        return jsonify({'success': False, 'message': f'Lỗi khi cập nhật tồn kho: {str(err)}'})
    finally:
        conn.close()

@app.route('/admin/orders')
def admin_orders():
    conn = get_db_connection()
    if conn is None:
        print("❌ Không thể kết nối database trong admin_orders.")
        flash('Lỗi kết nối cơ sở dữ liệu. Vui lòng thử lại sau.', 'error')
        return redirect(url_for('home'))
    
    orders_raw = []
    total_orders = 0
    pending_orders = 0
    confirmed_orders = 0
    shipped_orders = 0
    cancelled_orders = 0

    # Lấy dữ liệu lọc từ request
    status = request.args.get('status')
    from_date = request.args.get('from_date')
    to_date = request.args.get('to_date')

    # Câu truy vấn có đầy đủ thông tin khách hàng
    query = '''SELECT o.id AS order_id, u.username, p.name AS product_name,
                      o.quantity, o.total_price, o.status, o.created_at, o.admin_notes,
                      o.full_name, o.phone, o.email, o.address, o.city, o.district,
                      o.payment_method, o.notes
               FROM orders o
               JOIN users u ON o.user_id = u.id
               JOIN products p ON o.product_id = p.id
               WHERE 1=1'''
    params = []

    if status:
        query += " AND o.status = %s"
        params.append(status)

    if from_date:
        query += " AND o.created_at >= %s"
        params.append(from_date)

    if to_date:
        query += " AND o.created_at <= %s"
        params.append(to_date)

    query += " ORDER BY o.created_at DESC"

    try:
        with conn.cursor(dictionary=True) as c:
            # Truy vấn danh sách đơn hàng
            c.execute(query, params)
            orders_raw = c.fetchall()

            # Thống kê
            c.execute('SELECT COUNT(*) AS total FROM orders')
            total_orders = c.fetchone()['total']

            c.execute("SELECT COUNT(*) AS count FROM orders WHERE status = %s", ('pending',))
            result = c.fetchone()
            pending_orders = result['count'] if result else 0

            c.execute("SELECT COUNT(*) AS count FROM orders WHERE status = %s", ('confirmed',))
            result = c.fetchone()
            confirmed_orders = result['count'] if result else 0

            c.execute("SELECT COUNT(*) AS count FROM orders WHERE status = %s", ('shipped',))
            result = c.fetchone()
            shipped_orders = result['count'] if result else 0

            c.execute("SELECT COUNT(*) AS count FROM orders WHERE status = %s", ('cancelled',))
            result = c.fetchone()
            cancelled_orders = result['count'] if result else 0

    except mysql.connector.Error as err:
        print(f"Lỗi khi lấy danh sách đơn hàng admin: {err}")
        flash('Lỗi khi tải danh sách đơn hàng.', 'error')
        return redirect(url_for('home'))
    finally:
        conn.close()

    # Gộp đơn hàng theo order_id
    orders = {}
    for row in orders_raw:
        order_id = row['order_id']
        if order_id not in orders:
            orders[order_id] = {
                'id': order_id,
                'username': row['username'],
                'status': row['status'],
                'created_at': row['created_at'],
                'admin_notes': row['admin_notes'],
                'full_name': row.get('full_name'),
                'phone': row.get('phone'),
                'email': row.get('email'),
                'address': row.get('address'),
                'city': row.get('city'),
                'district': row.get('district'),
                'payment_method': row.get('payment_method'),
                'notes': row.get('notes'),
                'order_items': [],
                'total_amount': 0
            }
        else:
           for field in ['full_name', 'email', 'phone', 'address', 'city', 'district']:
               if row.get(field):
                   orders[order_id][field] = row[field]


        item_price = (row['total_price'] / row['quantity']) if row['quantity'] else 0
        item = {
            'product_name': row['product_name'],
            'quantity': row['quantity'],
            'price': item_price,
        }
        orders[order_id]['order_items'].append(item)
        orders[order_id]['total_amount'] += row['total_price']

    orders_list = list(orders.values())

    return render_template('admin_panel_html/admin_orders.html',
                           orders=orders_list,
                           total_orders=total_orders,
                           pending_orders=pending_orders,
                           confirmed_orders=confirmed_orders,
                           shipped_orders=shipped_orders,
                           cancelled_orders=cancelled_orders,
                           from_date=from_date,
                           to_date=to_date,
                           status=status)


@app.route('/admin/users')
def admin_users():
    conn = get_db_connection()
    if conn is None:
        flash('Lỗi kết nối CSDL!', 'error')
        return redirect(url_for('admin_panel'))

    try:
        with conn.cursor(dictionary=True) as c:
            c.execute('SELECT * FROM users ORDER BY created_at DESC')
            users = c.fetchall()

            c.execute('SELECT role, COUNT(*) as count FROM users GROUP BY role')
            role_stats = c.fetchall()

        return render_template('admin_panel_html/admin_users.html', users=users, role_stats=role_stats)
    finally:
        conn.close()
        
@app.route('/admin/users/<int:user_id>/delete', methods=['POST'])
@admin_required
def delete_user(user_id):
    if user_id == session.get('user_id'):
        flash('Bạn không thể tự xoá chính mình!', 'error')
        return redirect(url_for('admin_users'))

    conn = get_db_connection()
    if conn is None:
        flash('Lỗi kết nối CSDL!', 'error')
        return redirect(url_for('admin_users'))

    try:
        with conn.cursor() as c:
            c.execute('DELETE FROM users WHERE id = %s', (user_id,))
            conn.commit()
            flash('Xoá người dùng thành công!', 'success')
    except Exception as e:
        flash(f'Lỗi khi xoá người dùng: {str(e)}', 'error')
    finally:
        conn.close()

    return redirect(url_for('admin_users'))


@app.route('/change-password', methods=['GET', 'POST'])
def change_password():
    if 'user_id' not in session:
        flash('Vui lòng đăng nhập để đổi mật khẩu.', 'error')
        return redirect(url_for('login'))

    if request.method == 'POST':
        current_password = request.form.get('current_password', '').strip()
        new_password = request.form.get('new_password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()

        if not current_password or not new_password or not confirm_password:
            flash('Vui lòng điền đầy đủ thông tin.', 'error')
            return redirect(url_for('change_password'))

        if new_password != confirm_password:
            flash('Mật khẩu mới và xác nhận không khớp.', 'error')
            return redirect(url_for('change_password'))

        conn = get_db_connection()
        if conn is None:
            flash('Không thể kết nối cơ sở dữ liệu.', 'error')
            return redirect(url_for('change_password'))

        try:
            with conn.cursor(dictionary=True) as c:
                c.execute('SELECT password_hash FROM users WHERE id = %s', (session['user_id'],))
                user = c.fetchone()
                if not user or not bcrypt.check_password_hash(user['password_hash'], current_password):
                    flash('Mật khẩu hiện tại không đúng.', 'error')
                    return redirect(url_for('change_password'))

                new_hash = bcrypt.generate_password_hash(new_password).decode('utf-8')
                c.execute('UPDATE users SET password_hash = %s WHERE id = %s', (new_hash, session['user_id']))
                conn.commit()

                flash('Đổi mật khẩu thành công!', 'success')
                return redirect(url_for('home'))
        finally:
            conn.close()

    return render_template('change_password.html')




# Routes sản phẩm
@app.route('/products/<category>')
def products(category):
    conn = get_db_connection()
    if conn is None:
        return redirect(url_for('home'))
    try:
        with conn.cursor(dictionary=True) as c:
            c.execute('SELECT * FROM products WHERE category = %s ORDER BY name', (category,))
            products = c.fetchall()
    finally:
        conn.close()
    
    category_names = {
        'thuc_pham_cn': 'Thực phẩm chức năng',
        'duoc_my_pham': 'Dược mỹ phẩm', 
        'dung_cu_yt': 'Dụng cụ y tế',
        'thuoc': 'Thuốc'
    }
    
    return render_template('sanpham.html', 
                         products=products, 
                         category=category,
                         category_name=category_names.get(category, 'Sản phẩm'),
                         username=session.get('username'),
                         role=session.get('role'))

def get_product_by_id(product_id):
    conn = get_db_connection()
    if conn is None:
        return None
    try:
        with conn.cursor(dictionary=True) as c:
            c.execute('SELECT * FROM products WHERE id = %s', (product_id,))  # Sửa lỗi: ? → %s
            product = c.fetchone()
        return product
    finally:
        conn.close()

@app.route('/buy/<int:product_id>')
def buy_product(product_id):
    if 'user_id' not in session:
        flash('Vui lòng đăng nhập để mua hàng!', 'error')
        return redirect(url_for('login'))
    
    product = get_product_by_id(product_id)
    
    if not product:
        flash('Sản phẩm không tồn tại!', 'error')
        return redirect(url_for('home'))
    
    return render_template('checkout.html', product=product, username=session.get('username'))

@app.route('/process_order', methods=['POST'])
def process_order():
    if 'user_id' not in session:
        flash('Vui lòng đăng nhập để đặt hàng!', 'error')
        return redirect(url_for('login'))

    try:
        product_ids = request.form.getlist('product_ids')
        quantities = request.form.getlist('quantities')

        if not product_ids or not quantities or len(product_ids) != len(quantities):
            flash('Dữ liệu sản phẩm không hợp lệ', 'error')
            return redirect(url_for('home'))

        full_name = request.form.get('full_name', '').strip()
        phone = request.form.get('phone', '').strip()
        email = request.form.get('email', '').strip()
        address = request.form.get('address', '').strip()
        city = request.form.get('city', '').strip()
        district = request.form.get('district', '').strip()
        payment_method = request.form.get('payment_method', 'cod')
        notes = request.form.get('notes', '').strip()

        conn = get_db_connection()
        if conn is None:
            return redirect(url_for('home'))

        total_price_all = 0
        order_ids = []

        try:
            with conn.cursor() as c:
                for i in range(len(product_ids)):
                    product_id = int(product_ids[i])
                    quantity = int(quantities[i])
                    product = get_product_by_id(product_id)
                    if not product:
                        continue  # hoặc bỏ qua, hoặc raise Exception tùy bạn

                    product_price = product['price']
                    subtotal = product_price * quantity
                    shipping_fee = 0  # bạn có thể cộng thêm 1 lần duy nhất nếu cần
                    total_price = subtotal + shipping_fee

                    c.execute('''
                        INSERT INTO orders (user_id, product_id, quantity, total_price,
                                            full_name, phone, email, address, city, district,
                                            payment_method, notes, status, created_at)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'pending', NOW())
                    ''', (
                        session['user_id'], product_id, quantity, total_price,
                        full_name, phone, email, address, city, district,
                        payment_method, notes
                    ))
                    conn.commit()
                    order_id = c.lastrowid
                    order_ids.append(order_id)
                    total_price_all += total_price

            return render_template(
                'buy.html',
                order_id=order_ids[0],  # hoặc truyền danh sách nếu muốn
                order_time=datetime.now().strftime("%d/%m/%Y %H:%M"),
                order={'total': total_price_all},
                payment_method=payment_method
            )
        finally:
            conn.close()

    except Exception as e:
        flash(f'Có lỗi khi đặt hàng: {str(e)}', 'error')
        return redirect(url_for('home'))


    
@app.route('/product/<int:product_id>')
def product_detail_public(product_id):
    product = get_product_by_id(product_id)  # Hàm này bạn đã có sẵn
    if not product:
        flash("Sản phẩm không tồn tại!", "error")
        return redirect(url_for('home'))  # hoặc url_for('products') nếu bạn có trang danh sách

    return render_template('product_detail.html', product=product)



@app.route('/order_success/<int:order_id>')
def order_success(order_id):
    return render_template('buy.html', username=session.get('username'))




#Phan gio hang + don hang
@app.route('/orders')
def view_orders():
    if 'user_id' not in session:
        flash('Vui lòng đăng nhập để xem đơn hàng!', 'error')
        return redirect(url_for('login'))

    # --- Truy vấn đơn hàng ---
    orders = []
    conn = get_db_connection()
    if conn is None:
        return redirect(url_for('home'))

    try:
        with conn.cursor(dictionary=True) as c:
            c.execute('''
                SELECT o.id, o.quantity, o.total_price, o.status, o.created_at, o.admin_notes,
                       p.name as product_name, p.price as product_price, p.image_url as product_image
                FROM orders o
                JOIN products p ON o.product_id = p.id
                WHERE o.user_id = %s
                ORDER BY o.created_at DESC
            ''', (session['user_id'],))
            orders = c.fetchall()

        for order in orders:
            if order['created_at']:
                order['created_at_formatted'] = order['created_at'].strftime('%d/%m/%Y %H:%M')
            else:
                order['created_at_formatted'] = 'N/A'
    finally:
        conn.close()

    # --- Truy vấn giỏ hàng từ session['cart'] ---
    cart_items = []
    cart = session.get('cart', {})
    if cart:
        conn = get_db_connection()
        try:
            with conn.cursor(dictionary=True) as c:
                product_ids = list(cart.keys())
                format_strings = ','.join(['%s'] * len(product_ids))
                c.execute(f"SELECT * FROM products WHERE id IN ({format_strings})", product_ids)
                products = c.fetchall()

                for product in products:
                    product_id = str(product['id'])
                    quantity = cart.get(product_id, 0)
                    cart_items.append({
                        'id': product['id'],
                        'product_name': product['name'],
                        'product_price': product['price'],
                        'product_image': product['image_url'],
                        'quantity': quantity,
                        'unit': 'sản phẩm',
                        'stock': product['stock_quantity'],
                        'created_at': None
                    })
        finally:
            conn.close()

    # --- Trả về giao diện ---
    return render_template(
        'checkitem.html',
        orders=orders,
        cart_items=cart_items,
        username=session.get('username')
    )

@app.route('/order-details/<int:order_id>')
def order_details(order_id):
    if 'user_id' not in session:
        flash('Vui lòng đăng nhập để xem chi tiết đơn hàng!', 'error')
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    if conn is None:
        return redirect(url_for('home'))
    try:
        with conn.cursor(dictionary=True) as c:
            c.execute('''SELECT o.id, o.quantity, o.total_price, o.status, o.created_at,
                               p.name, p.price, p.description, p.image_url
                        FROM orders o
                        JOIN products p ON o.product_id = p.id
                        WHERE o.id = %s AND o.user_id = %s''', (order_id, session['user_id']))
            order_data = c.fetchone()
        
        if not order_data:
            flash('Không tìm thấy đơn hàng!', 'error')
            return redirect(url_for('view_orders'))
        
        order = {
            'id': order_data['id'],
            'quantity': order_data['quantity'],
            'total_price': order_data['total_price'],
            'status': order_data['status'],
            'created_at': order_data['created_at'].strftime('%Y-%m-%d %H:%M:%S') if order_data['created_at'] else None,
            'product_name': order_data['name'],
            'product_price': order_data['price'],
            'product_description': order_data['description'],
            'product_image': order_data['image_url']
        }
        
        return render_template('order_details.html', order=order, username=session.get('username'))
    finally:
        conn.close()

@app.route('/cancel-order/<int:order_id>', methods=['POST'])
def cancel_order(order_id):
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Chưa đăng nhập'})

    conn = get_db_connection()
    if conn is None:
        return jsonify({'success': False, 'message': 'Không thể kết nối đến cơ sở dữ liệu'})
    try:
        with conn.cursor() as c:
            c.execute('SELECT status FROM orders WHERE id = %s AND user_id = %s', 
                     (order_id, session['user_id']))
            order = c.fetchone()
            
            if not order:
                return jsonify({'success': False, 'message': 'Không tìm thấy đơn hàng'})
            
            if order[0] != 'pending':
                return jsonify({'success': False, 'message': 'Không thể hủy đơn hàng này'})

            c.execute('UPDATE orders SET status = %s WHERE id = %s', ('cancelled', order_id))
            conn.commit()
        
        return jsonify({'success': True, 'message': 'Đã hủy đơn hàng thành công'})
    finally:
        conn.close()
        

@app.route('/api/cart-count')
def get_cart_count():
    if 'user_id' not in session:
        return jsonify({'count': 0})

    conn = get_db_connection()
    if conn is None:
        return jsonify({'count': 0})
    
    try:
        with conn.cursor() as c:
            c.execute('SELECT COUNT(*) FROM orders WHERE user_id = %s AND status != %s', 
                     (session['user_id'], 'cancelled'))
            count = c.fetchone()[0]
        return jsonify({'count': count})
    finally:
        conn.close()
        
@app.route('/api/add-to-cart', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    try:
        product_id = str(data.get('product_id'))
        quantity = int(data.get('quantity', 1))
    except (TypeError, ValueError):
        return jsonify({'success': False, 'message': 'Dữ liệu không hợp lệ'}), 400

    if not product_id:
        return jsonify({'success': False, 'message': 'Thiếu product_id'}), 400

    # Thêm vào session giỏ hàng
    cart = session.get('cart', {})
    cart[product_id] = cart.get(product_id, 0) + quantity
    session['cart'] = cart
    session.modified = True  # BẮT BUỘC để Flask biết session có thay đổi

    return jsonify({'success': True, 'message': 'Đã thêm vào giỏ hàng'})

@app.route('/remove-from-cart/<int:item_id>', methods=['POST'])
def remove_from_cart(item_id):
    cart = session.get('cart_items', [])
    updated_cart = [item for item in cart if item['id'] != item_id]
    session['cart_items'] = updated_cart

    return jsonify({'success': True})



#thanh toan don hang
@app.route('/checkout')
def checkout():
    item_ids = request.args.getlist('items')
    quantities = request.args.getlist('quantities')

    if not item_ids or not quantities or len(item_ids) != len(quantities):
        flash('Dữ liệu không hợp lệ cho thanh toán', 'error')
        return redirect(url_for('view_checkitem'))

    conn = get_db_connection()
    products = []
    try:
        with conn.cursor(dictionary=True) as cursor:
            format_strings = ','.join(['%s'] * len(item_ids))
            cursor.execute(f"SELECT * FROM products WHERE id IN ({format_strings})", item_ids)
            rows = cursor.fetchall()

            for row in rows:
                product_id_str = str(row['id'])
                if product_id_str in item_ids:
                    index = item_ids.index(product_id_str)
                    quantity = int(quantities[index])
                    row['quantity'] = quantity
                    row['total_price'] = row['price'] * quantity
                    products.append(row)
    finally:
        conn.close()

    return render_template('checkout.html', products=products)



@app.route('/diagnosis/<category>')
def diagnosis(category='all'):
    conn = get_db_connection()
    if conn is None:
        flash('Không thể kết nối cơ sở dữ liệu!', 'error')
        return redirect(url_for('home'))

    try:
        valid_categories = ['all', 'respiratory', 'digestive', 'cardiovascular', 'endocrine', 'musculoskeletal']
        if category not in valid_categories:
            return "Không tìm thấy danh mục!", 404

        with conn.cursor(dictionary=True) as c:
            if category == 'all':
                c.execute('SELECT id, name, description, symptoms, treatment, image_url, category FROM diseases ORDER BY name')
            else:
                c.execute('SELECT id, name, description, symptoms, treatment, image_url, category FROM diseases WHERE category = %s ORDER BY name', (category,))
            diseases = c.fetchall()

        # ✅ Lọc trùng theo name (chỉ giữ 1 bản ghi cho mỗi tên bệnh)
        unique_diseases = {}
        for disease in diseases:
            if disease['name'] not in unique_diseases:
                unique_diseases[disease['name']] = disease

        print(f"Category requested: {category}")
        print(f"Diseases after filtering: {list(unique_diseases.values())}")

        return render_template('diagnosis.html',
                             diseases=list(unique_diseases.values()),
                             category=category,
                             username=session.get('username'))
    finally:
        conn.close()

@app.route('/search')
def search():
    query = request.args.get('query', '')
    search_type = request.args.get('type', 'products')
    if not query:
        return redirect(url_for('home'))
    
    conn = get_db_connection()
    if conn is None:
        return redirect(url_for('home'))
    try:
        with conn.cursor(dictionary=True) as c: 
            if search_type == 'diseases':
                c.execute('SELECT * FROM diseases WHERE name LIKE %s OR description LIKE %s OR symptoms LIKE %s', 
                         (f'%{query}%', f'%{query}%', f'%{query}%'))  
                results = c.fetchall()
                template = 'diagnosis.html'
                data = {'diseases': results, 'query': query}
            else:
                c.execute('SELECT * FROM products WHERE name LIKE %s OR description LIKE %s', 
                         (f'%{query}%', f'%{query}%'))  
                results = c.fetchall()
                template = 'admin_panel_html/search_results.html'
                data = {'products': results, 'query': query}
        
        data['username'] = session.get('username')
        return render_template(template, **data)
    finally:
        conn.close()

@app.route('/thuc-pham-chuc-nang')
def thuc_pham_chuc_nang():
    return redirect(url_for('products', category='thuc_pham_cn'))
@app.route('/duoc-my-pham')  
def duoc_my_pham():
    return redirect(url_for('products', category='duoc_my_pham'))
@app.route('/dung-cu-y-te')
def dung_cu_y_te():
    return redirect(url_for('products', category='dung_cu_yt'))
@app.route('/thuoc')
def thuoc():
    return redirect(url_for('products', category='thuoc'))
@app.route('/chan-doan-benh')
def chan_doan_benh_redirect():
    return redirect(url_for('diagnosis', category='all'))
@app.context_processor
def inject_user():
    return dict(username=session.get('username'), role=session.get('role'))

@app.context_processor
def inject_user_context():
    return dict(username=session.get('username'), role=session.get('role'))


@app.route('/gioithieu')
def gioithieu():
    return render_template('chinh_sach_html/gioithieu.html')
@app.route('/doingu')
def doingu():
    return render_template('chinh_sach_html/doingu.html')
@app.route('/baomat')
def baomat():
    return render_template('chinh_sach_html/baomat.html')
@app.route('/vanchuyen')
def vanchuyen():
    return render_template('chinh_sach_html/vanchuyen.html')
@app.route('/doitra')
def doitra():
    return render_template('chinh_sach_html/doitra.html')
@app.route('/brand/<brand_name>')
def brand_detail(brand_name):
    """Route để hiển thị trang chi tiết thương hiệu"""
    # Tạo tên file template
    template_name = f'brands_name/{brand_name}.html'
    
    # Flask sẽ tự động trả về 404 nếu template không tồn tại
    return render_template(template_name, brand_name=brand_name)

@app.route('/buy')
def buy():
    return render_template('buy.html')


if __name__ == '__main__':
    app.run(debug=True)