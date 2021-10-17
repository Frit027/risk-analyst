from app.models import Solution, Category, Condition, Requirement, Deal, Document
from app.constants import SolutionType
import csv
import re


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
        with open('app/static/csv/categories.csv', encoding='utf-8') as f:
            for name in f:
                db.session.add(Category(name=name.rstrip()))

    @staticmethod
    def fill_requirements(db):
        with open('app/static/csv/TotalReq_Банкротство_Аренда_Электроэнергия_2.csv', encoding='utf-8') as f:
            for data in csv.reader(f):
                db.session.add(Requirement(name=data[0]))

    @staticmethod
    def fill_conditions(db):
        with open('app/static/csv/TotalCond_Банкротство_Аренда_Электроэнергия_1.csv', encoding='utf-8') as f:
            for data in csv.reader(f):
                db.session.add(Condition(name=data[0]))

    @staticmethod
    def fill(db):
        pattern = re.compile(r'.[\d-]+/')

        with open('app/static/csv/TotalTable_Банкротство_Аренда_Электроэнергия_2.csv', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            previous_deal_id = ''

            for i, row in enumerate(reader):
                doc_id = row['FullPath'][19:]
                deal_id = pattern.search(doc_id).group(0)[:-1]
                doc_solution_name = row['LOC_SOL']
                deal_solution_name = row['SOL_GLOB']
                inst = int(row['Instance'])
                cond_str = row['COND_1']
                req_str = row['REQ_1']
                cat_str = row['CAT_1']

                # cat_lst = []
                # if row['CAT_1']:
                #     cat_lst.append(row['CAT_1'])
                # if row['CAT_2']:
                #     cat_lst.append(row['CAT_2'])
                # if row['CAT_3']:
                #     cat_lst.append(row['CAT_3'])

                req = Requirement.query.filter_by(name=req_str).first()
                cond = Condition.query.filter_by(name=cond_str).first()

                doc_solution = Solution.query.filter_by(name=doc_solution_name).first()
                deal_solution = Solution.query.filter_by(name=deal_solution_name).first()

                doc = Document(id=doc_id, req_detail=req_str, cond_detail=cond_str, instance=inst,
                               requirements=[req], conditions=[cond])
                doc_solution.documents.append(doc)
                req.documents.append(doc)
                cond.documents.append(doc)

                # categories = [Category.query.filter_by(name=name).first() for name in cat_lst]
                category = Category.query.filter_by(name=cat_str).first()

                if deal_id != previous_deal_id:
                    # deal = Deal(id=deal_id, categories=categories, documents=[doc])
                    deal = Deal(id=deal_id, categories=[category], documents=[doc])
                    deal_solution.deals.append(deal)
                    # [category.deals.append(deal) for category in categories]
                    category.deals.append(deal)

                    db.session.add(deal)
                else:
                    deal = Deal.query.get(deal_id)
                    deal.documents.append(doc)
                    db.session.add(deal)

                previous_deal_id = deal_id

                db.session.add(doc)

    @staticmethod
    def add_some_req_cond(db):
        with open('app/static/csv/bankruptcyReqListItog.csv', encoding='utf-8') as f1, \
             open('app/static/csv/bankruptcyCondListItog.csv', encoding='utf-8') as f2:
            for row in csv.reader(f1):
                db.session.add(Requirement(name=row[0]))

            for row in csv.reader(f2):
                db.session.add(Condition(name=row[0]))

    @staticmethod
    def update_documents(db):
        pattern = re.compile(r'.[\d-]+/')
        previous_deal_id = ''

        with open('app/static/csv/Merged Банкротство граждан_2.csv', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                doc_id = row['FullPath'][19:]
                deal_id = pattern.search(doc_id).group(0)[:-1]
                inst = int(row['Instance'])
                doc_solution_name = row['LOC_SOL']
                deal_solution_name = row['SOL_GLOB']
                cond_name = row['COND_1']
                req_name = row['REQ_1']
                if '( банкротом)' in req_name:
                    req_name = 'О признании гражданина несостоятельным (банкротом)'
                cat_name = row['CAT_1']

                doc_solution = Solution.query.filter_by(name=doc_solution_name).first()
                deal_solution = Solution.query.filter_by(name=deal_solution_name).first()

                req = Requirement.query.filter_by(name=req_name).first()
                cond = Condition.query.filter_by(name=cond_name).first()

                deal = Deal.query.get(deal_id)
                document = Document.query.get(doc_id) or Document(id=doc_id, req_detail=req_name, cond_detail=cond_name,
                                                                  instance=inst, requirements=[req], conditions=[cond])

                if document.solution_id is not None:
                    old_doc_solutions = Solution.query.get(doc.solution_id).documents
                    for doc in old_doc_solutions:
                        if doc.id == doc_id:
                            old_doc_solutions.remove(Document.query.get(doc_id))
                            break
                doc_solution.documents.append(document)

                old_deal_solutions = Solution.query.get(deal.solution_id).deals
                for deal in old_deal_solutions:
                    if deal.id == deal_id:
                        old_deal_solutions.remove(deal)
                        break
                deal_solution.deals.append(deal)

                if deal_id != previous_deal_id:
                    deal.documents = [document]
                    deal.categories = [Category.query.filter_by(name=cat_name).first()]
                else:
                    deal.documents.append(document)

                previous_deal_id = deal_id

                if req_name == 'О признании гражданина несостоятельным (банкротом)':
                    for doc in req.documents:
                        if doc.id == doc_id:
                            req.documents.remove(Document.query.get(doc_id))
                            break
                req.documents.append(document)
                cond.documents.append(document)

                db.session.commit()
