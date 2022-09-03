from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__) # Initiate the web app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app) # Initiate the database, which is necessary to store todos

class Todo(db.Model):
    '''
    A database model for todo items. Include 2 fields:
    id: primary field, integer
    title: string, the contents of the todo

    '''
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))

@app.route('/')
def index():
    todo_list = Todo.query.all()
    return render_template('base.html', todo_list=todo_list)


@app.route('/add', methods=['POST'])
def add():
    title = request.form.get("title")
    db.session.add(Todo(title=title))
    db.session.commit()
    return redirect(url_for("index")) # refresh the page after an addition


@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index")) # refresh the page after a deletion



if __name__ == "__main__":
    db.create_all()
    app.run(debug=True) # development mode