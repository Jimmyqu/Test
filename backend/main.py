from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String
import json


class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)

class User(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    gender: Mapped[int] = mapped_column(Integer, nullable=False)


@app.route("/userList", methods = ['get'])
def userList():
  pageNum = request.args.get('pageNum') if request.args.get('pageNum') else 1
  pageSize = request.args.get('pageSize') if request.args.get('pageSize') else 6

  count = db.session.query(User).count()
  users = db.session.query(User).offset((int(pageNum) - 1) * int(pageSize)).limit(int(pageSize)).all()

  userList = []
  for user in users:
    userList.append({
      'id': user.id,
      'username': user.username,
      'gender': user.gender
    })
  return json.dumps({
    'code': 200,
    'msg': 'success',
    'data': {
      'total': count,
      'userList': userList,
      'pageNum': int(pageNum),
    }
  }, ensure_ascii=False)

@app.route("/addUser", methods = ['post'])
def addUser():
  username = request.json.get('username')
  gender = request.json.get('gender')
  user = User(username=username, gender=gender)
  try:
    db.session.add(user)
    db.session.commit()
    return json.dumps({
      'code': 200,
      'msg': 'success',
      'data': {
        'id': user.id,
        'username': user.username,
        'gender': user.gender
      }
    }, ensure_ascii=False)
  except:
    return json.dumps({
      'code': 500,
      'msg': 'error'
    }, ensure_ascii=False)

@app.route("/updateUser", methods = ['post'])
def updateUser():
  id = request.json.get('id')
  username = request.json.get('username')
  gender = request.json.get('gender')
  user = db.session.query(User).filter(User.id == id).first()
  user.username = username
  user.gender = gender

  try:
    db.session.commit()
    return json.dumps({
      'code': 200,
      'msg': 'success',
      'data': {
        'id': user.id,
        'username': user.username,
        'gender': user.gender
      }
    }, ensure_ascii=False)
  except:
    return json.dumps({
      'code': 500,
      'msg': 'error'
    }, ensure_ascii=False)

@app.route("/deleteUser", methods = ['post'])
def deleteUser():
  id = request.json.get('id')
  user = db.session.query(User).filter(User.id == id).first()
  db.session.delete(user)
  db.session.commit()
  return json.dumps({
    'code': 200,
    'msg': 'success',
    'data': {
      'id': user.id,
      'username': user.username,
      'gender': user.gender
    }
  }, ensure_ascii=False)


if __name__ == "__main__":
  app.run(debug=True)
