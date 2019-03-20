# -*- coding: utf-8 -*-
# @Time    : 2018/12/17 14:39
# @Author  : dodo8619
# @Email   : lj16888619@gmail.com
# @File    : clpa_sqlalchemy.py



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




# stmt = db.text("SELECT id FROM students where id=:id")
# results=db.get_engine().execute(stmt, id='1').fetchall()
# for row in results:
#     print(type(row))



# db.session.add_all( [Classes(id=7,name="cc111"),Classes(id=8,name="cc211"),Classes(id=9,name="cc311")]  )
# db.session.commit()

# data=Classes.query.filter_by(id=7).first()
# db.session.delete(data)
# db.session.commit()


# data=Classes.query.filter_by(id=9).first()
# data.name="xuliangjun"
# db.session.commit()



# stmt=db.text( " select GetWorkDay('2018-12-19 00:00:00' ,1 ) as t  " )
# results=db.get_engine().execute(stmt).first()
# print( results.t )


# sql=db.session.query(Classes).join(Students,isouter=False).filter(Classes.id==1).all()
# print(sql)