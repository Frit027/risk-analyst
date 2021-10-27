from app.models import Category, Condition, Requirement, Deal, Solution


class EntitiesIntersection:
    @staticmethod
    def get_deals(category_ids, requirement_ids, condition_ids):
        lst = []
        if len(category_ids):
            lst.append(set(deal.id for id in category_ids for deal in Category.query.get(id).deals))
        if len(requirement_ids):
            lst.append(set(doc.deal_id for id in requirement_ids for doc in Requirement.query.get(id).documents))
        if len(condition_ids):
            lst.append(set(doc.deal_id for id in condition_ids for doc in Condition.query.get(id).documents))

        if lst:
            res = lst[0]
            [res.intersection_update(ids) for ids in lst]
            return [Deal.query.get(id) for id in res]
        return []

    @staticmethod
    def get_docs(category_ids, requirement_ids, condition_ids, solution_ids):
        lst = []
        if len(category_ids):
            lst.append(set(doc for id in category_ids for deal in Category.query.get(id).deals for doc in deal.documents))
        if len(requirement_ids):
            lst.append(set(doc for id in requirement_ids for doc in Requirement.query.get(id).documents))
        if len(condition_ids):
            lst.append(set(doc for id in condition_ids for doc in Condition.query.get(id).documents))
        if len(solution_ids):
            lst.append(set(doc for id in solution_ids for doc in Solution.query.get(id).documents))

        if lst:
            res = lst[0]
            [res.intersection_update(docs) for docs in lst]
            sort_docs = sorted(res, key=lambda x: x.id)
            r = []
            if len(sort_docs):
                [r.append(sort_docs[i]) for i in range(0, len(sort_docs) - 1)
                 if sort_docs[i].deal_id != sort_docs[i + 1].deal_id]
                r.append(sort_docs[-1])
            return r
        return []

    @staticmethod
    def get_req_cond_by_categories(category_ids):
        deal_ids = set(deal.id for id in category_ids for deal in Category.query.get(id).deals)
        docs = set(doc for id in deal_ids for doc in Deal.query.get(id).documents)
        return {'requirements': sorted(set(req for doc in docs for req in doc.requirements), key=lambda x: x.name),
                'conditions': sorted(set(cond for doc in docs for cond in doc.conditions), key=lambda x: x.name)
                }
