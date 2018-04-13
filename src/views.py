# -*- coding: utf-8 -*-
"""
Views module
"""
import os
import types
from datetime import datetime
from uuid import uuid4

from flask import render_template, jsonify, redirect, send_from_directory, request
from sqlalchemy import desc
from sqlalchemy.orm import load_only, joinedload

from constants import UPLOADS_DIR
from forms import ChecklistForm, FilterReportsForm, ActivityForm
from models import Activity, Report
from linq import where, select

from application import app, auth, db #pylint: disable=E0401
from pagination import Pagination
from functions import filter_by_form, fill_filter_form


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
    if not form.validate():
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
    all_reports_query = filter_by_form(all_reports_query, form)
    reports_count = all_reports_query.count()

    all_reports_query = all_reports_query \
        .order_by(desc(Report.created))
    reports = all_reports_query \
        .offset((page-1) * REPORTS_PER_PAGE) \
        .limit(REPORTS_PER_PAGE)
    pagination = Pagination(page, REPORTS_PER_PAGE, reports_count)

    fill_filter_form(form)
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


@app.route('/activities/', methods=['GET'], defaults={'page': 1})
@app.route('/activities/page/<int:page>/', methods=['GET'])
@auth.login_required
def activities_action(page):
    """
    Activities
    """
    form = FilterReportsForm(request.values)
    query = Activity.query
    query = filter_by_form(query, form)
    total_count = query.count()
    activities = query \
        .order_by(Activity.id) \
        .offset((page-1) * REPORTS_PER_PAGE) \
        .limit(REPORTS_PER_PAGE)

    pagination = Pagination(page, REPORTS_PER_PAGE, total_count)
    fill_filter_form(form)
    return render_template(
        'activities.html',
        activities=activities,
        pagination=pagination,
        form=form,
        title='Список мероприятий | Активное долголение'
    )


@app.route('/activities/edit/<int:activity_id>/', methods=['GET','POST'])
def activity_edit_action(activity_id):
    """
    Edit activity
    """
    activity = Activity.query.get(activity_id)
    form = ActivityForm(request.values, obj=activity)
    if request.method == 'POST' and form.validate():
        form.populate_obj(activity)
        db.session.add(activity)
        db.session.commit()
        return redirect('/activities/')
    return render_template(
        'activity.html',
        form=form,
        title='Редактирование мероприятия | Активное долголение'
    )

@app.route('/dashboard/', methods=['GET'])
@auth.login_required
def dashboard():
    """
    Dashboard with graphs
    """
    query = Activity.query.options(load_only('category')).all()
    categories = sorted(set([row.name for row in query]))
    counties = sorted(set([row.county for row in query]))
    today_reports = Report.query.filter_by(issued=datetime.now().date()).all()
    today_plan = []
    today_fact = []
    series = []
    for cat in categories:
        today_fact.append(
            sum(
                x for x in select(
                    where(today_reports, lambda x: x.activity.name == cat),
                    lambda x: x.visitors)
            )
        )
        today_plan.append(
            sum(
                x for x in select(
                    where(today_reports, lambda x: x.activity.name == cat),
                    lambda x: x.activity.planned_visitors)
            )
        )
        counties_data = []
        for county in counties:
            counties_data.append(
                sum(
                    x for x in select(
                        where(
                            today_reports,
                            lambda x: x.activity.county == county and x.activity.name == cat),
                        lambda x: x.visitors)
                )
            )
        series.append({
            'name': cat,
            'data': counties_data,
            'stack': 'v'
        })
    result = {
        'today': {
            'chart1': {
                'categories': categories,
                'fact': today_fact,
                'plan': today_plan
            },
            'chart2': {
                'districts': counties,
                'series': series
            }
        },
        'aggregate': {
        }
    }
    return render_template(
        'dashboard.html',
        data=result,
        title='Графики | Активное долголетие'
    )


@app.route('/uploads/<path:path>')
def send_uplods(path):
    """
    Return uploads
    """
    return send_from_directory('uploads', path)
