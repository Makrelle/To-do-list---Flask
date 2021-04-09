import os


from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

base_dir = os.path.abspath(os.path.dirname(__file__))

# database configuration
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///"\
                                        + os.path.join(base_dir, "db.sqlite")

db = SQLAlchemy(app)
db.init_app(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)


@app.route("/")
def home():
    complete = Todo.query.filter_by(complete=True).all()
    incomplete = Todo.query.filter_by(complete=False).all()
    c_count = len(complete)
    i_count = len(incomplete)
    return render_template("index.html", complete=complete,
                           incomplete=incomplete, c_count=c_count,
                           i_count=i_count)


@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("task_name")
    new_todo = Todo(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/update/<int:todo_id>")
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("home"))


@app.before_first_request
def create_tables():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)

