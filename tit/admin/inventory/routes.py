from flask import render_template, request, redirect, url_for, Blueprint
from tit.admin.inventory.forms import CreateProductForm, RestockForm, ImportForm, PaymentForm, Delivery
import datetime
import os
import shelve
import tit.classes.product as Product
import tit.classes.delivery as Delivery
from tit import app 

inventory = Blueprint('inventory', __name__, template_folder='templates', static_url_path='static', url_prefix='/inventory')

@inventory.route('/add_product', methods=['GET', 'POST'])
def add_product():
    create_product_form = CreateProductForm()
    if request.method == 'POST' and create_product_form.validate_on_submit():
        with shelve.open('products.db', 'c') as products_db:
            products_dict = {}

            try:
                products_dict = products_db['products']
            except:
                print("Error in retrieving Products from products.db")

            filename = create_product_form.sku.data + "." + create_product_form.file.data.filename.split(".")[-1]
            create_product_form.file.data.save('tit/static/uploads/' + filename)

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
            products_db['products'] = products_dict

            products_list = []
            for key in products_dict:
                product = products_dict.get(key)
                products_list.append(product)
                
            

            return redirect(url_for('admin.inventory.add_product',  products_list = products_list))  
    return render_template('add_product.html', form=create_product_form)


@inventory.route('/retrieve_product')
def retrieve_products():
    products_dict = {}
    try:
        products_db = shelve.open('products.db', 'r')
        products_dict = products_db['products']
        products_db.close()
    except:
        print("Error in retrieving Product from products.db.")

    products_list = []
    for key in products_dict:
        product = products_dict.get(key)
        products_list.append(product)

    return render_template('retrieve_product.html', count=len(products_list), products_list=products_list)


@inventory.route('/restock_product', methods=['GET', 'POST'])
def restock_product():
    restock_form = RestockForm(request.form)     
    with shelve.open('products.db', 'w') as products_db:
        products_dict = {}
        products_dict = products_db['products']

        for key in products_dict:
            product = products_dict.get(key)
            sku = product.get_sku()
            restock_form.sku_select.choices += [(sku)]
    if request.method == 'POST' and restock_form.validate_on_submit():
        with shelve.open('products.db', 'w') as products_db:
            products_dict = {}
            delivery_dict = {}
            try:
                delivery_dict = products_db["delivery"]
            except:
                pass
            try:
                products_dict = products_db['products']
            except:
                pass

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

            products_db['products'] = products_dict
            products_db['delivery'] = delivery_dict

            
            return redirect(url_for('admin.inventory.retrieve_products'))
    else:
        return render_template('restock_product.html', form = restock_form)


@inventory.route('/edit_product/<sku>/', methods=['GET', 'POST'])
def edit_product(sku):
    update_product_form = CreateProductForm()
    if request.method == 'POST' and update_product_form.validate():
        with shelve.open('products.db', 'w') as products_db:
            products_dict = {}
            products_dict = products_db['products']

            product = products_dict.get(sku)
            product.set_product_name(update_product_form.product_name.data)
            product.set_sku(update_product_form.sku.data)
            product.set_product_price(update_product_form.product_price.data)
            product.set_quantity(update_product_form.quantity.data)
            product.set_product_description(update_product_form.product_description.data)
            product.set_category(update_product_form.category.data)

            if update_product_form.file.data:
                filename = update_product_form.sku.data + "." + update_product_form.file.data.filename.split(".")[-1]
                os.remove('tit/static/uploads/' + product.get_filename())
                product.set_filename(filename)
                update_product_form.file.data.save('tit/static/uploads/' + filename)

            products_db['products'] = products_dict

            return redirect(url_for('admin.inventory.retrieve_products'))
    else:
        with shelve.open('products.db', 'r') as products_db:
            products_dict = {}
            products_db = shelve.open('products.db', 'r')
            products_dict = products_db['products']

            product = products_dict.get(sku)
            update_product_form.product_name.data = product.get_product_name()
            update_product_form.sku.data = product.get_sku()
            update_product_form.product_price.data = product.get_product_price()
            update_product_form.quantity.data = product.get_quantity()
            update_product_form.product_description.data = product.get_product_description()
            update_product_form.category.data = product.get_category()

            return render_template('edit_product.html', form=update_product_form, filename=product.get_filename())


@inventory.route('/delete_product/<sku>', methods=['POST'])
def delete_product(sku):
    products_dict = {}
    products_db = shelve.open('products.db', 'w')
    products_dict = products_db['products']
    product = products_dict.get(sku)

    products_dict.pop(sku)
    os.remove('tit/static/uploads/' + product.get_filename())

    products_db['products'] = products_dict
    products_db.close()

    return redirect(url_for('admin.inventory.retrieve_products'))


@inventory.route('/import_xlsx')
def import_xlsx():
    form = ImportForm()
    print("hello")
    if request.method == 'POST' and form.validate_on_submit():
        print("hell2o")
        filename = form.xlsx.data.filename
        form.xlsx.data.save('static/xlsx/' + filename)
        return redirect(url_for('admin.inventory.retrieve_products'))
    return render_template('import_xlsx.html', form= form)