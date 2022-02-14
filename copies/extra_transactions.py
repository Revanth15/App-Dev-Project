# @app.route('/delivery/<cust_id>/', method=['GET', 'POST'])
# def delivery(cust_id):
#     delivery_form = Delivery()
#     if request.method == 'POST' and delivery_form.validate():
#         with shelve.open('delivery.db', 'w') as delivery_db:
#             delivery_dict = {}
#             delivery_dict = delivery_db['delivery']

#             delivery = delivery_dict.get(cust_id)
#             product.set_first_name(delivery_form.first_name.data)
#             product.set_last_name(delivery_form.last_name.data)
#             product.set_address(delivery_form.address.data)
#             product.set_unit_number(delivery_form.unit_number.data)
#             product.set_postal_code(delivery_form.postal_code.data)
#             product.set_email(delivery_form.email.data)
#             product.set_phone_number(delivery_form.phone_number.data)

#             delivery_db['delivery'] = delivery_dict

#             return redirect(url_for('payment'))
#     else:
#         with shelve.open('delivery.db', 'r') as delivery_db:
#             delivery_dict = {}
#             delivery_db = shelve.open('delivery.db', 'r')
#             delivery_dict = delivery_db['delivery']

#             delivery = delivery_dict.get(cust_id)
#             delivery_form.first_name.data = delivery.get_first_name()
#             delivery_form.last_name.data = delivery.get_last_name()
#             delivery_form.address.data = delivery.get_address()
#             delivery_form.unit_number.data = delivery.get_unit_number()
#             delivery_form.postal_code.data = delivery.get_postal_code()
#             delivery_form.email.data = delivery.get_email()
#             delivery_form.phone_number.data = delivery.get_phone_number()
#         return render_template('delivery.html', form=delivery_form)
