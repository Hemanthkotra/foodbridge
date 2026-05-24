from flask import Flask, request, jsonify, session
from datetime import datetime
import sqlite3
import hashlib

app = Flask(__name__)
app.secret_key = 'foodbridge-secret-2024-xk92pL'
from flask import render_template, redirect, url_for

# --- Helper: connect to database ---
def get_db():
    conn = sqlite3.connect('foodwaste.db')
    conn.row_factory = sqlite3.Row  # lets us access columns by name
    return conn

# --- Helper: hash passwords (never store plain text!) ---
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# ============================================================
# ROUTE 1: Register a restaurant or orphanage
# ============================================================
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    required = ['name', 'email', 'password', 'role']
    for field in required:
        if not data.get(field):
            return jsonify({'error': f'{field} is required'}), 400

    if data['role'] not in ('restaurant', 'orphanage'):
        return jsonify({'error': 'role must be restaurant or orphanage'}), 400

    db = get_db()
    try:
        db.execute('''
            INSERT INTO users (name, email, password, role, address, phone)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            data['name'],
            data['email'],
            hash_password(data['password']),
            data['role'],
            data.get('address', ''),
            data.get('phone', '')
        ))
        db.commit()
        return jsonify({'message': 'Registration successful!'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Email already registered'}), 409
    finally:
        db.close()


# ============================================================
# ROUTE 2: Log in
# ============================================================
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    db = get_db()

    user = db.execute('''
        SELECT * FROM users
        WHERE email = ? AND password = ?
    ''', (data['email'], hash_password(data['password']))).fetchone()
    db.close()

    if not user:
        return jsonify({'error': 'Invalid email or password'}), 401

    session['user_id'] = user['id']
    session['role']    = user['role']
    session['name']    = user['name']

    return jsonify({
        'message': f"Welcome, {user['name']}!",
        'role': user['role']
    })


# ============================================================
# ROUTE 3: Restaurant posts a food listing
# ============================================================
@app.route('/food/add', methods=['POST'])
def add_food():
    if session.get('role') != 'restaurant':
        return jsonify({'error': 'Only restaurants can post food'}), 403

    data = request.get_json()

    required = ['item_name', 'quantity', 'expiry_time']
    for field in required:
        if not data.get(field):
            return jsonify({'error': f'{field} is required'}), 400

    db = get_db()
    db.execute('''
        INSERT INTO food_listings (restaurant_id, item_name, quantity, expiry_time, notes)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        session['user_id'],
        data['item_name'],
        data['quantity'],
        data['expiry_time'],
        data.get('notes', '')
    ))
    db.commit()
    db.close()

    return jsonify({'message': 'Food listing added successfully!'}), 201


# ============================================================
# ROUTE 4: Orphanage views all available food
# ============================================================
@app.route('/food/available', methods=['GET'])
def available_food():
    if session.get('role') != 'orphanage':
        return jsonify({'error': 'Only orphanages can view available food'}), 403

    db = get_db()
    listings = db.execute('''
        SELECT
            fl.id,
            fl.item_name,
            fl.quantity,
            fl.expiry_time,
            fl.notes,
            u.name    AS restaurant_name,
            u.address AS restaurant_address,
            u.phone   AS restaurant_phone
        FROM food_listings fl
        JOIN users u ON fl.restaurant_id = u.id
        WHERE fl.status = 'available'
        ORDER BY fl.expiry_time ASC
    ''').fetchall()
    db.close()

    return jsonify([dict(row) for row in listings])


# ============================================================
# ROUTE 5: Orphanage claims a food listing
# ============================================================
@app.route('/food/claim/<int:food_id>', methods=['POST'])
def claim_food(food_id):
    if session.get('role') != 'orphanage':
        return jsonify({'error': 'Only orphanages can claim food'}), 403

    db = get_db()

    # Check the listing exists and is still available
    listing = db.execute('''
        SELECT * FROM food_listings WHERE id = ? AND status = 'available'
    ''', (food_id,)).fetchone()

    if not listing:
        return jsonify({'error': 'Food listing not found or already claimed'}), 404

    # Record the claim
    db.execute('''
        INSERT INTO claims (food_id, orphanage_id)
        VALUES (?, ?)
    ''', (food_id, session['user_id']))

    # Mark the listing as claimed so no one else can take it
    db.execute('''
        UPDATE food_listings SET status = 'claimed' WHERE id = ?
    ''', (food_id,))

    db.commit()
    db.close()

    return jsonify({'message': 'Food claimed successfully! Contact the restaurant to arrange pickup.'})


# ============================================================
# ROUTE 6: Log out
# ============================================================
@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Logged out successfully'})




@app.route('/')
def home():
    return render_template('home.html')

@app.route('/dashboard/restaurant')
def restaurant_dashboard():
    if session.get('role') != 'restaurant':
        return redirect(url_for('login_page'))
    return render_template('dashboard_restaurant.html', name=session.get('name'))

@app.route('/dashboard/orphanage')
def orphanage_dashboard():
    if session.get('role') != 'orphanage':
        return redirect(url_for('login_page'))
    db = get_db()
    listings = db.execute('''
        SELECT fl.id, fl.item_name, fl.quantity, fl.expiry_time, fl.notes,
               u.name AS restaurant_name, u.address AS restaurant_address, u.phone AS restaurant_phone
        FROM food_listings fl
        JOIN users u ON fl.restaurant_id = u.id
        WHERE fl.status = 'available'
        ORDER BY fl.expiry_time ASC
    ''').fetchall()
    db.close()
    return render_template('dashboard_orphanage.html',
                           name=session.get('name'),
                           listings=[dict(r) for r in listings])

@app.route('/login-page')
def login_page():
    return render_template('login.html')

@app.route('/register-page')
def register_page():
    return render_template('register.html')  

# --- Run the app ---
if __name__ == '__main__':
    app.run(debug=False)  