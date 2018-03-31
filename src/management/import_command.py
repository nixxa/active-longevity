"""
Import data command
"""
#pylint: disable=E1101
import csv

from flask_script import Command, Option

from application import db #pylint: disable=E0401
from models import Activity #pylint: disable=E0401


class ImportCommand(Command):
    """
    Import data from csv file
    """
    option_list = (
        Option('--file', '-f', dest='filename', help='Imported filename'),
    )

    def run(self, filename): #pylint: disable=E0202,W0221
        print('Filename: {}'.format(filename))
        count = 0
        with open(filename, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in reader:
                activity = Activity(
                    category=row[3].strip().strip(u'\ufeff').replace('*', '').lower().title(),
                    name=row[4].strip().strip(u'\ufeff').lower().title(),
                    place=row[7].strip().strip(u'\ufeff').lower(),
                    executor=row[10].strip().strip(u'\ufeff'),
                    address=row[9].strip().strip(u'\ufeff'),
                    county=row[0].strip().strip(u'\ufeff'),
                    district=row[8].strip().strip(u'\ufeff'),
                    planned_visitors=row[12].strip().strip(u'\ufeff')
                )
                print('Parsed activity {}'.format(count))
                count += 1
                db.session.add(activity)
                db.session.commit()
