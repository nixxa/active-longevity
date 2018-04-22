# -*- coding: utf-8 -*-
"""
Views module
"""
import os
import hashlib
import random
import string
from datetime import datetime, timedelta
from uuid import uuid4

from flask import (
    render_template, jsonify, redirect, send_from_directory, request, session, url_for)
from sqlalchemy import desc
from sqlalchemy.orm import load_only
from sqlalchemy.exc import IntegrityError

from constants import UPLOADS_DIR
from forms import (
    ChecklistForm, FilterReportsForm, ActivityForm, RegisterUserForm, RegisterConfirmForm,
    LoginForm, RecoverPasswordForm, RecoverPasswordFormPhase2)
from models import (
    Activity, Report, User, USER_ROLE_REPORTER, USER_ROLE_ADMIN, USER_ROLE_CUSTOMER,
    OneTimeAction, OTA_RECOVER_PASSWORD)
from linq import where, select

from application import app, db, config #pylint: disable=E0401
from pagination import Pagination
from functions import filter_by_form, fill_filter_form, is_safe_url
from sendmail import MailProvider
from security import authorize, check_auth


REPORTS_PER_PAGE = 20
TITLE = 'Активное долголетие'


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Render form or authenticate credentials
    """
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        if check_auth(form.username.data, form.password.data):
            return form.redirect('home_action')
        else:
            form.password.errors.append('Неправильная почта или пароль')
    return render_template(
        'login.html',
        form=form,
        title='Аутентификация | %s' % TITLE)


@app.route('/logout')
def logout():
    """
    Logout user from website
    """
    session['user'] = None
    return redirect('/')


@app.route('/recover/', methods=['GET', 'POST'])
def recover_password_action():
    """
    Recover password by email
    """
    form = RecoverPasswordForm()
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            form.email.errors.append('E-mail указан неверно')
        else:
            action = OneTimeAction(
                guid=uuid4().hex,
                action_type=OTA_RECOVER_PASSWORD,
                body=dict(user_id=user.guid)
            )
            db.session.add(action)
            db.session.commit()
            # send email with link to user
            mail = MailProvider()
            mail.send_recover_link(user, action.guid)
            return render_template(
                'recover_sent.html',
                title='Восстановление пароля | %s' % TITLE
            )
    return render_template(
        'recover_password.html',
        form=form,
        title='Восстановление пароля | %s' % TITLE
    )


@app.route('/recover/<code>/', methods=['GET', 'POST'])
def recover_password_phase2_action(code):
    """
    Setting new password
    """
    form = RecoverPasswordFormPhase2()
    action = OneTimeAction.query.get(code)
    user = User.query.get(action.body['user_id'])
    form.guid.data = user.guid
    if request.method == 'POST' and form.validate():
        user = User.query.get(form.guid.data)
        if user is None:
            form.email.errors.append('E-mail указан неверно')
        else:
            secret = config.SECRET_KEY
            passw = form.password.data
            hashstr = hashlib.sha256('{}:{}'.format(passw, secret).encode('utf-8')).hexdigest()
            user.password_hash = hashstr
            user.password_secret = secret
            db.session.delete(action)
            db.session.commit()
            return render_template(
                'recover_password_success.html',
                title='Восстановление пароля | %s' % TITLE
            )
    return render_template(
        'recover_password_2.html',
        form=form,
        title='Восстановление пароля | %s' % TITLE
    )


@app.route('/')
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

    for key in districts:
        districts[key] = sorted(districts[key])
    return render_template(
        'index.html',
        counties=counties,
        districts=districts,
        title='Районы | %s' % TITLE
    )


@app.route('/checklist/<county>/<district>/')
@authorize([USER_ROLE_REPORTER, USER_ROLE_CUSTOMER, USER_ROLE_ADMIN])
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
        title='Отчет | %s' % TITLE
    )


@app.route('/checklist/save/', methods=['POST'])
@authorize([USER_ROLE_REPORTER, USER_ROLE_CUSTOMER, USER_ROLE_ADMIN])
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
        reporter_id=session['user'].guid,
        image_source=os.path.join('/uploads/{}'.format(filename))
    )
    db.session.add(report)
    db.session.commit()
    return jsonify(dict(url='/checklist/{}/saved/'.format(report.id)))


@app.route('/checklist/<int:report_id>/saved/', methods=['GET'])
@authorize([USER_ROLE_REPORTER, USER_ROLE_CUSTOMER, USER_ROLE_ADMIN])
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
        title='Отчет | %s' % TITLE
    )


@app.route('/reports/', methods=['GET'], defaults={'page': 1})
@app.route('/reports/page/<int:page>/', methods=['GET'])
@authorize([USER_ROLE_CUSTOMER, USER_ROLE_ADMIN])
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
        title='Список отчетов | %s' % TITLE
    )


@app.route("/reports/delete/<int:report_id>/<int:page>/")
@authorize([USER_ROLE_CUSTOMER, USER_ROLE_ADMIN])
def report_delete_action(report_id, page):
    """
    Delete selected report and return to reports on same page
    """
    Report.query.filter_by(id=report_id).delete()
    return redirect('/reports/page/{}'.format(page))


@app.route('/activities/', methods=['GET'], defaults={'page': 1})
@app.route('/activities/page/<int:page>/', methods=['GET'])
@authorize([USER_ROLE_CUSTOMER, USER_ROLE_ADMIN])
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
        title='Список мероприятий | %s' % TITLE
    )


@app.route('/activities/edit/<int:activity_id>/', methods=['GET','POST'])
@authorize([USER_ROLE_CUSTOMER, USER_ROLE_ADMIN])
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
        title='Редактирование мероприятия | %s' % TITLE
    )

@app.route('/dashboard/', methods=['GET', 'POST'])
@authorize([USER_ROLE_CUSTOMER, USER_ROLE_ADMIN])
def dashboard():
    """
    Dashboard with graphs
    """
    start_date = datetime.utcnow().date()
    end_date = start_date + timedelta(days=1)
    if request.method == 'POST':
        end_date = datetime.strptime(request.values['to'], '%Y-%m-%d')
        start_date = datetime.strptime(request.values['from'], '%Y-%m-%d')
    query = Activity.query.options(load_only('category')).all()
    categories = sorted(set([row.name for row in query]))
    counties = sorted(set([row.county for row in query]))
    today_reports = Report.query \
        .filter(Report.issued >= start_date) \
        .filter(Report.issued < end_date) \
        .all()
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
        start=start_date.strftime('%Y-%m-%d'),
        end=end_date.strftime('%Y-%m-%d'),
        title='Графики | %s' % TITLE
    )


@app.route('/uploads/<path:path>')
def send_uplods(path):
    """
    Return uploads
    """
    return send_from_directory('uploads', path)


@app.route('/register/', methods=['GET', 'POST'])
def register_action():
    """
    Register user action
    """
    form = RegisterUserForm(request.values)
    if request.method == 'POST' and form.validate():
        secret = config.SECRET_KEY
        passw = form.password.data
        hashstr = hashlib.sha256('{}:{}'.format(passw, secret).encode('utf-8')).hexdigest()
        code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
        user = User(
            guid=uuid4().hex,
            created=datetime.utcnow(),
            email=form.email.data,
            password_secret=secret,
            password_hash=hashstr,
            confirm_code=code,
            fullname=form.fullname.data,
            role=USER_ROLE_REPORTER,
            disabled=True,
            confirmed=False
        )
        db.session.add(user)
        try:
            db.session.commit()
            mail = MailProvider()
            mail.send_registration_code(user)
        except IntegrityError as error:
            return 500, str(error)
        return redirect('/register/{}/confirm/'.format(user.guid))
    return render_template(
        'register.html',
        form=form,
        title='Регистрация | %s' % TITLE
    )


@app.route('/register/<user_id>/confirm/', methods=['GET', 'POST'], defaults={'code': None})
@app.route('/register/<user_id>/<code>/confirm/')
def register_confirm_action(user_id, code):
    """
    Confirmation for user registration
    """
    user = User.query.get(user_id)
    form = RegisterConfirmForm(request.values, obj=user)
    if request.method == 'POST' and form.validate():
        code = form.code.data
    if user.confirm_code == code:
        user.confirmed = True
        db.session.commit()
        return redirect('/register/{}/confirmed/'.format(user.guid))
    return render_template(
        'register_confirm.html',
        form=form,
        title='Подтверждение регистрации | %s' % TITLE
    )


@app.route('/register/<user_id>/confirmed/')
def register_confirmed_action(user_id):
    """
    Confirmed page
    """
    user = User.query.get(user_id)
    return render_template(
        'register_confirmed.html',
        title='Подтверждение регистрации | %s' % TITLE
    )


@app.route('/users/', defaults={'page': 1})
@app.route('/users/page/<int:page>/')
@authorize([USER_ROLE_CUSTOMER, USER_ROLE_ADMIN])
def users_action(page):
    """
    Users view
    """
    query = User.query
    total_count = query.count()
    users = query \
        .order_by(User.email) \
        .offset((page-1) * REPORTS_PER_PAGE) \
        .limit(REPORTS_PER_PAGE)

    pagination = Pagination(page, REPORTS_PER_PAGE, total_count)
    return render_template(
        'users.html',
        users=users,
        pagination=pagination,
        title='Пользователи | %s' % TITLE
    )


@app.route('/users/<user_id>/<int:page>/toggle/')
@authorize([USER_ROLE_CUSTOMER, USER_ROLE_ADMIN])
def toggle_user_action(user_id, page):
    """
    Toggle user status
    """
    user = User.query.get(user_id)
    user.disabled = not user.disabled
    return redirect('/users/page/{}'.format(page))


@app.route('/users/<user_id>/<int:page>/promote/<role>/')
@authorize([USER_ROLE_CUSTOMER, USER_ROLE_ADMIN])
def promote_user_action(user_id, page, role):
    """
    Toggle user status
    """
    user = User.query.get(user_id)
    user.role = user.role + ',' + role
    return redirect('/users/page/{}'.format(page))


@app.route('/users/<user_id>/<int:page>/demote/<role>/')
@authorize([USER_ROLE_CUSTOMER, USER_ROLE_ADMIN])
def demote_user_action(user_id, page, role):
    """
    Toggle user status
    """
    user = User.query.get(user_id)
    roles = user.roles
    roles.remove(role)
    user.role = ','.join(roles)
    return redirect('/users/page/{}'.format(page))
