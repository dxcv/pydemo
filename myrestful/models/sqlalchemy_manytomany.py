# -*- coding: utf-8 -*-
# @Time    : 2018/12/18 18:34
# @Author  : dodo8619
# @Email   : lj16888619@gmail.com
# @File    : sqlalchemy_manytomany.py


from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://cljj_base_event:cljj_base_event@192.168.1.99:3306/cljj_base_event'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


'''
学生与课程关联表
'''
tb_student_course = db.Table('tb_student_course',
                             db.Column('student_id', db.Integer, db.ForeignKey('students.id')),
                             db.Column('course_id', db.Integer, db.ForeignKey('courses.id'))
                             )


class Student(db.Model):
    '''
    学生
    '''
    __tablename__ = "students"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

     # 关联属性，多对多的情况，可以写在任意一个模型类中
    courses = db.relationship('Course', secondary=tb_student_course,
                              backref='relate_student' )


class Course(db.Model):
    '''
    课程
    '''
    __tablename__ = "courses"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)



def addData():
    stu1 = Student(name='s1')
    stu2 = Student(name='s2')
    stu3 = Student(name='s3')

    cou1 = Course(name='c4')
    cou2 = Course(name='c5')
    cou3 = Course(name='c6')

    stu1.courses = [cou2, cou3]    # 记得要添加关系
    stu2.courses = [cou2]
    stu3.courses = [cou1, cou2, cou3]

    db.session.add_all([stu1, stu2, stu2])
    db.session.add_all([cou1, cou2, cou3])

    db.session.commit()

def selectData():
    stu1 =Student.query.all()
    for course in stu1:
        print(course)

    print(Student)


# addData()
selectData()
