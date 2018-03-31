# -*- coding: utf-8 -*-
"""
Views module
"""
import os
from datetime import datetime
from uuid import uuid4

from flask import render_template, request, jsonify
from werkzeug.utils import secure_filename

from constants import UPLOADS_DIR
from forms import ChecklistForm
from models import Activity, Report

from application import app, auth, db #pylint: disable=E0401


@app.route('/')
@auth.login_required
def home():
    """
    Renders the home page.
    """
    activities = Activity.query.all()
    counties = set()
    districts = dict()
    for activity in activities:
        county = activity.county
        counties.add(county)
        if not county in districts:
            districts[activity.county] = set()
        districts[activity.county].add(activity.district)
    return render_template(
        'index.html',
        counties=counties,
        districts=districts,
        title='Районы | Активное долголетие'
    )


@app.route('/checklist/<county>/<district>/')
@auth.login_required
def checklist(county, district):
    """
    Renders the home page.
    """
    activities = Activity.query.filter_by(county=county).filter_by(district=district)
    objects = set([x.executor for x in activities])
    names = set([x.name for x in activities])
    return render_template(
        'checklist.html',
        objects=objects,
        names=names,
        county=county,
        district=district,
        title='Отчет | Активное долголетие'
    )


@app.route('/checklist/save/', methods=['POST'])
@auth.login_required
def checklist_save():
    """
    Save verified checklist
    """
    form = ChecklistForm()
    if not form.validate_on_submit():
        return 400, 'Bad params'
    photo = form.photo.data
    filename = uuid4().hex + '.jpg' # + secure_filename(photo.filename).split('.')[1]
    # create dir for checklist
    if not os.path.exists(UPLOADS_DIR):
        os.makedirs(UPLOADS_DIR)
    filepath = os.path.join(UPLOADS_DIR, filename)
    photo.save(filepath)
    # create report
    activity = Activity.query.first()
    report = Report(
        activity_id=activity.id,
        visitors=form.visitors.data,
        image_source='/uploads/{}'.format(filename)
    )
    db.session.add(report)
    db.session.commit()
    return jsonify(dict(url='/checklist/{}/saved/'.format(report.id)))


@app.route('/checklist/<int:report_id>/saved/', methods=['GET'])
@auth.login_required
def checklist_saved(report_id):
    """
    View saved report
    """
    report = Report.query.filter_by(id=report_id).first()
    return render_template(
        'checklist_saved.html',
        uid=str(report.id),
        save_date=datetime.now(),
        report=report,
        title='Отчет | Активное долголетие'
    )


@app.route('/reports/', methods=['GET'])
@auth.login_required
def reports():
    """
    Save verified checklist
    """
    reports = Report.query.all()
    return render_template(
        'reports.html',
        reports=reports,
        title='Список отчетов | Активное долголетие'
    )


@app.route('/dashboard/', methods=['GET'])
@auth.login_required
def dashboard():
    """
    Dashboard with graphs
    """
    return render_template(
        'dashboard.html',
        title='Графики | Активное долголетие'
    )


@app.route('/file/upload/', methods=['POST'])
@auth.login_required
def upload():
    """
    Upload and save file
    """
    # check if the post request has the file part
    if 'file' not in request.files:
        return 'No file part', 500
    file = request.files['file']
    # if user does not select file, browser also
    # submit a empty part without filename
    if not file or file.filename == '':
        return 'No selected file', 500
    filename = secure_filename(file.filename)
    # create dir for checklist
    if not os.path.exists(UPLOADS_DIR):
        os.makedirs(UPLOADS_DIR)
    filepath = os.path.join(UPLOADS_DIR, filename)
    file.save(filepath)
    return '', 200
