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
        count = 0
        print('Filename: {}'.format(filename))
        with open(filename, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in reader:
                week_schedule = dict()
                week_schedule['0'] = self.strip_line(row[10])
                week_schedule['1'] = self.strip_line(row[11])
                week_schedule['2'] = self.strip_line(row[12])
                week_schedule['3'] = self.strip_line(row[13])
                week_schedule['4'] = self.strip_line(row[14])
                week_schedule['5'] = self.strip_line(row[15])
                week_schedule['6'] = self.strip_line(row[16])
                activity = Activity(
                    category=self.strip_line(row[3]).replace('*', '').lower().title(),
                    name=self.strip_line(row[4]).lower().title(),
                    place=self.strip_line(row[7]).lower(),
                    executor=self.strip_line(row[19]),
                    address=self.strip_line(row[9]),
                    county=self.strip_line(row[0]),
                    district=self.strip_line(row[6]).title(),
                    planned_visitors=self.integer_or_zero(row[21]),
                    week_schedule=week_schedule,
                    number=self.number_or_none(row[1])
                )
                print('Parsed activity {}'.format(count))
                count += 1
                db.session.add(activity)
                db.session.commit()

    def strip_line(self, line):
        return line.strip().strip(u'\ufeff')

    def number_or_none(self, cell):
        try:
            return '%.1f' % round(float(self.strip_line(cell)), 1)
        except:
            return None
    
    def integer_or_zero(self, cell):
        try:
            return int(self.strip_line(cell))
        except:
            return 0
