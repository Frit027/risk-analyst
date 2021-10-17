from app.models import Solution


class StatisticsCalculator:
    @staticmethod
    def get_percent(deals, type):
        k = 0
        for deal in deals:
            solution = Solution.query.get(deal.solution_id).name
            if solution == type:
                k += 1
        return k / len(deals) * 100
