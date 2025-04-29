from app import app
from flask import render_template, redirect, url_for, request

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/extract', methods=['post'])
def extract_data():
    product_id = request.form.get('product_id')
    return redirect(url_for('product', product_id=product_id))


@app.route('/extract', methods=['get'])
def extract():
    return render_template("extract.html")

@app.route('/products')
def products():
    return render_template("products.html")

@app.route('/author')
def author():
    return render_template("author.html")

@app.route('/products/<int:product_id>')
def product(product_id:int):
    return render_template("product.html", product_id=product_id)

@app.route('/')
def base():
    return render_template("base.html")