# -*- coding: utf-8 -*-
"""
Models module
"""
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON
from application import db #pylint: disable=E0401


class Activity(db.Model):
    """
    Activity class
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    place = db.Column(db.String(200), nullable=False)
    executor = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(200), nullable=True)
    county = db.Column(db.String(50), nullable=False)
    district = db.Column(db.String(100), nullable=False)
    planned_visitors = db.Column(db.Integer, nullable=False, default=0)
    week_schedule = db.Column(JSON, nullable=True)
    number = db.Column(db.String(10), nullable=True)

    def __repr__(self):
        return '<Activity id: {}, {}-{}>'.format(self.id, self.category, self.name)


class Report(db.Model):
    """
    Report class
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    reporter_id = db.Column(db.String(100), db.ForeignKey('user.guid'), nullable=True)
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.id'), nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    issued = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    visitors = db.Column(db.Integer, nullable=False, default=0)
    image_source = db.Column(db.String(1000), nullable=True)

    activity = db.relationship('Activity', backref=db.backref('reports', lazy=True))
    reporter = db.relationship('User', backref=db.backref('reports', lazy=True))

    def __repr__(self):
        return '<Report id: {}, activity: {}, date: {}>'.format(
            self.id, self.activity_id, self.created)


USER_ROLE_REPORTER = 'reporter'
USER_ROLE_CUSTOMER = 'customer'
USER_ROLE_ADMIN = 'admin'
USER_ROLES = (USER_ROLE_REPORTER, USER_ROLE_CUSTOMER, USER_ROLE_ADMIN)


class User(db.Model):
    """
    User class
    """
    guid = db.Column(db.String(100), primary_key=True, unique=True)
    created = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(1000), nullable=False)
    password_secret = db.Column(db.String(100), nullable=False)
    confirm_code = db.Column(db.String(6), nullable=True)
    fullname = db.Column(db.String(1000), nullable=True)
    role = db.Column(db.String(50), nullable=False, default=USER_ROLE_REPORTER)
    disabled = db.Column(db.Boolean(), nullable=False, default=True)
    confirmed = db.Column(db.Boolean(), nullable=False, default=False)

    @property
    def roles(self):
        """
        Return concatenated roles
        """
        return self.role.split(',')

    def __repr__(self):
        return '<User id: {}, email: {}, disabled: {}>'.format(
            self.guid, self.email, self.disabled
        )


OTA_RECOVER_PASSWORD = 'recover_password'

class OneTimeAction(db.Model):
    """
    OneTime action class
    """
    guid = db.Column(db.String(100), primary_key=True, unique=True)
    action_type = db.Column(db.String(100), nullable=False, default=OTA_RECOVER_PASSWORD)
    created = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)
    body = db.Column(JSON, nullable=True)
