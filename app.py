from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from constants import StatusType
import random
import sys


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost/trial'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'a78b1fe0e6491de8e9cf2a49a6e20c8f'

db = SQLAlchemy(app)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    deals = db.relationship('Deal', backref='category_deals', lazy='dynamic')


class Deal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    # статус для каждого дела (1:1)
    status = db.relationship('Status', backref='deal', uselist=False)

    # документы каждого дела
    documents = db.relationship('Document', backref='deal_documents', lazy='dynamic')


class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    # связь с таблицей Deal
    deal_id = db.Column(db.Integer, db.ForeignKey('deal.id'))

    # связь с таблицей Document
    document_id = db.Column(db.Integer, db.ForeignKey('document.id'))


class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)
    short_claim = db.Column(db.String(255), nullable=False)
    detail_claim = db.Column(db.Text, nullable=False)

    # статус для каждого дела (1:1)
    status = db.relationship('Status', backref='document', uselist=False)
    deal_id = db.Column(db.Integer, db.ForeignKey('deal.id'))


db.create_all()


@app.route('/', methods=['GET', 'POST'])
def index():
    doc1 = Document(url='it is url1', short_claim='short_claim1',
                    detail_claim='detail_claim1', status=Status(name=StatusType.PARTIALLY_SATISFIED.value))
    deal1 = Deal(documents=[doc1], status=Status(name=StatusType.DENIED.value))

    category_name = 'Продажа'
    category_names = list(x[0] for x in Category.query.with_entities(Category.name).all())
    categories = Category.query.all()
    for v in categories:
        print('NAME', v.name, end=': ')
        for d in v.deals:
            print(d.status.name, end=' ')
        print()

    if category_name in category_names:
        category = Category.query.filter_by(name=category_name).first()
        category.deals.append(deal1)
    else:
        category = Category(name=category_name, deals=[deal1])
    db.session.add(category)

    print('123456', category_names, file=sys.stdout)

    db.session.add(deal1)
    db.session.commit()

    return render_template('index.html')


@app.route('/data', methods=['GET', 'POST'])
def send_data():
    if request.method == 'POST':
        id = request.form['category'] # получаю id категории

        '''
        достаю категорию из БД и все относящиеся к ней дела,
        смотрю статус каждого дела,
        считаю прцоенты
        '''

        num1, num2 = [random.randint(1, 100) for _ in range(2)]

        # возвращаю проценты клиенту
        return {'satisfied_percent': num1,
                'partially_satisfied_percent': num2,
                'denied_percent': 100 - (num1 + num2)}


if __name__ == '__main__':
    app.run()
