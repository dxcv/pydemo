# -*- coding: utf-8 -*-
# @Time    : 2018/12/7 13:48
# @Author  : dodo8619
# @Email   : lj16888619@gmail.com
# @File    : StudentDb.py


from pymongo import MongoClient , ASCENDING ,DESCENDING
from random import sample , randint

from bson.objectid import ObjectId

client = MongoClient('192.168.1.99', 27017)

timedtask_db=client.get_database("timedtask")

stuent_colle=timedtask_db.get_collection("student")

cache_colle=timedtask_db.get_collection("tcache")


def m_insert_many():
    many_students=[]
    for i in range(10):
        o={
            "name":sample( [ "Tom","Jim","Om" ] , 1 ) ,
            "age":randint(10,100),
            "sex":randint(0,1),
            "createtime": datetime.now()
        }
        many_students.append(o)

    stuent_colle.insert_many(many_students)



def m_find_byId():
    obj=stuent_colle.find_one({"_id":ObjectId(str("5c0a0e07c7a32c3fac36697d")) })
    print(obj)

def m_find_byage():
    ''''''
    sts=stuent_colle.find( {"age":{ "$gte": 55 , "$lte" : 70 }} ).sort("age",DESCENDING)
    for s in sts:
        print(s)


def m_find_bytime():
    sts=stuent_colle.find( { "createtime" :
                                 { "$gte" :  datetime.strptime( "2018-12-07 14:07:16" , "%Y-%m-%d %H:%M:%S" )   } } ).sort("createtime",DESCENDING)
    for s in sts:
        print(s)


def m_findall():
    # for post in stuent_colle.find():
    #     pprint.pprint(post)
    objs=stuent_colle.find().skip(1).limit(200).sort([("age", ASCENDING), ("sex", DESCENDING)])
    for obj in objs:
        print(obj)

def m_in():
    objs=stuent_colle.find( { "age":{ "$in":(16,51) }  } )
    if objs:
        print(objs.count())
        for obj in objs:
            print(obj)

def m_or():
    objs=stuent_colle.find( {"$or":[{"age":16},{"age":51}] } )
    if objs:
        print(objs.count())
        for obj in objs:
            print(obj)



def m_update_one():
    stuent_colle.update_one( {"_id":ObjectId("5c0a0e07c7a32c3fac36697d")} , {"$set":{"age":168,"name":"徐良俊"}} )


def m_remove_one():
    stuent_colle.remove({"_id":ObjectId("5c0a0e07c7a32c3fac36697d")})


def m_type():
    for i in stuent_colle.find({'age': {'$type': 0}}):
        print(i)



#  insert_one   insert_many
#  update_one   update_many
#  find_one     find
#  remove/delete_one      delete_many

#  skip  limit
#  count
#  sorted

#  $set  $lt  $lte  $eq  $ne  $gt  $gte

# m_findall()



from datetime import datetime
from mymongodb.Util import DictObj

# t = Tcache(cache_name="粗",url="http://www.baidu.com",createtime=datetime.now(),runtime="XXXX")
# cache_colle.insert_one(ObjectToDict(t))


obj=cache_colle.find_one({"cache_name":"粗"})
objb=DictObj(obj)
print(objb.url)
