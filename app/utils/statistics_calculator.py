import sys

from app.models import Solution
from app.utils.entities_intersection import EntitiesIntersection
from app.constants import SolutionType


class StatisticsCalculator:
    @staticmethod
    def __get_percent(deals, type):
        k = 0
        for deal in deals:
            solution = Solution.query.get(deal.solution_id).name
            if solution == type:
                k += 1
        return k / len(deals) * 100

    @staticmethod
    def get_percents_by_solution(cat_ids, req_ids, cond_ids):
        deals = EntitiesIntersection.get_deals(cat_ids, req_ids, cond_ids)
        if not deals:
            return {'response': None}
        return {'satisfied_percent': StatisticsCalculator.__get_percent(deals, SolutionType.SATISFIED.value),
                'partially_satisfied_percent': StatisticsCalculator.__get_percent(deals, SolutionType.PARTIALLY_SATISFIED.value),
                'denied_percent': StatisticsCalculator.__get_percent(deals, SolutionType.DENIED.value)
                }

    @staticmethod
    def get_count_instance(cat_ids, req_ids, cond_ids):
        count_1, count_2, count_3, count_4 = 0, 0, 0, 0
        deals = EntitiesIntersection.get_deals(cat_ids, req_ids, cond_ids)
        for deal in deals:
            if deal.documents[-1].instance == 1:
                count_1 += 1
            if deal.documents[-1].instance == 2:
                count_2 += 1
            if deal.documents[-1].instance == 3:
                count_3 += 1
            if deal.documents[-1].instance == 4:
                count_4 += 1
        return {'count_1': count_1, 'count_2': count_2, 'count_3': count_3, 'count_4': count_3}
