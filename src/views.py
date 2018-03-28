import os
from uuid import uuid4
from datetime import datetime
from app import app, auth, db
from flask import render_template, request
from constants import UPLOADS_DIR, ALLOWED_EXTENSIONS
from werkzeug.utils import secure_filename
from models import Activity, Report
from sqlalchemy.orm import load_only
from forms import ChecklistForm


class Place:
    def __init__(self, county, district):
        self.county = county
        self.district = district


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
    activity = Activity.query.first()
    report = Report(
        activity_id=activity.id,
        visitors=form.visitors.data
    )
    db.session.add(report)
    db.session.commit()
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
    if not allowed_file(file.filename):
        return 'File %s is not allowed' % file.filename, 500
    filename = secure_filename(file.filename)
    # create dir for checklist
    if not os.path.exists(UPLOADS_DIR):
        os.makedirs(UPLOADS_DIR)
    filepath = os.path.join(UPLOADS_DIR, filename)
    file.save(filepath)
    return '', 200


def allowed_file(filename):
    fext = os.path.splitext(filename)[1].lower()
    return fext in ALLOWED_EXTENSIONS
