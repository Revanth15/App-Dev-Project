# from flask import render_template, request, redirect, url_for, session, jsonify
# import email_validator
# import shelve
# import os
# from tit.main.rewards.Forms import editVouchersForm, addVouchersForm, UserSignUpForm
# import user, reward
# from werkzeug.utils import secure_filename




# @app.route('/myVouchers')
# def myVouchers():
#     '''
#     users_dict = {}
#     db = shelve.open('storage.db', 'r')

#     try:
#         user_dict = db['Users']
#     except:
#         print("Error in retrieving Users from storage.db.")

#     db.close()
#     user_list = []
#     for key in user_dict:
#         user = user_dict.get(key)
#         user_list.append(user)

#     return render_template('myVouchers.html', count=len(user_list), vouchers_list=user_list)
#     '''

#     vouchers_dict = {}
#     db = shelve.open('vouchers.db', 'r')

#     try:
#         vouchers_dict = db['Vouchers']
#     except:
#         print("Error in retrieving Vouchers from vouchers.db.")

#     db.close()
#     vouchers_list = []
#     for key in vouchers_dict:
#         voucher = vouchers_dict.get(key)
#         vouchers_list.append(voucher)
#     return render_template('myVouchers.html', count=len(vouchers_list), vouchers_list=vouchers_list)

