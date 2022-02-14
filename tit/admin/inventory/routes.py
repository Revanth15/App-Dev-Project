from re import S
from flask import render_template, request, redirect, url_for, Blueprint
from tit.admin.inventory.forms import CreateProductForm, RestockForm, ImportForm
from tit.utils import set_notifications
import datetime
import os
import shelve
import tit.classes.product as Product
import tit.classes.delivery as Delivery
from tit.utils import get_db, set_db
from tit import app 

inventory = Blueprint('inventory', __name__, template_folder='templates', static_url_path='static', url_prefix='/inventory')

@inventory.route('/add_product', methods=['GET', 'POST'])
def add_product():
    create_product_form = CreateProductForm()
    if request.method == 'POST' and create_product_form.validate_on_submit():
        products_dict = get_db('products', 'products')

        filename = create_product_form.sku.data + "." + create_product_form.file.data.filename.split(".")[-1]
        create_product_form.file.data.save(app.config['STATIC_PATH']+ 'product_uploads/' + filename)

        product = Product.Product(
            product_name = create_product_form.product_name.data, 
            sku = create_product_form.sku.data, 
            product_price = create_product_form.product_price.data, 
            quantity = create_product_form.quantity.data, 
            product_description = create_product_form.product_description.data, 
            filename = filename,
            category = create_product_form.category.data
            ) 

        products_dict[product.get_sku()]= product
        set_db('products', 'products', products_dict)

        products_list = []
        for key in products_dict:
            product = products_dict.get(key)
            products_list.append(product)
            
        return redirect(url_for('admin.inventory.add_product',  products_list = products_list))  
    return render_template('inventory/add_product.html', form=create_product_form)


@inventory.route('/retrieve_product')
def retrieve_products():
    products_dict = get_db('products', 'products')

    products_list = []
    for key in products_dict:
        product = products_dict.get(key)
        products_list.append(product)

    return render_template('inventory/retrieve_product.html', count=len(products_list), products_list=products_list)


@inventory.route('/restock_product', methods=['GET', 'POST'])
def restock_product():
    restock_form = RestockForm(request.form)     
    products_dict = get_db('products', 'products')

    for key in products_dict:
        product = products_dict.get(key)
        sku = product.get_sku()
        restock_form.sku_select.choices += [(sku)]
        
    if request.method == 'POST' and restock_form.validate_on_submit():
        products_dict = get_db('products', 'products')
        delivery_dict = get_db('products', 'delivery')

        sku = restock_form.sku_select.data

        associated_product = products_dict.get(sku)
        delivery = Delivery.Delivery(
            sku = sku,
            restock_quantity = restock_form.restock_quantity.data,
            delivery_date = restock_form.delivery_date.data,
            restock_price= associated_product.get_product_price() * 0.7)

        
        restock_quantity = restock_form.restock_quantity.data 
        quantity = associated_product.get_quantity()
        updated_quantity = restock_quantity + quantity

        associated_product.set_quantity(updated_quantity)

        # delivery.set_delivery_date(restock_form.delivery_date.data)

        products_dict[sku] = associated_product
        delivery_dict[sku] = delivery

        set_db('products', 'products', products_dict)
        set_db('products', 'delivery', delivery_dict)
        
        return redirect(url_for('admin.inventory.retrieve_products'))
    else:
        return render_template('inventory/restock_product.html', form = restock_form)


@inventory.route('/edit_product/<sku>/', methods=['GET', 'POST'])
def edit_product(sku):
    update_product_form = CreateProductForm()
    if request.method == 'POST' and update_product_form.validate():
        products_dict = get_db('products', 'products')

        product = products_dict.get(sku)
        product.set_product_name(update_product_form.product_name.data)
        product.set_sku(update_product_form.sku.data)
        product.set_product_price(update_product_form.product_price.data)
        product.set_quantity(update_product_form.quantity.data)
        product.set_product_description(update_product_form.product_description.data)
        product.set_category(update_product_form.category.data)

        if update_product_form.file.data:
            filename = update_product_form.sku.data + "." + update_product_form.file.data.filename.split(".")[-1]
            os.remove(app.config['STATIC_PATH']+ 'product_uploads/' + product.get_filename())
            product.set_filename(filename)
            update_product_form.file.data.save(app.config['STATIC_PATH']+ 'product_uploads/' + filename)

        set_db('products', 'products', products_dict)

        for sku in products_dict:
            if products_dict[sku].get_quantity() < 30:
                if products_dict[sku].get_quantity() == 0:
                    set_notifications(f'{sku} is out of stock', 'OutOfStock', 'Click here to go to restock', 'inventory.retrieve_products')
                set_notifications(f'{sku} is low in stock', 'LowStock', 'Click here to go to restock', 'inventory.retrieve_products' )

        return redirect(url_for('admin.inventory.retrieve_products'))
    else:
        products_dict = get_db('products', 'products')

        product = products_dict.get(sku)
        update_product_form.product_name.data = product.get_product_name()
        update_product_form.sku.data = product.get_sku()
        update_product_form.product_price.data = product.get_product_price()
        update_product_form.quantity.data = product.get_quantity()
        update_product_form.product_description.data = product.get_product_description()
        update_product_form.category.data = product.get_category()

        return render_template('inventory/edit_product.html', form=update_product_form, filename=product.get_filename())


@inventory.route('/delete_product/<sku>', methods=['POST'])
def delete_product(sku):
    products_dict = get_db('products', 'products')
    product = products_dict.get(sku)

    products_dict.pop(sku)
    os.remove(app.config['STATIC_PATH']+ 'product_uploads/' + product.get_filename())

    set_db('products', 'products', products_dict)

    return redirect(url_for('admin.inventory.retrieve_products'))


@inventory.route('/import_xlsx')
def import_xlsx():
    form = ImportForm()
    print("hello")
    if request.method == 'POST' and form.validate_on_submit():
        print("hell2o")
        filename = form.xlsx.data.filename
        form.xlsx.data.save(app.config['STATIC_PATH']+ 'xlsx/' + filename)
        return redirect(url_for('admin.inventory.retrieve_products'))
    return render_template('inventory/import_xlsx.html', form= form)