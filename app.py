from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from constants import SolutionType
import sys


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost/trial'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'a78b1fe0e6491de8e9cf2a49a6e20c8f'

db = SQLAlchemy(app)


category_deal = db.Table(
    'category_deal',
    db.Column('category_id', db.Integer, db.ForeignKey('category.id')),
    db.Column('deal_id', db.String(255), db.ForeignKey('deal.id'))
)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    deals = db.relationship('Deal',
                            secondary=category_deal,
                            back_populates='categories')


class Deal(db.Model):
    id = db.Column(db.String(255), primary_key=True)
    solution_id = db.Column(db.Integer, db.ForeignKey('solution.id'))

    categories = db.relationship(Category,
                                 secondary=category_deal,
                                 back_populates='deals')
    documents = db.relationship('Document', backref='deal_documents', lazy='dynamic')


class Solution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    deals = db.relationship(Deal, backref='solutions_deals', lazy='dynamic')
    documents = db.relationship('Document', backref='solution_documents', lazy='dynamic')


document_requirement = db.Table(
    'document_requirement',
    db.Column('document_id', db.String(255), db.ForeignKey('document.id')),
    db.Column('requirement_id', db.Integer, db.ForeignKey('requirement.id'))
)


document_condition = db.Table(
    'document_condition',
    db.Column('document_id', db.String(255), db.ForeignKey('document.id')),
    db.Column('condition_id', db.Integer, db.ForeignKey('condition.id'))
)


class Document(db.Model):
    id = db.Column(db.String(255), primary_key=True)
    req_detail = db.Column(db.Text, nullable=False)
    cond_detail = db.Column(db.Text, nullable=False)
    instance = db.Column(db.Integer, nullable=False)
    deal_id = db.Column(db.String(255), db.ForeignKey('deal.id'))
    solution_id = db.Column(db.Integer, db.ForeignKey('solution.id'))

    requirements = db.relationship('Requirement',
                                   secondary=document_requirement,
                                   back_populates='documents')
    conditions = db.relationship('Condition',
                                 secondary=document_condition,
                                 back_populates='documents')


class Requirement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)

    documents = db.relationship(Document,
                                secondary=document_requirement,
                                back_populates='requirements')


class Condition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)

    documents = db.relationship(Document,
                                secondary=document_condition,
                                back_populates='conditions')


# db.create_all()


@app.route('/')
def index():
    # from database_filler import DatabaseFiller
    # DatabaseFiller.fill_solution(db)
    # DatabaseFiller.fill_category(db)
    # DatabaseFiller.fill_requirements(db)
    # DatabaseFiller.fill_conditions(db)
    # DatabaseFiller.fill(db)

    db.session.commit()

    return render_template('index.html',
                           solutions=Solution.query.order_by(Solution.name).all(),
                           categories=Category.query.order_by(Category.name).all(),
                           requirements=Requirement.query.order_by(Requirement.name).all(),
                           conditions=Condition.query.order_by(Condition.name).all())


@app.route('/data', methods=['GET', 'POST'])
def send_statistics():
    if request.method == 'POST':
        solution_id = request.form['sol_id']
        category_id = request.form['cat_id']
        requirement_id = request.form['req_id']
        condition_id = request.form['cond_id']

        print(f'{solution_id} {category_id} {requirement_id} {condition_id}', file=sys.stdout)

        deals = get_deals(solution_id, category_id, requirement_id, condition_id)
        if not deals:
            return {'response': None}

        return {'satisfied_percent': get_percent(deals, SolutionType.SATISFIED.value),
                'partially_satisfied_percent': get_percent(deals, SolutionType.PARTIALLY_SATISFIED.value),
                'denied_percent': get_percent(deals, SolutionType.DENIED.value)}


def get_deals(solution_id, category_id, requirement_id, condition_id):
    lst = []
    if solution_id != 'NaN':
        s = set(deal.id for deal in Solution.query.get(solution_id).deals)
        print('ID дел данного решения:', s, file=sys.stdout)
        lst.append(s)
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


def get_percent(deals, type):
    k = 0
    for deal in deals:
        solution = Solution.query.get(deal.solution_id).name
        if solution == type:
            k += 1
    return k / len(deals) * 100


if __name__ == '__main__':
    app.run()
