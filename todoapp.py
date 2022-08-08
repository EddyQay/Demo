from flask import Flask, render_template, request,redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:kosi@localhost:5432/todoapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# links  sqlalchemy to our flask app
db = SQLAlchemy(app)


class Todo(db.Model):
    __tablename__ = 'todolist'
    id = db.Column(db.Integer,primary_key=True)
    description = db.Column(db.String(), nullable=False)

    def __repr__(self) :
       return f'<Todo {self.id} {self.description}>'


# to create the tables we will do
db.create_all()
# MVC pattern
# route listening to our post request
@app.route('/todos/create', methods=['POST'])
# create a todo handler that runs when the request is sent
def create_todo():
# use request,form for the returned input value,manipulate our models
  # replace this description = request.form.get('description','')with
   description = request.get_json()['description'] 
   todo =Todo(description=description)
   db.session.add(todo)
   db.session.commit()
  #  instead of redirect return redirect(url_for('index'))we will use
   return jsonify({
    'description': todo.description
    })


# using a XMLHttpRequest to make ajax calls
@app.route('/')
def index():
    # flask uses render template to specify html files
  return render_template('index.html', data=Todo.query.all())

if __name__ == '__main__':
    app.run(host='0.0.0.0b', port=3000)