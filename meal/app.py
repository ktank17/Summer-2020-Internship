from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms_sqlalchemy.fields import QuerySelectField

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Meal %r>' % self.id

def meal_query():
    return Meal.query

class MealForm(FlaskForm):
    opts = QuerySelectField(query_factory=meal_query, allow_blank=True)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        meal_content = request.form['content']
        new_meal = Meal(content=meal_content)

        try:
            db.session.add(new_meal)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your meal'

    else:
        meals = Meal.query.order_by(Meal.date_created).all()
        return render_template('index.html', meals=meals)

@app.route('/', methods=['GET'])
def dropdown():
    mealoptions = ['Breakfast', 'Lunch', 'Snack', 'Dinner']
    return render_template('index.html', mealoptions=mealoptions)


@app.route('/delete/<int:id>')
def delete(id):
    meal_to_delete = Meal.query.get_or_404(id)

    try:
        db.session.delete(meal_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that meal'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    meal = Meal.query.get_or_404(id)

    if request.method == 'POST':
        meal.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your meal'

    else:
        return render_template('update.html', meal=meal)


if __name__ == "__main__":
    app.run(debug=True)