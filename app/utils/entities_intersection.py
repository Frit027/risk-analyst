from app.models import Category, Condition, Requirement, Deal
import sys


class EntitiesIntersection:
    @staticmethod
    def get_deals(category_id, requirement_id, condition_id):
        lst = []
        if category_id != 'NaN':
            s = set(deal.id for deal in Category.query.get(category_id).deals)
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
