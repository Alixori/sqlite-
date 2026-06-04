import sqlite3
from pathlib import Path

DB_NAME = 'sales_db.sqlite'
SQL_FILE = 'SQLite(1).sql'

conn = sqlite3.connect(DB_NAME)
conn.execute('PRAGMA foreign_keys = ON;')
sql = Path(SQL_FILE).read_text(encoding='utf-8')
conn.executescript(sql)
print('DB_CREATED')
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
''').fetchall()
print('QUERY_ROWS', len(rows))
for row in rows:
    print(row)
conn.close()
