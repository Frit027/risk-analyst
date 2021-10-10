from app import Solution, Category, Condition, Requirement
from constants import SolutionType
import csv


class DatabaseFiller:

    @staticmethod
    def fill_solution(db):
        st1 = Solution(name=SolutionType.SATISFIED.value)
        st2 = Solution(name=SolutionType.PARTIALLY_SATISFIED.value)
        st3 = Solution(name=SolutionType.DENIED.value)
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
