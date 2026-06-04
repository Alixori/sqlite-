from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)
DB_NAME = 'sales_db.sqlite'

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON;')
    return conn

@app.route('/')
def index():
    return redirect(url_for('sales_report'))

@app.route('/sales')
def sales_report():
    conn = get_db_connection()
    sales = conn.execute('''
        SELECT
            s.sale_id,
            c.first_name || ' ' || c.last_name AS client_name,
            p.product_name,
            s.quantity_sold,
            s.total_amount,
            s.sale_date
        FROM sales s
        JOIN clients c ON s.client_id = c.client_id
        JOIN products p ON s.product_id = p.product_id
        ORDER BY s.sale_date DESC
    ''').fetchall()
    conn.close()
    return render_template('sales.html', sales=sales)

@app.route('/products')
def products():
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products ORDER BY product_id').fetchall()
    conn.close()
    return render_template('products.html', products=products)

@app.route('/products/add', methods=['POST'])
def add_product():
    product_name = request.form['product_name']
    price = request.form['price']
    category = request.form['category']
    
    conn = get_db_connection()
    conn.execute('INSERT INTO products (product_name, price, category) VALUES (?, ?, ?)',
                 (product_name, float(price), category))
    product_id = conn.lastrowid
    conn.execute('INSERT INTO inventory (product_id, quantity_in_stock) VALUES (?, ?)',
                 (product_id, 0))
    conn.commit()
    conn.close()
    return redirect(url_for('products'))

@app.route('/products/update/<int:product_id>', methods=['POST'])
def update_product(product_id):
    product_name = request.form['product_name']
    price = request.form['price']
    category = request.form['category']
    
    conn = get_db_connection()
    conn.execute('UPDATE products SET product_name = ?, price = ?, category = ? WHERE product_id = ?',
                 (product_name, float(price), category, product_id))
    conn.commit()
    conn.close()
    return redirect(url_for('products'))

@app.route('/products/delete/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM products WHERE product_id = ?', (product_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('products'))

@app.route('/inventory')
def inventory():
    conn = get_db_connection()
    inventory = conn.execute('''
        SELECT i.inventory_id, i.product_id, p.product_name, p.price, i.quantity_in_stock, i.last_updated
        FROM inventory i
        JOIN products p ON i.product_id = p.product_id
        ORDER BY p.product_name
    ''').fetchall()
    conn.close()
    return render_template('inventory.html', inventory=inventory)

@app.route('/inventory/update/<int:inventory_id>', methods=['POST'])
def update_inventory(inventory_id):
    quantity = request.form['quantity_in_stock']
    
    conn = get_db_connection()
    conn.execute('UPDATE inventory SET quantity_in_stock = ?, last_updated = ? WHERE inventory_id = ?',
                 (int(quantity), datetime.now(), inventory_id))
    conn.commit()
    conn.close()
    return redirect(url_for('inventory'))

@app.route('/clients')
def clients():
    conn = get_db_connection()
    clients = conn.execute('SELECT * FROM clients ORDER BY client_id').fetchall()
    conn.close()
    return render_template('clients.html', clients=clients)

@app.route('/clients/add', methods=['POST'])
def add_client():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    phone = request.form['phone']
    
    conn = get_db_connection()
    try:
        conn.execute('INSERT INTO clients (first_name, last_name, email, phone) VALUES (?, ?, ?, ?)',
                     (first_name, last_name, email, phone))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return redirect(url_for('clients'))
    conn.close()
    return redirect(url_for('clients'))

@app.route('/clients/update/<int:client_id>', methods=['POST'])
def update_client(client_id):
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    phone = request.form['phone']
    
    conn = get_db_connection()
    try:
        conn.execute('UPDATE clients SET first_name = ?, last_name = ?, email = ?, phone = ? WHERE client_id = ?',
                     (first_name, last_name, email, phone, client_id))
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    conn.close()
    return redirect(url_for('clients'))

@app.route('/clients/delete/<int:client_id>', methods=['POST'])
def delete_client(client_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM clients WHERE client_id = ?', (client_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('clients'))

@app.route('/sales/add', methods=['POST'])
def add_sale():
    client_id = request.form['client_id']
    product_id = request.form['product_id']
    quantity_sold = request.form['quantity_sold']
    total_amount = request.form['total_amount']
    
    conn = get_db_connection()
    conn.execute('INSERT INTO sales (client_id, product_id, quantity_sold, total_amount) VALUES (?, ?, ?, ?)',
                 (int(client_id), int(product_id), int(quantity_sold), float(total_amount)))
    conn.commit()
    conn.close()
    return redirect(url_for('sales_report'))

@app.route('/sales/delete/<int:sale_id>', methods=['POST'])
def delete_sale(sale_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM sales WHERE sale_id = ?', (sale_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('sales_report'))

@app.route('/api/products')
def api_products():
    conn = get_db_connection()
    products = conn.execute('SELECT product_id, product_name, price FROM products').fetchall()
    conn.close()
    return jsonify([dict(p) for p in products])

@app.route('/api/clients')
def api_clients():
    conn = get_db_connection()
    clients = conn.execute('SELECT client_id, first_name, last_name FROM clients').fetchall()
    conn.close()
    return jsonify([{
        'client_id': c['client_id'],
        'name': f"{c['first_name']} {c['last_name']}"
    } for c in clients])

if __name__ == '__main__':
    app.run(debug=True, port=5000)
