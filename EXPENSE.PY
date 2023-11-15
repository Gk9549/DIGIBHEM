from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__) 

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://a****n:M*******5@database**************.us-east-1.rds.amazonaws.com:3306/database1'
db = SQLAlchemy(app)

# Expense Model
class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    amount = db.Column(db.Float)
    description = db.Column(db.String(255))
    category = db.Column(db.String(50))
    user_id = db.Column(db.Integer)

# API to add an expense
@app.route('/add_expense', methods=['POST'])
def add_expense():
    data = request.get_json()
    new_expense = Expense(
        date=data['date'],
        amount=data['amount'],
        description=data['description'],
        category=data['category'],
        user_id=data['user_id']
    )
    db.session.add(new_expense)
    db.session.commit()
    return jsonify({"message": "Expense added successfully"})

# API to retrieve expenses
@app.route('/get_expenses', methods=['GET'])
def get_expenses():
    expenses = Expense.query.all()
    expense_list = []
    for expense in expenses:
        expense_list.append({
            'id': expense.id,
            'date': expense.date.strftime('%Y-%m-%d'),
            'amount': expense.amount,
            'description': expense.description,
            'category': expense.category
        })

    return render_template('index.html', expenses=expense_list)

# Root route
@app.route('/')
def index():
    return render_template('expense.html', expenses=[])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
