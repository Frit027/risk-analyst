from app.models import Solution, Category, Condition, Requirement, Deal, Document
from app.constants import SolutionType
import csv
import re


class DatabaseFiller:
    @staticmethod
    def fill_solution(db):
        [db.session.add(Solution(name=type.value)) for type in SolutionType]

    @staticmethod
    def fill_category(db):
        with open('app/static/csv/categories.csv', encoding='utf-8') as f:
            [db.session.add(Category(name=name.rstrip())) for name in f]

    @staticmethod
    def fill_requirements(db):
        with open('app/static/csv/requirements.csv', encoding='utf-8') as f:
            [db.session.add(Requirement(name=data[0])) for data in csv.reader(f)]

    @staticmethod
    def fill_conditions(db):
        with open('app/static/csv/conditions.csv', encoding='utf-8') as f:
            [db.session.add(Condition(name=data[0])) for data in csv.reader(f)]

    @staticmethod
    def fill(db):
        pattern = re.compile(r'.[\d-]+/')

        with open('app/static/csv/data.csv', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            previous_deal_id = ''

            for i, row in enumerate(reader):
                doc_id = row['FullPath'][19:]
                deal_id = pattern.search(doc_id).group(0)[:-1]
                cond_str = row['COND_1']
                req_str = row['REQ_1']

                req = Requirement.query.filter_by(name=req_str).first()
                cond = Condition.query.filter_by(name=cond_str).first()

                doc_solution = Solution.query.filter_by(name=row['LOC_SOL']).first()
                deal_solution = Solution.query.filter_by(name=row['SOL_GLOB']).first()

                doc = Document(id=doc_id, req_detail=req_str, cond_detail=cond_str, instance=int(row['Instance']),
                               requirements=[req], conditions=[cond])
                doc_solution.documents.append(doc)
                req.documents.append(doc)
                cond.documents.append(doc)

                category = Category.query.filter_by(name=row['CAT_1']).first()

                if deal_id != previous_deal_id:
                    deal = Deal(id=deal_id, categories=[category], documents=[doc])
                    deal_solution.deals.append(deal)
                    category.deals.append(deal)
                    db.session.add(deal)
                else:
                    deal = Deal.query.get(deal_id)
                    deal.documents.append(doc)
                    db.session.add(deal)

                previous_deal_id = deal_id
                db.session.add(doc)
