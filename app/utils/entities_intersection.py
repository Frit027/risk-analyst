from app.models import Category, Condition, Requirement, Deal, Solution
import sys


class EntitiesIntersection:
    @staticmethod
    def get_deals(category_ids, requirement_id, condition_id):
        lst = []
        if len(category_ids):
            s = set(deal.id for id in category_ids for deal in Category.query.get(id).deals)
            print('ID дел данной категории:', s, file=sys.stdout)
            lst.append(s)
        if requirement_id != 'NaN':
            s = set(doc.deal_id for doc in Requirement.query.get(requirement_id).documents)
            print('ID дел данного требования:', s, file=sys.stdout)
            lst.append(s)
        if condition_id != 'NaN':
            s = set(doc.deal_id for doc in Condition.query.get(condition_id).documents)
            print('ID дел данного обстоятельства:', s, file=sys.stdout)
            lst.append(s)

        if lst:
            res = lst[0]
            for ids in lst:
                res.intersection_update(ids)
            print('Пересечение:', res, file=sys.stdout)
            return [Deal.query.get(id) for id in res]
        return []

    @staticmethod
    def get_docs(solution_id, category_ids, requirement_id, condition_id):
        lst = []
        if solution_id:
            docs = set(doc for doc in Solution.query.get(solution_id).documents)
            print('Доки данного решения:', docs, file=sys.stdout)
            lst.append(docs)
        if len(category_ids):
            s = set(doc for id in category_ids for deal in Category.query.get(id).deals for doc in deal.documents)
            print('Доки данной категории:', s, file=sys.stdout)
            lst.append(s)
        if requirement_id:
            s = set(doc for doc in Requirement.query.get(requirement_id).documents)
            print('Доки данного требования:', s, file=sys.stdout)
            lst.append(s)
        if condition_id:
            s = set(doc for doc in Condition.query.get(condition_id).documents)
            print('Доки данного обстоятельства:', s, file=sys.stdout)
            lst.append(s)

        if lst:
            res = lst[0]
            for docs in lst:
                res.intersection_update(docs)
            print('Пересечение:', res, file=sys.stdout)
            return res
        return []

    @staticmethod
    def get_req_cond_by_categories(category_ids):
        deal_ids = set(deal.id for id in category_ids for deal in Category.query.get(id).deals)
        docs = set(doc for id in deal_ids for doc in Deal.query.get(id).documents)
        s = sorted(set(req for doc in docs for req in doc.requirements), key=lambda x: x.name)
        return {'requirements': sorted(set(req for doc in docs for req in doc.requirements), key=lambda x: x.name),
                'conditions': sorted(set(cond for doc in docs for cond in doc.conditions), key=lambda x: x.name)
                }
