from app.models import Category, Condition, Requirement, Deal, Solution
import sys


class EntitiesIntersection:
    @staticmethod
    def get_deals(category_ids, requirement_ids, condition_ids):
        lst = []
        if len(category_ids):
            s = set(deal.id for id in category_ids for deal in Category.query.get(id).deals)
            print('IDs дел данных категорий:', s, file=sys.stdout)
            lst.append(s)
        if len(requirement_ids):
            s = set(doc.deal_id for id in requirement_ids for doc in Requirement.query.get(id).documents)
            print('IDs дел данных требований:', s, file=sys.stdout)
            lst.append(s)
        if len(condition_ids):
            s = set(doc.deal_id for id in condition_ids for doc in Condition.query.get(id).documents)
            print('IDs дел данных обстоятельств:', s, file=sys.stdout)
            lst.append(s)

        if lst:
            res = lst[0]
            for ids in lst:
                res.intersection_update(ids)
            print('Пересечение дел:', res, file=sys.stdout)
            return [Deal.query.get(id) for id in res]
        return []

    @staticmethod
    def get_docs(category_ids, requirement_ids, condition_ids, solution_ids):
        lst = []
        if len(category_ids):
            s = set(doc for id in category_ids for deal in Category.query.get(id).deals for doc in deal.documents)
            # print(f'category_ids = {category_ids}', file=sys.stdout)
            print('Доки данной категории:', s, file=sys.stdout)
            lst.append(s)
        if len(requirement_ids):
            s = set(doc for id in requirement_ids for doc in Requirement.query.get(id).documents)
            # print(f'requirement_ids = {requirement_ids}', file=sys.stdout)
            print('Доки данного требования:', s, file=sys.stdout)
            lst.append(s)
        if len(condition_ids):
            s = set(doc for id in condition_ids for doc in Condition.query.get(id).documents)
            # print(f'condition_ids = {condition_ids}', file=sys.stdout)
            print('Доки данного обстоятельства:', s, file=sys.stdout)
            lst.append(s)
        if len(solution_ids):
            docs = set(doc for id in solution_ids for doc in Solution.query.get(id).documents)
            print('Доки данного решения:', docs, file=sys.stdout)
            # print(f'solution_ids = {solution_ids}', file=sys.stdout)
            lst.append(docs)

        if lst:
            res = lst[0]
            for docs in lst:
                res.intersection_update(docs)
            print('Пересечение доков:', res, file=sys.stdout)
            return res
        return []

    @staticmethod
    def get_req_cond_by_categories(category_ids):
        deal_ids = set(deal.id for id in category_ids for deal in Category.query.get(id).deals)
        docs = set(doc for id in deal_ids for doc in Deal.query.get(id).documents)
        return {'requirements': sorted(set(req for doc in docs for req in doc.requirements), key=lambda x: x.name),
                'conditions': sorted(set(cond for doc in docs for cond in doc.conditions), key=lambda x: x.name)
                }
