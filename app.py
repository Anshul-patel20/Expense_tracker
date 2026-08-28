from flask import Flask, render_template, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)

app.secret_key= "expenses-tracker-secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///expenses.db"
db = SQLAlchemy(app)
class Expenses(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    amount=db.Column(db.Float, nullable=False)
    category= db.Column(db.String(49), nullable=False)
    date= db.Column(db.String(20), nullable=False)
    description= db.Column(db.String(200))

@app.route("/")
def home():

    expenses= Expenses.query.all()

    total_spent = sum(expense.amount for expense in expenses)

    current_month = datetime.now().strftime("%Y-%m")

    this_month_expenses = [
        expense for expense in expenses
        if expense.date.startswith(current_month)
    ]

    this_month = sum(expense.amount for expense in this_month_expenses)
    transactions = len(expenses)
    
    return render_template("index.html", expenses=expenses,total_spent=total_spent, this_month=this_month, transactions=transactions)

@app.route("/add-expenses", methods=["POST"])
def add_expenses():

    amount=request.form["amount"]
    category=request.form["category"]
    date=request.form["date"]
    description=request.form["description"]

    expenses = Expenses(
    amount=amount,
    category=category,
    date=date,
    description=description
)
    

    db.session.add(expenses)
    db.session.commit()

    flash("Expense added successfully!")
    return redirect("/")

@app.route("/delete-expense/<int:id>", methods=["POST"])
def delete_expense(id):

    expenses = Expenses.query.get(id)

    db.session.delete(expenses)
    db.session.commit()

    return redirect("/")

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)