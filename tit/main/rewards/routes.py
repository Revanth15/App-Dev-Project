from flask import render_template, Blueprint
import shelve

from tit.utils import get_db

rewards = Blueprint('rewards', __name__, template_folder='templates', static_url_path='static', url_prefix='/rewards')

@rewards.route('/discover')
def discover():
    vouchers_dict = get_db('vouchers','Vouchers')
    vouchers_list = []
    for key in vouchers_dict:
        voucher = vouchers_dict.get(key)
        if voucher.get_quantity() != 0:
            vouchers_list.append(voucher)

    return render_template('rewards/discover.html', count=len(vouchers_list), vouchers_list=vouchers_list)

@rewards.route('/discover/<int:id>')
def customer_spools(id):
    customer_dict = get_db('storage','Customers')
    customer = customer_dict.get(id)
    spools = customer.get_spools()

    # vouchers_dict = {}
    # db = shelve.open('vouchers.db', 'r')

    # try:
    #     vouchers_dict = db['Vouchers']
    # except:
    #     print("Error in retrieving Vouchers from vouchers.db.")

    # db.close()
    # vouchers_list = []
    # for key in vouchers_dict:
    #     voucher = vouchers_dict.get(key)
    #     vouchers_list.append(voucher)

    # return render_template('discover.html', count=len(vouchers_list), vouchers_list=vouchers_list, spools=spools)
    return render_template('rewards/discover.html', spools=spools)



