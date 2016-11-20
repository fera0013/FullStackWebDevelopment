"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template,url_for, request,redirect,flash,jsonify
from catalog import app
import model

db = model.CatalogItemModel()
db.initialize()

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    categories=db.get_categories()
    latest_items=db.get_latest_items(2)
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
        categories=categories,
        latest_items=latest_items
    )

@app.route('/catalog/<string:category_name>/items', methods=['GET', 'POST'])
def Catalog(category_name):
    categories=db.get_categories()
    items=db.get_items_of_category(category_name)
    return render_template('catalog.html',categories=categories, items=items)

@app.route('/catalog/<string:category_name>/<string:item_title>', methods=['GET', 'POST'])
def Item(item_title):
    item=db.get_item(item_title)
    return render_template('item.html', item=item)
