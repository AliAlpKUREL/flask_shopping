from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)


# Utility function to handle database connections
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row  # This allows us to work with dictionaries instead of tuples
    return conn


@app.route('/')
def home():
    conn = get_db_connection()

    # Get categories and count products in each category
    categories = conn.execute('SELECT category, COUNT(*) as count FROM products GROUP BY category').fetchall()

    # Pagination implementation
    page = request.args.get('page', 1, type=int)  # Default to page 1
    per_page = 10  # Number of products per page
    offset = (page - 1) * per_page  # Calculate the offset for the query

    # Get products for the current page
    products = conn.execute('SELECT * FROM products LIMIT ? OFFSET ?', (per_page, offset)).fetchall()

    conn.close()

    # Pass page, categories, and products to the template
    return render_template('home.html', categories=categories, products=products, page=page)


@app.route('/category/<category_name>')
def category_products(category_name):
    conn = get_db_connection()

    # Fetch products for the selected category
    products = conn.execute('SELECT * FROM products WHERE category = ?', (category_name,)).fetchall()

    # Get categories and count products in each category
    categories = conn.execute('SELECT category, COUNT(*) as count FROM products GROUP BY category').fetchall()

    conn.close()

    return render_template('home.html', categories=categories, products=products)


@app.route('/search')
def search():
    query = request.args.get('q', '')
    conn = get_db_connection()

    if query:
        # Search for products matching the query in name or description
        products = conn.execute("SELECT * FROM products WHERE name LIKE ? OR description LIKE ?",
                                (f'%{query}%', f'%{query}%')).fetchall()
    else:
        # If no query is provided, show an empty result or a message
        products = []

    conn.close()

    return render_template('search.html', products=products, query=query)


@app.route('/product/<int:product_id>')
def product_detail(product_id):
    conn = get_db_connection()

    # Fetch the product details for the given product_id
    product = conn.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()

    conn.close()

    if product is None:
        # Handle case where the product is not found
        return render_template('404.html'), 404

    return render_template('product_detail.html', product=product)


if __name__ == '__main__':
    app.run(debug=True)
