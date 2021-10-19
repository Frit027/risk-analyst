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
    def get_percents(cat_ids, req_ids, cond_ids):
        deals = EntitiesIntersection.get_deals(cat_ids, req_ids, cond_ids)
        if not deals:
            return {'response': None}
        return {'satisfied_percent': StatisticsCalculator.__get_percent(deals, SolutionType.SATISFIED.value),
                'partially_satisfied_percent': StatisticsCalculator.__get_percent(deals, SolutionType.PARTIALLY_SATISFIED.value),
                'denied_percent': StatisticsCalculator.__get_percent(deals, SolutionType.DENIED.value)
                }
