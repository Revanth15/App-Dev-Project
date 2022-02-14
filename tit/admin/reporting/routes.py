from flask import render_template, request, redirect, url_for, session, send_file, Blueprint, g

from tit.classes.Archive import Archive
from tit.admin.reporting.Forms import CreateReportForm, UpdateReportForm
from tit.admin.reporting.utils import createExcel, createPDF, db_count_occurence, db_get_qty, get_ext, createCSV
from tit.utils import dbkeys, get_db, set_db
from tit import app

import shelve
import json
import datetime
import os

reporting = Blueprint('reporting', __name__,template_folder='templates', static_url_path='static', url_prefix='/reports')

@reporting.route('/', methods=['GET', 'POST'])
def reports():
    tab = request.args.get('tab')
    if tab is None:
        tab = 'inventory'

    createReportForm = CreateReportForm()
    if createReportForm.validate_on_submit():
        archive_dict = get_db('archive', 'Archives')

        archive = Archive(createReportForm.filetype.data, createReportForm.tags.data)
        if createReportForm.filename.data != "":
            if createReportForm.filename.data+get_ext(createReportForm.filetype.data) in archive_dict:
                session['create_fail'] = createReportForm.filename.data+get_ext(createReportForm.filetype.data)
                return redirect(url_for("archives"))
            archive.set_filename(createReportForm.filename.data)
        archive_dict[archive.get_filename()+get_ext(archive.get_filetype())] = archive
        set_db('archive', 'Archives', archive_dict)

        if createReportForm.filetype.data == '1':
            jsdata = request.form['images']
            createPDF(f"{archive.get_filename()}.pdf", jsdata, createReportForm.charts.data)
        elif createReportForm.filetype.data == '2':
            createExcel(f"{archive.get_filename()}.xlsx",archive_dict)
        elif createReportForm.filetype.data == '3':
            createCSV(f"{archive.get_filename()}.csv", archive_dict)

        session['create_success'] = [archive.get_filename(), get_ext(archive.get_filetype()), archive.get_id()]

        return redirect(url_for('admin.reporting.archives', filetype=get_ext(archive.get_filetype())))

    data = []
    data.append(db_count_occurence('traffic', 'Sessions', 'get_created', '%m-%d'))
    data.append(db_get_qty('products', 'products', 'get_quantity'))
    # data.append(get_db('archive', 'Archives', 'get_created', '%m-%d'))
    print(data)
    return render_template('reports/admin_reports.html', data=data, form=createReportForm, datetime=datetime.datetime.now(), tab=tab)

@reporting.route('/logs')
def logs():
    tab = request.args.get('tab')
    if tab is None:
        tab = 'inventory'


    sessions_dict = get_db('traffic', 'Sessions')
    traffic = []
    for viewer in sessions_dict.values():
        traffic.append((viewer.get_ip(), viewer.get_session(), viewer.get_created(), viewer.get_views()[-1][0], viewer.get_views()[-1][-1]))
    
    delivery_dict = get_db('products', "delivery")
    deliveries = []
    for delivery in delivery_dict.values():
        deliveries.append((delivery.get_created(), delivery.get_sku(), delivery.get_restock_quantity(), delivery.get_delivery_date(), delivery.get_restock_price()))


    return render_template('reports/admin_logs.html', datetime=datetime.datetime.now(), deliveries= deliveries, traffic = traffic, tab=tab)

@reporting.route('/logs/session/<id>')
def get_session(id):
    sessions_dict = get_db('traffic', 'Sessions')
    viewer = sessions_dict[id]

    return render_template('reports/sessionviewer.html', session = viewer)
    

#ARCHIVES SECTION

@reporting.route('/archives', methods=['GET', 'POST'])
def archives():
    createReportForm = CreateReportForm(request.form)
    updateReportForm = UpdateReportForm(request.form)
    filetypes = {'1': '.pdf', '2': '.xlsx', "3": '.csv'}
    
    if request.method == 'POST' and createReportForm.validate():
        archive_dict = {}
        archive_dict = get_db('archive', 'Archives')
        archive = Archive(createReportForm.filetype.data, createReportForm.tags.data)
        if createReportForm.filename.data != "":
            if createReportForm.filename.data+filetypes[createReportForm.filetype.data] in archive_dict:
                session['create_fail'] = createReportForm.filename.data+filetypes[createReportForm.filetype.data]
                return redirect(url_for("archives"))
            archive.set_filename(createReportForm.filename.data)
        
        archive_dict[archive.get_filename()+filetypes[archive.get_filetype()]] = archive
        set_db('archive', 'Archives', archive_dict)
        
        return redirect(url_for("archives"))

    elif request.method == 'GET':
        archive_dict = {}
        archive_dict = get_db('archive', 'Archives')
        archives = []
        for key in archive_dict:
            file = archive_dict[key]
            archives.append((file.get_filename(), file.get_filetype(), file.get_tags(), file.get_created('date'), file.get_created('time'), file.get_id()))
        return render_template('reports/report_archives.html', archives=archives, form=createReportForm, u_form= updateReportForm)

@reporting.route('/archives/delete/<key>', methods=['POST']) 
def delete_archive(key):
    
    archive_dict = get_db('archive', 'Archives')
    
    if key.split('.')[1] == 'pdf':
        file = 'files\\reports\\'
    elif key.split('.')[1] == 'csv':
        file = 'files\\csv\\'
    else:
        file = 'files\\excel\\'

    if os.path.exists(app.config['STATIC_PATH']+file+key):
        os.remove(app.config['STATIC_PATH']+file+key)
    

    archive_dict.pop(key)

    set_db('archive', 'Archives', archive_dict)

    return redirect(url_for('admin.reporting.archives'))

@reporting.route('/archives/update/<id>', methods=['POST']) 
def update_archive(id):
    updateReportForm = UpdateReportForm(request.form)

    if request.method == 'POST' and updateReportForm.validate():
        archive_dict = {}

        db = shelve.open(app.config['ADMIN_PATH']+'archive.db', 'c')

        try:
            archive_dict = db['Archives']
        except:
            print("Error in retrieving Files from archive.db.")


        filenameList = []
        for key in archive_dict:
            report = archive_dict[key]
            filenameList.append(report.get_filename())

        for key in archive_dict:
            report = archive_dict[key]
            filename = updateReportForm.filename.data
            tags = updateReportForm.tags.data
            ext = get_ext(report.get_filetype())

            if report.get_id() == id:
                x = filenameList.index(report.get_filename())
                filenameList.pop(x)
                if filename == report.get_filename() and tags == report.get_tags():
                    session['update_none'] = ''
                elif filename == report.get_filename() and tags != report.get_tags():
                    session['update_success'] = ['tags', filename+ext]
                    report.set_tags(tags)
                    

                elif filename != report.get_filename() and tags == report.get_tags() and filename not in filenameList:
                    session['update_success'] = ['filename', report.get_filename()+ext, filename+ext]
                    if ext == '.pdf':
                        file = 'files\\reports\\'
                    elif ext == '.excel':
                        file = 'files\\excel\\'
                    elif ext == '.csv':
                        file = 'files\\csv\\'
                    os.rename(app.config['STATIC_PATH']+file+report.get_filename()+ext, app.config['STATIC_PATH']+file+filename+ext)
                    archive_dict.pop(report.get_filename()+get_ext(report.get_filetype()))
                    report.set_filename(filename)
                elif filename != report.get_filename() and tags != report.get_tags() and filename not in filenameList:
                    session['update_success'] = [report.get_filename()+ext, filename+ext]
                    if ext == '.pdf':
                        file = 'files\\reports\\'
                    elif ext == '.excel':
                        file = 'files\\excel\\'
                    elif ext == '.csv':
                        file = 'files\\csv\\'
                    os.rename(app.config['STATIC_PATH']+file+report.get_filename()+ext, app.config['STATIC_PATH']+file+filename+ext)
                    archive_dict.pop(report.get_filename()+get_ext(report.get_filetype()))
                    report.set_filename(filename)
                    report.set_tags(tags)
                else:
                    session['create_fail'] = filename+ext
                
                archive_dict[report.get_filename()+get_ext(report.get_filetype())] = report
                db['Archives'] = archive_dict
                
                break

        return redirect(url_for('admin.reporting.archives'))

#DOWNLOADS SECTION

@reporting.route('/download/<id>')
def download_reports(id):
    archive_dict = get_db('archive', 'Archives')
    for obj in list(archive_dict.values()):
        if obj.get_id() == id:
            filename = obj.get_filename()
            filetype = obj.get_filetype()
            break

    if filetype == '1':
        file = 'files\\reports\\'
    elif filetype == '2':
        file = 'files\\excel\\'
    elif filetype == '3':
        file = 'files\\csv\\'

    filename = filename + get_ext(filetype)
    
    return send_file('static\\'+file+filename, as_attachment=True)

@reporting.route('/open/<id>')
def open(id):
    archive_dict = get_db('archive', 'Archives')
    for obj in list(archive_dict.values()):
        if obj.get_id() == id:
            filename = obj.get_filename()
            filetype = obj.get_filetype()
            break

    if filetype == '1':
        file = 'files\\reports\\'
    elif filetype == '2':
        file = 'files\\excel\\'
    elif filetype == '3':
        file = 'files\\csv\\'

    filename = filename + get_ext(filetype)
    
    return send_file('static\\'+file+filename)