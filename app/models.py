from app import db


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
