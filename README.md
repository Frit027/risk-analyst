<h1><div style="text-align: center;">RiskAnalyst</div></h1>

# Description
The website has the following features:
- search for court cases using various filters: category, requirements, circumstance and decision;
- viewing the hierarchy of the case;
- opening the text of a separate case document;
- viewing the characteristics of the case (category of the dispute, requirements, circumstances, the decision on the case as a whole, the decision at this instance);
- viewing decision statistics for the selected filters using a pie chart;
- viewing, by the selected filters, the number of cases completed on each of the instances using a histogram.
# Getting Started
1. Clone the repository to your folder.
2. Install all requirements (requirements.txt).
3. Create a database in PostgreSQL (pgAdmin 4).
4. Set up a connection to the database in the ```__init__.py``` using the template:  
```app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@server/db'```
5. Run the project.
# Usage
The website can be accessed via the following link:
[https://frit027.pythonanywhere.com/]()
# Built With
## Backend
1. Python 3.8
2. Flask
3. PostgreSQL (ORM: Flask-SQLAlchemy)
## Frontend
1. JavaScript (jQuery)
2. HTML5 (Jinja2)
3. CSS3