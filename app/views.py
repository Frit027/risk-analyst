from app.models import Solution, Category, Condition, Requirement, Document, Deal
from app.utils.entities_intersection import EntitiesIntersection
from app.utils.statistics_calculator import StatisticsCalculator
from app.utils.txt_parser import TxtParser
from app import app, db
from flask import render_template, request, session
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

    if 'cat_ids' in session or 'req_ids' in session or 'cond_ids' in session:
        cat_ids = session.get('cat_ids', [])
        req_ids = session.get('req_ids', [])
        cond_ids = session.get('cond_ids', [])

        session.pop('cat_ids', None)
        session.pop('req_ids', None)
        session.pop('cond_ids', None)
        return render_template('main.html',
                               solutions=Solution.query.order_by(Solution.name).all(),
                               categories=get_categories(),  # Category.query.order_by(Category.name).all(),
                               requirements=Requirement.query.order_by(Requirement.name).all(),
                               conditions=Condition.query.order_by(Condition.name).all(),
                               data=StatisticsCalculator.get_percents(cat_ids, req_ids, cond_ids))

    return render_template('main.html',
                           solutions=Solution.query.order_by(Solution.name).all(),
                           categories=get_categories(), # Category.query.order_by(Category.name).all(),
                           requirements=Requirement.query.order_by(Requirement.name).all(),
                           conditions=Condition.query.order_by(Condition.name).all()
                           )


@app.route('/documents', methods=['GET', 'POST'])
def documents_page():
    if request.method == 'POST':
        def to_int(ids): return tuple(map(int, ids))

        category_ids = to_int(request.form.getlist('cat_ids'))
        requirement_ids = to_int(request.form.getlist('req_ids'))
        condition_ids = to_int(request.form.getlist('cond_ids'))
        solution_ids = to_int(request.form.getlist('sol_ids'))

        session['cat_ids'] = category_ids
        session['req_ids'] = requirement_ids
        session['cond_ids'] = condition_ids

        return render_template('documents_list.html',
                               solutions=Solution.query.order_by(Solution.name).all(),
                               categories=get_categories(), # Category.query.order_by(Category.name).all(),
                               requirements=Requirement.query.order_by(Requirement.name).all(),
                               conditions=Condition.query.order_by(Condition.name).all(),
                               docs=EntitiesIntersection.get_docs(category_ids, requirement_ids, condition_ids, solution_ids)
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


@app.route('/data', methods=['GET', 'POST'])
def send_statistics():
    if request.method == 'POST':
        return StatisticsCalculator.get_percents(request.form.getlist('cat_ids[]'),
                                                 request.form.getlist('req_ids[]'),
                                                 request.form.getlist('cond_ids[]')
                                                 )


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
