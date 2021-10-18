from app.models import Solution, Category, Condition, Requirement, Document, Deal
from app.utils.entities_intersection import EntitiesIntersection
from app.utils.statistics_calculator import StatisticsCalculator
from app.utils.txt_parser import TxtParser
from app.constants import SolutionType
from app import app, db
from flask import render_template, request
import jsonpickle
import sys


@app.route('/')
def index():
    # from app.database_filler import DatabaseFiller
    # DatabaseFiller.fill_solution(db)
    # DatabaseFiller.fill_category(db)
    # DatabaseFiller.fill_requirements(db)
    # DatabaseFiller.fill_conditions(db)
    # DatabaseFiller.fill(db)
    # DatabaseFiller.add_some_req_cond(db)
    # DatabaseFiller.update_documents(db)

    # db.session.commit()

    return render_template('index.html',
                           solutions=Solution.query.order_by(Solution.name).all(),
                           categories=get_categories(), # Category.query.order_by(Category.name).all(),
                           requirements=Requirement.query.order_by(Requirement.name).all(),
                           conditions=Condition.query.order_by(Condition.name).all()
                           )


@app.route('/documents', methods=['GET', 'POST'])
def documents_page():
    if request.method == 'POST':
        solution_id = request.form.get('sol_id')
        category_ids = tuple(map(int, request.form.getlist('cat_ids')))
        requirement_id = request.form.get('req_id')
        condition_id = request.form.get('cond_id')

        print(f'solution_id = {solution_id}', file=sys.stdout)
        print(f'category_ids = {category_ids}', file=sys.stdout)
        print(f'requirement_id = {requirement_id}', file=sys.stdout)
        print(f'condition_id = {condition_id}', file=sys.stdout)
        res = EntitiesIntersection.get_docs(solution_id, category_ids, requirement_id, condition_id)

        return render_template('documents_list.html',
                               solutions=Solution.query.order_by(Solution.name).all(),
                               categories=get_categories(), # Category.query.order_by(Category.name).all(),
                               requirements=Requirement.query.order_by(Requirement.name).all(),
                               conditions=Condition.query.order_by(Condition.name).all(),
                               docs=res
                               )
    return render_template('documents_list.html',
                           solutions=Solution.query.order_by(Solution.name).all(),
                           categories=get_categories(), # Category.query.order_by(Category.name).all(),
                           requirements=Requirement.query.order_by(Requirement.name).all(),
                           conditions=Condition.query.order_by(Condition.name).all()
                           )


@app.route('/document/<string:doc_id>', methods=['GET'])
def document_page(doc_id):
    deal_id = doc_id.split('_')[0]
    doc_id = doc_id.replace('_', '/')

    text_doc = TxtParser.f(doc_id)

    deal = Deal.query.get(deal_id)
    doc = Document.query.get(doc_id)
    categories = deal.categories
    deal_solution = Solution.query.get(deal.solution_id).name
    doc_solution = Solution.query.get(doc.solution_id).name

    return render_template('detail_document.html',
                           documents=deal.documents,
                           cur_doc=doc,
                           category=categories[0],
                           deal_solution=deal_solution,
                           doc_solution=doc_solution,
                           text=text_doc
                           )


@app.route('/data', methods=['POST'])
def send_statistics():
    if request.method == 'POST':
        deals = EntitiesIntersection.get_deals(request.form.getlist('cat_ids[]'),
                                               request.form['req_id'],
                                               request.form['cond_id']
                                               )

        if not deals:
            return {'response': None}

        return {'satisfied_percent': StatisticsCalculator.get_percent(deals, SolutionType.SATISFIED.value),
                'partially_satisfied_percent': StatisticsCalculator.get_percent(deals, SolutionType.PARTIALLY_SATISFIED.value),
                'denied_percent': StatisticsCalculator.get_percent(deals, SolutionType.DENIED.value)
                }


@app.route('/req_cond', methods=['POST'])
def send_req_cond():
    return jsonpickle.encode(EntitiesIntersection.get_req_cond_by_categories(request.form.getlist('cat_ids[]')))


@app.route('/all_req_cond', methods=['POST'])
def send_all_req_cond():
    return jsonpickle.encode({'requirements': Requirement.query.order_by(Requirement.name).all(),
                              'conditions': Condition.query.order_by(Condition.name).all()}
                             )


def get_categories():
    return [Category.query.filter_by(name='Банкротство гражданина').first(),
            Category.query.filter_by(name='Аренда земли').first(),
            Category.query.filter_by(name='Поставка электроэнергии').first()]
