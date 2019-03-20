# -*- coding: utf-8 -*-
# @Time    : 2018/12/18 18:33
# @Author  : dodo8619
# @Email   : lj16888619@gmail.com
# @File    : sqlalchemy_onetomany.py.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://cljj_base_event:cljj_base_event@192.168.1.99:3306/cljj_base_event'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

# 班级表
class Classes(db.Model):
    __tablename__ = "classes"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(20),nullable=False,unique=True)
    students = db.relationship('Students',backref='sts',uselist=True)

# 学生表
class Students(db.Model):
    __tablename__ = "students"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(40),nullable=False)
    cls_id = db.Column(db.Integer,db.ForeignKey("classes.id"))    # 注意要写成（表名.字段名）



def addData1():
    db.session.add( Classes(id=1,name="cc1") )
    db.session.add( Classes(id=2,name="cc2") )
    db.session.add( Classes(id=3,name="cc3") )

    db.session.add(Students(id=1, name="stu1",cls_id =1))
    db.session.add(Students(id=2, name="stu2",cls_id =2))
    db.session.add(Students(id=3, name="stu3",cls_id =1))

    db.session.commit()

def selectData1():
    classes_datas =Classes.query.all()
    for cls in classes_datas:
        print(cls.students)

    student_datas = Students.query.all()
    for stu in student_datas:
        print(stu.sts)

# addData1()
# selectData1()


stmt = db.text("SELECT * FROM event where id=:id")
results=db.get_engine().execute(stmt, id='125').fetchall()
for row in results:
    print(row)