# -*- coding: utf-8 -*-
"""
Models module
"""
from datetime import datetime
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

    def __repr__(self):
        return '<Activity id: {}, {}-{}>'.format(self.id, self.category, self.name)


class Report(db.Model):
    """
    Report class
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.id'), nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    issued = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    visitors = db.Column(db.Integer, nullable=False, default=0)
    image_source = db.Column(db.String(1000), nullable=True)

    activity = db.relationship('Activity', backref=db.backref('reports', lazy=True))

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

    def __repr__(self):
        return '<User id: {}, email: {}, disabled: {}>'.format(
            self.guid, self.email, self.disabled
        )
