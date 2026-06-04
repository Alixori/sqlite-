# Sales Management System - Web UI

A modern, user-friendly web interface for managing your sales database with Flask and SQLite.

## Features

✨ **Complete CRUD Operations** for all tables:
- 📦 **Products** - Add, edit, and delete products with pricing and categories
- 👥 **Clients** - Manage client information and contact details
- 📊 **Sales** - Record and track sales transactions
- 📈 **Inventory** - Monitor and update product stock levels

✨ **Modern Web Interface**:
- Responsive design that works on desktop and mobile
- Beautiful gradient UI with smooth animations
- Modal dialogs for adding and editing records
- Real-time total calculation for sales

## Installation

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

Or install Flask directly:

```bash
pip install Flask
```

### 2. Initialize the Database (Optional)

If you need to create a fresh database with sample data:

```bash
python run_sql.py
```

This will create `sales_db.sqlite` with the predefined schema and sample data.

## Running the Application

Start the Flask web server:

```bash
python app.py
```

The application will be available at: **http://localhost:5000**

## Usage Guide

### Navigation

The main navigation bar at the top provides access to all sections:
- **Sales Report** - View all sales and record new transactions
- **Products** - Manage your product catalog
- **Inventory** - Track stock levels
- **Clients** - Manage customer information

### Managing Products

1. Click "📦 Products" in the navigation
2. Click "+ Add New Product" to create a new product
3. Fill in:
   - Product Name
   - Price
   - Category
4. Click "Add Product" to save
5. To edit: Click the "Edit" button next to a product
6. To delete: Click the "Delete" button (confirmation required)

### Managing Clients

1. Click "👥 Clients" in the navigation
2. Click "+ Add New Client" to create a new client
3. Fill in:
   - First Name
   - Last Name
   - Email (optional)
   - Phone (optional)
4. Click "Add Client" to save
5. Edit and delete options work similarly to Products

### Managing Inventory

1. Click "📈 Inventory" in the navigation
2. View all products and their current stock levels
3. Click "Update Stock" next to any product
4. Enter the new quantity and click "Update Inventory"

### Recording Sales

1. Click "📊 Sales Report" in the navigation
2. Click "+ Record New Sale"
3. Select:
   - **Client** - from the dropdown list
   - **Product** - from the dropdown list (shows price)
   - **Quantity** - how many units sold
   - **Total Amount** - automatically calculated (Quantity × Price)
4. Click "Record Sale" to save
5. To delete a sale: Click the "Delete" button (confirmation required)

## Database Schema

### Products Table
```
- product_id (INTEGER, PRIMARY KEY)
- product_name (TEXT)
- price (REAL)
- category (TEXT)
```

### Inventory Table
```
- inventory_id (INTEGER, PRIMARY KEY)
- product_id (INTEGER, FOREIGN KEY)
- quantity_in_stock (INTEGER)
- last_updated (DATETIME)
```

### Clients Table
```
- client_id (INTEGER, PRIMARY KEY)
- first_name (TEXT)
- last_name (TEXT)
- email (TEXT, UNIQUE)
- phone (TEXT)
```

### Sales Table
```
- sale_id (INTEGER, PRIMARY KEY)
- client_id (INTEGER, FOREIGN KEY)
- product_id (INTEGER, FOREIGN KEY)
- quantity_sold (INTEGER)
- sale_date (DATETIME)
- total_amount (REAL)
```

## API Endpoints

The application also provides JSON API endpoints for integration:

- `GET /api/products` - Get all products as JSON
- `GET /api/clients` - Get all clients as JSON

## Troubleshooting

### Port 5000 Already in Use

If you see "Address already in use" error, Flask is already running. Either:
1. Stop the existing Flask process
2. Change the port in `app.py`: `app.run(debug=True, port=5001)`

### Database Locked Error

This usually means multiple instances are accessing the database. Ensure only one Flask instance is running.

### Cannot Find Module 'flask'

Make sure you've installed Flask:
```bash
pip install Flask
```

## Tips for Best Use

1. **Regular Backups** - The SQLite database file `sales_db.sqlite` is your data. Keep regular backups.
2. **Email Uniqueness** - Emails must be unique per client to prevent duplicates.
3. **Stock Management** - Keep the inventory updated when recording sales to maintain accurate stock levels.
4. **Delete Carefully** - Deleted records cannot be recovered. Confirm deletions carefully.

## Files Structure

```
.
├── app.py                      # Flask application
├── run_sql.py                  # Database initialization script
├── query_viewer.py             # Legacy query viewer
├── sales_db.sqlite             # SQLite database
├── requirements.txt            # Python dependencies
├── sqliteinventory.sql         # Database schema
└── templates/
    ├── base.html               # Base template with styling
    ├── sales.html              # Sales report page
    ├── products.html           # Products management page
    ├── clients.html            # Clients management page
    └── inventory.html          # Inventory management page
```

## Future Enhancements

Possible improvements:
- User authentication and authorization
- Advanced reporting and analytics
- CSV export functionality
- Product images
- Sales filtering by date range
- Email notifications for low inventory

## License

This project is part of your personal sales management system.

---

**Enjoy managing your sales! 🚀**
