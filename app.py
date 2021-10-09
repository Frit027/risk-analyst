from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import random
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
                            back_populates='categories') # backref=db.backref('categories_deals', lazy='dynamic'))


class Deal(db.Model):
    id = db.Column(db.String(255), primary_key=True)
    status_id = db.Column(db.Integer, db.ForeignKey('status.id'))

    categories = db.relationship(Category,
                                 secondary=category_deal,
                                 back_populates='deals') # backref=db.backref('deals_categories', lazy='dynamic'))
    documents = db.relationship('Document', backref='deal_documents', lazy='dynamic')


class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    deals = db.relationship(Deal, backref='status_deals', lazy='dynamic')
    documents = db.relationship('Document', backref='status_documents', lazy='dynamic')


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
    con_detail = db.Column(db.Text, nullable=False)
    instance = db.Column(db.Integer, nullable=False)
    deal_id = db.Column(db.String(255), db.ForeignKey('deal.id'))
    status_id = db.Column(db.Integer, db.ForeignKey('status.id'))

    requirements = db.relationship('Requirement',
                                   secondary=document_requirement,
                                   back_populates='documents')
                                   # backref=db.backref('documents_requirements', lazy='dynamic'))
    conditions = db.relationship('Condition',
                                 secondary=document_condition,
                                 back_populates='documents')
                                 # backref=db.backref('documents_conditions', lazy='dynamic'))


class Requirement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)

    documents = db.relationship(Document,
                                secondary=document_requirement,
                                back_populates='requirements')
                                # backref=db.backref('requirements_documents', lazy='dynamic'))


class Condition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)

    documents = db.relationship(Document,
                                secondary=document_condition,
                                back_populates='conditions')
                                # backref=db.backref('conditions_documents', lazy='dynamic'))


db.create_all()


@app.route('/')
def index():
    # from database_filler import DatabaseFiller
    # DatabaseFiller.fill_status(db)
    # DatabaseFiller.fill_category(db)
    # DatabaseFiller.fill_requirements(db)
    # DatabaseFiller.fill_conditions(db)

    # db.session.add(category)
    # db.session.add(deal)
    db.session.commit()

    return render_template('index.html')


@app.route('/data', methods=['GET', 'POST'])
def send_data():
    if request.method == 'POST':
        id = request.form['category']

        num1, num2 = [random.randint(1, 49) for _ in range(2)]

        return {'satisfied_percent': num1,
                'partially_satisfied_percent': num2,
                'denied_percent': 100 - (num1 + num2)}


if __name__ == '__main__':
    app.run()
