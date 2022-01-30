from multiprocessing.sharedctypes import Value
from flask import render_template, request, redirect, url_for, session, Blueprint, flash
import shelve
import os
from tit.admin.rewards.Forms import editVouchersForm, addVouchersForm
import tit.classes.reward as reward
from werkzeug.utils import secure_filename
from tit import app

rewards = Blueprint('rewards', __name__, template_folder='templates', static_url_path='static', url_prefix='/rewards')

@rewards.route('/add', methods=['GET', 'POST'])
def addVouchers_admin():
    addVouchers_admin_form = addVouchersForm()
    print(addVouchers_admin_form.validate_on_submit())
    if request.method == 'POST' :
        with shelve.open('tit/database/vouchers.db', 'c') as db:
            print("hello")
            vouchers_dict = {}

            try:
                vouchers_dict = db['Vouchers']
            except:
                print("Error in retrieving Voucher from vouchers.db.")

            filename = addVouchers_admin_form.vcode.data + "." + addVouchers_admin_form.file.data.filename.split(".")[-1]
            addVouchers_admin_form.file.data.save(app.config['STATIC_PATH']+'reward_uploads/' + filename)

            code = addVouchers_admin_form.vcode.data
            for voucher in vouchers_dict.values():
                if code == voucher.get_discount_code():
                    print("Error!!!!!!!!!!!!!!!!!!!")
                    session['voucher_unaccepted'] = voucher.get_name() + ', ' + voucher.get_discount_code()
                    return redirect(url_for('admin.rewards.addVouchers_admin'))
            voucher = reward.Voucher(addVouchers_admin_form.vname.data, 
                                    addVouchers_admin_form.vdescription.data,
                                    addVouchers_admin_form.vcode.data, 
                                    addVouchers_admin_form.spools_needed.data,
                                    addVouchers_admin_form.vamount.data, 
                                    addVouchers_admin_form.vexpirydate.data,
                                    addVouchers_admin_form.vquantity.data,
                                    filename)

            if len(vouchers_dict) > 0:
                voucher.set_voucher_id(list(vouchers_dict)[-1]+1)
                vouchers_dict[voucher.get_voucher_id()] = voucher
                db['Vouchers'] = vouchers_dict


            vouchers_dict[voucher.get_voucher_id()] = voucher
            db['Vouchers'] = vouchers_dict

            # Test codes
            vouchers_dict = db['Vouchers']
            voucher = vouchers_dict[voucher.get_voucher_id()]
            print(voucher.get_name(), voucher.get_discount_code(), "was stored in vouchers.db successfully with voucher_id ==", voucher.get_voucher_id())

            db.close()

            session['voucher_created'] = voucher.get_name() + ', ' + voucher.get_discount_code()
            flash('You have been logged in', 'success')

            return redirect(url_for('admin.rewards.viewVouchers_admin'))
    return render_template('rewards/addVouchers_admin.html', form=addVouchers_admin_form)



@rewards.route('/view', methods=['GET', 'POST'])
def viewVouchers_admin():
    vouchers_dict = {}

    try:
        db = shelve.open('tit/database/vouchers.db', 'r')
        vouchers_dict = db['Vouchers']
        db.close()
    except:
        print("Error in retrieving Vouchers from vouchers.db.")

    vouchers_list = []
    for key in vouchers_dict:
        voucher = vouchers_dict.get(key)
        vouchers_list.append(voucher)

    return render_template('rewards/viewVouchers_admin.html', count=len(vouchers_list), vouchers_list=vouchers_list)



@rewards.route('/edit/<int:id>/', methods=['GET', 'POST'])
def editVouchers_admin(id):
    editVouchers_admin_form = editVouchersForm()
    print(editVouchers_admin_form.validate_on_submit())
    if request.method == 'POST' and editVouchers_admin_form.validate():
        with shelve.open('tit/database/vouchers.db', 'w') as db:
            print("hello")
            vouchers_dict = {}

            try:
                vouchers_dict = db['Vouchers']
            except:
                print("Error in retrieving Voucher from vouchers.db.")

            filename = editVouchers_admin_form.vcode.data + "." + editVouchers_admin_form.file.data.filename.split(".")[-1]
            editVouchers_admin_form.file.data.save(app.config['STATIC_PATH']+'reward_uploads/' + filename)

            voucher = vouchers_dict.get(id)
            voucher.set_name(editVouchers_admin_form.vname.data)
            voucher.set_description(editVouchers_admin_form.vdescription.data)
            voucher.set_discount_code(editVouchers_admin_form.vcode.data)
            voucher.set_spools(editVouchers_admin_form.spools_needed.data)
            voucher.set_discount_amount(editVouchers_admin_form.vamount.data)
            voucher.set_expiry_date(editVouchers_admin_form.vexpirydate.data)
            voucher.set_quantity(editVouchers_admin_form.vquantity.data)
            voucher.set_filename(filename)
            
            db['Vouchers'] = vouchers_dict
            db.close()

            session['voucher_updated'] = voucher.get_name() + ', ' + voucher.get_discount_code()
            
            return redirect(url_for('admin.rewards.viewVouchers_admin'))

    else:
        vouchers_dict = {}
        db = shelve.open('tit/database/vouchers.db', 'r')

        try:
            vouchers_dict = db['Vouchers']
        except:
            print("Error in retrieving Voucher from vouchers.db.")

        voucher = vouchers_dict.get(id)
        editVouchers_admin_form.vname.data = voucher.get_name()
        editVouchers_admin_form.vdescription.data = voucher.get_description()
        editVouchers_admin_form.vcode.data = voucher.get_discount_code()
        editVouchers_admin_form.spools_needed.data = voucher.get_spools()
        editVouchers_admin_form.vamount.data = voucher.get_discount_amount()
        editVouchers_admin_form.vexpirydate.data = voucher.get_expiry_date()
        editVouchers_admin_form.vquantity.data = voucher.get_quantity()
        editVouchers_admin_form.file.data = voucher.get_filename()

        db.close()

        return render_template('rewards/editVouchers_admin.html', form=editVouchers_admin_form , filename=voucher.get_filename())





@rewards.route('/delete/<int:id>', methods=['POST']) 
def delete_voucher(id):
    vouchers_dict = {}
    db = shelve.open('tit/database/vouchers.db', 'w')

    try:
        vouchers_dict = db['Vouchers']
    except:
        print("Error in retrieving Voucher from vouchers.db.")

    voucher = vouchers_dict.get(id)

    vouchers_dict.pop(id)
    os.remove(app.config['STATIC_PATH']+"reward_uploads/" + voucher.get_filename())


    db['Vouchers'] = vouchers_dict

    db.close()

    session['voucher_deleted'] = voucher.get_name() + ', ' + voucher.get_discount_code()

    return redirect(url_for('admin.rewards.viewVouchers_admin'))
