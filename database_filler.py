from app import Status, Category, Condition, Requirement
from constants import StatusType
import csv


class DatabaseFiller:

    @staticmethod
    def fill_status(db):
        st1 = Status(name=StatusType.SATISFIED.value)
        st2 = Status(name=StatusType.PARTIALLY_SATISFIED.value)
        st3 = Status(name=StatusType.DENIED.value)
        for st in [st1, st2, st3]:
            db.session.add(st)

    @staticmethod
    def fill_category(db):
        with open('static/categories.csv', encoding='utf-8') as f:
            for name in f:
                db.session.add(Category(name=name.rstrip()))

    @staticmethod
    def fill_requirements(db):
        with open('static/requirements.csv', encoding='utf-8') as f:
            for data in csv.reader(f):
                db.session.add(Requirement(name=data[0]))

    @staticmethod
    def fill_conditions(db):
        with open('static/conditions.csv', encoding='utf-8') as f:
            for data in csv.reader(f):
                db.session.add(Condition(name=data[0]))
