from app import db
import csv
import json
import sys
from models import Activity
from functions import AlchemyEncoder


if __name__ == '__main__':
    print('Filename: {}'.format(sys.argv[1]))
    count = 0
    with open(sys.argv[1], newline='', encoding='utf-8') as csvfile:
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
