import sqlite3
from pathlib import Path

DB_NAME = 'sales_db.sqlite'


def fetch_sales_report():
    conn = sqlite3.connect(DB_NAME)
    conn.execute('PRAGMA foreign_keys = ON;')
    rows = conn.execute('''
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
        ORDER BY s.sale_id
    ''').fetchall()
    conn.close()
    return rows


if __name__ == '__main__':
    print('Sales Report')
    print('------------')
    rows = fetch_sales_report()
    if not rows:
        print('No rows found.')
    else:
        for row in rows:
            print(row)
