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
    # from app.utils.database_filler import DatabaseFiller
    # DatabaseFiller.fill_solution(db)
    # DatabaseFiller.fill_category(db)
    # DatabaseFiller.fill_requirements(db)
    # DatabaseFiller.fill_conditions(db)
    # DatabaseFiller.fill(db)
    #
    # db.session.commit()

    cat_ids = session.get('cat_ids', [])
    req_ids = session.get('req_ids', [])
    cond_ids = session.get('cond_ids', [])
    sol_ids = session.get('sol_ids', [])

    return render_template('main.html',
                           categories=get_categories(),
                           requirements=Requirement.query.order_by(Requirement.name).all(),
                           conditions=Condition.query.order_by(Condition.name).all(),
                           solutions=Solution.query.order_by(Solution.name).all(),
                           docs=jsonpickle.encode(EntitiesIntersection.get_docs(cat_ids, req_ids, cond_ids, sol_ids)),
                           statistics=StatisticsCalculator.get_percents_by_solution(cat_ids, req_ids, cond_ids),
                           ids={'cat_ids': cat_ids, 'req_ids': req_ids, 'cond_ids': cond_ids, 'sol_ids': sol_ids}
                           )


@app.route('/docs_statistics', methods=['POST'])
def send_docs():
    def to_int(ids): return tuple(map(int, ids))

    cat_ids = to_int(request.form.getlist('cat_ids[]'))
    req_ids = to_int(request.form.getlist('req_ids[]'))
    cond_ids = to_int(request.form.getlist('cond_ids[]'))
    sol_ids = to_int(request.form.getlist('sol_ids[]'))

    session['cat_ids'] = cat_ids
    session['req_ids'] = req_ids
    session['cond_ids'] = cond_ids
    session['sol_ids'] = sol_ids

    return jsonpickle.encode({'docs': EntitiesIntersection.get_docs(cat_ids, req_ids, cond_ids, sol_ids),
                              'statistics': StatisticsCalculator.get_percents_by_solution(cat_ids, req_ids, cond_ids)
                              })


@app.route('/document/<string:doc_id>', methods=['GET'])
def document_page(doc_id):
    deal_id = doc_id.split('_')[0]
    doc_id = doc_id.replace('_', '/')
    deal = Deal.query.get(deal_id)
    doc = Document.query.get(doc_id)

    return render_template('detail_document.html',
                           documents=deal.documents,
                           cur_doc=doc,
                           category=deal.categories[0],
                           deal_solution=Solution.query.get(deal.solution_id).name,
                           doc_solution=Solution.query.get(doc.solution_id).name,
                           text=TxtParser.get_text(doc_id)
                           )


@app.route('/statistics', methods=['GET'])
def statistics_page():
    cat_ids = session.get('cat_ids', [])
    req_ids = session.get('req_ids', [])
    cond_ids = session.get('cond_ids', [])
    sol_ids = session.get('sol_ids', [])

    cur_cat = request.args.get('cur_cat', [])
    cur_req = request.args.get('cur_req', [])
    cur_cond = request.args.get('cur_cond', [])
    if cur_cat and cur_req and cur_cond:
        cat_ids = [cur_cat]
        req_ids = [cur_req]
        cond_ids = [cur_cond]
        sol_ids = []

    return render_template('diagrams.html',
                           categories=get_categories(),
                           requirements=Requirement.query.order_by(Requirement.name).all(),
                           conditions=Condition.query.order_by(Condition.name).all(),
                           percents=StatisticsCalculator.get_percents_by_solution(cat_ids, req_ids, cond_ids),
                           counts=StatisticsCalculator.get_count_instance(cat_ids, req_ids, cond_ids),
                           ids={'cat_ids': cat_ids, 'req_ids': req_ids, 'cond_ids': cond_ids, 'sol_ids': sol_ids}
                           )


@app.route('/data', methods=['POST'])
def send_statistics():
    def to_int(ids): return tuple(map(int, ids))

    cat_ids = to_int(request.form.getlist('cat_ids[]'))
    req_ids = to_int(request.form.getlist('req_ids[]'))
    cond_ids = to_int(request.form.getlist('cond_ids[]'))

    return {'percents_by_sol': StatisticsCalculator.get_percents_by_solution(cat_ids, req_ids, cond_ids),
            'count_by_inst': StatisticsCalculator.get_count_instance(cat_ids, req_ids, cond_ids)
            }


@app.route('/req_cond', methods=['POST'])
def send_req_cond():
    return jsonpickle.encode(EntitiesIntersection.get_req_cond_by_categories(request.form.getlist('cat_ids[]')))


@app.route('/all_req_cond', methods=['POST'])
def send_all_req_cond():
    session.pop('cat_ids', None)
    session.pop('req_ids', None)
    session.pop('cond_ids', None)

    return jsonpickle.encode({'requirements': Requirement.query.order_by(Requirement.name).all(),
                              'conditions': Condition.query.order_by(Condition.name).all()}
                             )


@app.route('/clear_req', methods=['POST'])
def clear_session_for_req():
    session.pop('req_ids', None)
    return ''


@app.route('/clear_cond', methods=['POST'])
def clear_session_for_cond():
    session.pop('cond_ids', None)
    return ''


@app.route('/clear_sol', methods=['POST'])
def clear_session_for_sol():
    session.pop('sol_ids', None)
    return ''


def get_categories():
    return [Category.query.filter_by(name='Банкротство гражданина').first(),
            Category.query.filter_by(name='Аренда земли').first(),
            Category.query.filter_by(name='Поставка электроэнергии').first()]
