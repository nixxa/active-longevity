# -*- coding: utf-8 -*-
"""
Views module
"""
import os
from datetime import datetime
from uuid import uuid4

from flask import render_template, jsonify, redirect, send_from_directory, request
from sqlalchemy import desc
from sqlalchemy.orm import load_only, joinedload

from constants import UPLOADS_DIR
from forms import ChecklistForm, FilterReportsForm
from models import Activity, Report
from linq import where, select

from application import app, auth, db #pylint: disable=E0401
from pagination import Pagination


REPORTS_PER_PAGE = 20


@app.route('/')
@auth.login_required
def home_action():
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
def checklist_action(county, district):
    """
    Renders the home page.
    """
    activities = Activity.query.filter_by(county=county).filter_by(district=district).all()
    executors = sorted(set([x.executor for x in activities]))
    result = dict()
    for item in executors:
        result[item] = sorted(
            set(select(where(activities, lambda x: x.executor == item), lambda f: f.name)))
    return render_template(
        'checklist.html',
        collection=result,
        county=county,
        district=district,
        title='Отчет | Активное долголетие'
    )


@app.route('/checklist/save/', methods=['POST'])
@auth.login_required
def checklist_save_action():
    """
    Save verified checklist
    """
    form = ChecklistForm()
    if not form.validate_on_submit():
        return 400, 'Bad params'
    photo = form.photo.data
    filename = uuid4().hex + '.jpg'
    # create dir for checklist
    if not os.path.exists(UPLOADS_DIR):
        os.makedirs(UPLOADS_DIR)
    filepath = os.path.join(UPLOADS_DIR, filename)
    photo.save(filepath)
    # create report
    activity = Activity.query \
        .filter_by(county=form.county.data) \
        .filter_by(district=form.district.data) \
        .filter_by(executor=form.executor.data) \
        .filter_by(name=form.activity.data) \
        .first()
    report = Report(
        activity_id=activity.id,
        visitors=form.visitors.data,
        issued=form.date.data,
        image_source=os.path.join('/uploads/{}'.format(filename))
    )
    db.session.add(report)
    db.session.commit()
    return jsonify(dict(url='/checklist/{}/saved/'.format(report.id)))


@app.route('/checklist/<int:report_id>/saved/', methods=['GET'])
@auth.login_required
def checklist_saved_action(report_id):
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


@app.route('/reports/', methods=['GET'], defaults={'page': 1})
@app.route('/reports/page/<int:page>/', methods=['GET'])
@auth.login_required
def reports_action(page):
    """
    Save verified checklist
    """
    form = FilterReportsForm(request.values)
    all_reports_query = Report.query.join(Report.activity, aliased=True)
    if form.category.data is not None and form.category.data != 'None':
        all_reports_query = all_reports_query.filter_by(category=form.category.data)
    if form.name.data is not None and form.name.data != 'None':
        all_reports_query = all_reports_query.filter_by(name=form.name.data)
    if form.district.data is not None and form.district.data != 'None':
        all_reports_query = all_reports_query.filter_by(district=form.district.data)
    if form.executor.data is not None and form.executor.data != 'None':
        all_reports_query = all_reports_query.filter_by(executor=form.executor.data)
    reports_count = all_reports_query.count()

    all_reports_query = all_reports_query \
        .order_by(desc(Report.created))
    reports = all_reports_query \
        .offset((page-1) * REPORTS_PER_PAGE) \
        .limit(REPORTS_PER_PAGE)
    pagination = Pagination(page, REPORTS_PER_PAGE, reports_count)

    query = Activity.query.options(load_only('category', 'name', 'district', 'executor')).all()
    form.category.choices = [('None', 'все')] + \
        [(x, x) for x in sorted(set([row.category for row in query]))]
    form.name.choices = [('None', 'все')] + \
        [(x, x) for x in sorted(set([row.name for row in query]))]
    form.district.choices = [('None', 'все')] + \
        [(x, x) for x in sorted(set([row.district for row in query]))]
    form.executor.choices = [('None', 'все')] + \
        [(x, x) for x in sorted(set([row.executor for row in query]))]
    return render_template(
        'reports.html',
        reports=reports,
        pagination=pagination,
        form=form,
        title='Список отчетов | Активное долголетие'
    )


@app.route("/reports/delete/<int:report_id>/<int:page>/")
def report_delete_action(report_id, page):
    """
    Delete selected report and return to reports on same page
    """
    Report.query.filter_by(id=report_id).delete()
    return redirect('/reports/page/{}'.format(page))


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


@app.route('/uploads/<path:path>')
def send_js(path):
    return send_from_directory('uploads', path)
