# -*- coding: utf-8 -*-
# @Time    : 2018/12/27 18:07
# @Author  : dodo8619
# @Email   : lj16888619@gmail.com
# @File    : oraclemong.py

from pymongo import MongoClient
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import json,decimal,datetime

class MyJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        if isinstance(o, datetime.datetime):
            return datetime.datetime.strftime(o,"%Y-%m-%d %H:%M:%S")
        if isinstance(o, web_fundinfo):
            return convert_to_dict(o)
        if isinstance(o, curfscode):
            return convert_to_dict(o)

        super(MyJSONEncoder, self).default(o)

flask=Flask(__name__)
flask.config["SQLALCHEMY_DATABASE_URI"] ='oracle://cl_fof:cl_fof@192.168.1.242:1521/oru1'
flask.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
flask.config['SQLALCHEMY_ECHO'] = False
flask.config['SQLALCHEMY_BINDS'] = {
    'dc':'oracle://dc_u1:dc@192.168.1.242:1521/oru1',
    'fof':'oracle://cl_fof:cl_fof@192.168.1.242:1521/oru1',
    'web':'oracle://clweb_new:clweb_new@192.168.1.242:1521/oru1',
    'prod':'oracle://clprod:111111@192.168.1.242:1521/oru1'
}

db = SQLAlchemy(flask)
webdb = SQLAlchemy(flask)
webdb.session.bind = webdb.get_engine(bind='web')
proddb = SQLAlchemy(flask)
proddb.session.bind = proddb.get_engine(bind='prod')

client = MongoClient('192.168.1.99', 27017)
database=client.get_database("analyze")
web_fundinfo_col=database.get_collection("web_fundinfo") #基金基本信息
web_fundinfo_col.create_index([("fundid", 1)], unique=True)
curfscode_col=database.get_collection("curfscode")#同系列基金
curfscode_col.create_index([("symbol",1)],unique=True)

class web_fundinfo(webdb.Model):
    '''基金基本信息'''
    fundid=webdb.Column(webdb.String,webdb.ForeignKey('web_fundotherinfo.fundid'),primary_key=True) #基金代码
    stockscale = webdb.Column(webdb.Float) #股票投资占净值比例
    bondcurscale=webdb.Column(webdb.Float) #债券及货币合计占净值比例
    curscale=webdb.Column(webdb.Float) #货币资金占净值比例
    otherscale=webdb.Column(webdb.Float) #其他投资占净值比例
    mholdingsrate=webdb.Column(webdb.Float) #十大重仓股比例
    mholdingbrate=webdb.Column(webdb.Float) #五大重仓债比例
    stocksize=webdb.Column(webdb.Float) #股票投资市值合计
    bondcursize=webdb.Column(webdb.Float) #债券及货币合计
    cursize=webdb.Column(webdb.Float) #货币资金合计
    othersize=webdb.Column(webdb.Float) #其他投资市值
    bondsize=webdb.Column(webdb.Float) #债券市值合计
    fundsize=webdb.Column(webdb.Float) #基金总资产
    invfundsize=webdb.Column(webdb.Float) #基金投资市值合计
    setupdate=webdb.Column(webdb.DateTime) #成立日期
    investgoal=webdb.Column(webdb.Text) #投资目标
    investrange=webdb.Column(webdb.Text) #投资范围
    investplot=webdb.Column(webdb.Text) #投资策略
    assignprinciple=webdb.Column(webdb.Text)#分配原则
    riskfeature=webdb.Column(webdb.Text) #风险收益特征
    nflag=webdb.Column() #净值披露方式标志(0净值 1份额收益)
    setupsize=webdb.Column(webdb.Float) #首募规模
    zxfe=webdb.Column(webdb.Float) #总份额
    ferq=webdb.Column() #最大变更日期
    zxgm=webdb.Column(webdb.Float) #募集规模
    gmrq=webdb.Column() #变更日期
    tgh=webdb.Column() #基金托管人名称
    yhpj=webdb.Column() #三年评级
    jjglf=webdb.Column() #费率费用上限
    jjtgf=webdb.Column()#费率费用上限
    content=webdb.Column() #基金亮点
    fundname=webdb.Column() #基金名称
    fundpy=webdb.Column() #基金名称首字母缩写
    ftype=webdb.Column() #基金分类
    type2=webdb.Column() #基金类型
    nav=webdb.Column(webdb.Float) #单位净值
    sumofnav=webdb.Column(webdb.Float) #单位累计净值
    navdate=webdb.Column() #净值日期
    risk=webdb.Column() #基金风险等级
    fundst=webdb.Column() #基金状态
    salestate=webdb.Column()#销售状态
    iswalletfund=webdb.Column() #是否钱包基金（0 否 1 是）
    isbfund=webdb.Column() #是否货币b类基金（0：否；1：是）
    similarrankm1=webdb.Column() #同类型排名(近1月)
    similarrankm3=webdb.Column()#同类型排名(近3月)
    similarrankm6=webdb.Column() #同类型排名(近6月)
    similarranky0=webdb.Column() #同类型排名(年初至今)
    similarranky1=webdb.Column() #同类型排名(近1年)
    similarranky3=webdb.Column() #同类型排名(近3年)
    similarranky5=webdb.Column() #同类型排名(近5年)
    isshortfinancefund=webdb.Column() #是否短期理财产品（0：否；1：是）
    dayrate=webdb.Column() #基金日增长率
    m1rate=webdb.Column() #最近1月净值增长率
    m3rate=webdb.Column() #最近3月净值增长率
    m6rate=webdb.Column() #最近6月净值增长率
    y1rate=webdb.Column() #最近1年净值增长率
    y3rate=webdb.Column() #最近3年净值增长率
    y5rate=webdb.Column() #最近5年净值增长率
    sumrate=webdb.Column() #上市至今净值增长率
    d7rate=webdb.Column()#最近1周净值增长率
    feerate=webdb.Column() #折后费率
    subfeerate=webdb.Column() #认购费率
    iplanst=webdb.Column() #定投状态 1.可以定投 0.不可定投
    managerid=webdb.Column() #基金经理代码
    managername=webdb.Column() #基金经理名称
    mdays=webdb.Column() #基金经理任职天数
    companyid=webdb.Column() #基金公司代码
    companyname=webdb.Column() #基金公司名称
    datatime=webdb.Column() #数据更新的系统时间
    y0rate=webdb.Column() #年初至今净值增长率
    industrysegments=webdb.Column() #行业板块
    investmenttheme=webdb.Column() #投资主题
    invsetmentstyle=webdb.Column() #投资风格（L-大 M-中 S-小）
    stockfspace=webdb.Column() #股票仓位(1-低 2-中 3-高)
    bondclassify=webdb.Column() #债券分类（1-一级 2-二级 3-纯债）
    speciallabel=webdb.Column() #特色标签(0无 1	量化基金 2	金牛奖基金 3	沪港深基金 4养老基金 5	逆向投资基金)
    buylimit=webdb.Column() #最大购买限额
    orgfeerate=webdb.Column() #原始费率
    fholder_rate=webdb.Column() #机构持仓占比
    minbuymoney=webdb.Column() #起购金额
    runperiod=webdb.Column() #封闭期


class web_fundotherinfo(webdb.Model):
    '''基金补充信息'''
    fundid=webdb.Column(webdb.String,primary_key=True) #基金代码
    assettype=webdb.Column() #资产类别
    location=webdb.Column()#投资地域
    managementstyle=webdb.Column() #管理方式
    structurestyle=webdb.Column() #组织形式
    exchangeplace=webdb.Column() #交易场所
    fundbenchmark1=webdb.Column()#适用基准
    guanlifeiyear=webdb.Column(webdb.Float)#年管理费
    tuoguanfeiyear=webdb.Column(webdb.Float)#年托管费
    xiaoshoufuwufeiyear=webdb.Column(webdb.Float) #年销售费
    zuigaoshengoufei=webdb.Column(webdb.Float)#最高申购费
    zuigaoshuhuifei=webdb.Column(webdb.Float)#最高赎回费
    investrate=webdb.Column(webdb.Float)#基金投资费率
    legalname=webdb.Column()#法定名称
    runmode=webdb.Column()#运行方式
    fundanalyzetype=webdb.Column()#基金分析类型：股票型、货币型、指数型、分级型
    custodianid=webdb.Column() #托管单位id
    custodianname=webdb.Column()#托管单位名称
    stockholdcount=webdb.Column()#持股数量
    stockholdcountdate=webdb.Column()#持股数量对应日期
    minpurchasevalue=webdb.Column()#最低申购金额
    betavalue=webdb.Column(webdb.Float)#贝塔值
    medianstockvalue=webdb.Column(webdb.Float)#持股流通市值中位数
    medianstockdate=webdb.Column()#持股流通市值中位数对应日期
    averagesurplusrate=webdb.Column(webdb.Float)#加权平均日盈率
    averagesurplusratedate=webdb.Column()#加权平均日盈率对应时间
    averagenetvalue=webdb.Column(webdb.Float)#加权平均市净值
    averagenetvaluedate=webdb.Column()#加权平均市净值对应时间
    standarddeviation=webdb.Column(webdb.Float)#标准差
    sharp=webdb.Column()#夏普比率
    stockturnoverrate=webdb.Column(webdb.Float)#股票资产换手率
    stockturnoverratedate=webdb.Column() #股票资产换手率对应时间
    sharetransfertype=webdb.Column()#份额结转方式
    bankdeposit=webdb.Column(webdb.Float)#银行存款
    bondrepofinane=webdb.Column() #债券回购融资
    floatingratenoteof397=webdb.Column() #剩余存续期超过397天的浮动利率债券
    assettypeofparent=webdb.Column() #资产类别（母基金）
    locationofparent=webdb.Column()#投资地域（母基金）
    managementstyleofparent=webdb.Column() #管理方式（母基金）
    setupdateofparent=webdb.Column() #成立时间（母基金）
    parentfundfollowindex=webdb.Column() #母基金跟踪指数
    parentfundid=webdb.Column() #母基金ID
    parentfundname=webdb.Column() #母基金名称
    zxfeofparent=webdb.Column() #母基金基金份额
    ferqofparent=webdb.Column() #母基金份额对应的日期
    typeafundid=webdb.Column() #A类基金id
    typeafundname=webdb.Column() #A类基金名称
    zxfeofatype=webdb.Column() #A类基金份额
    ferqofatype=webdb.Column() #A类基金份额对应的日期
    typebfundid=webdb.Column() #B类基金id
    typebfundname=webdb.Column() #B类基金名称
    zxfeofbtype=webdb.Column() #B类基金份额
    ferqofbtype=webdb.Column() #B类基金份额对应的日期
    y1sharprate=webdb.Column(webdb.Float) #一年净值夏普比
    y2sharprate=webdb.Column(webdb.Float) #2年净值夏普比
    y5sharprate=webdb.Column(webdb.Float) #5年净值夏普比
    y1netvolatility=webdb.Column(webdb.Float) #一年净值波动率
    y2netvolatility=webdb.Column(webdb.Float) #2年净值波动率
    y5netvolatility=webdb.Column(webdb.Float) #5年净值波动率
    fundoperatecost=webdb.Column(webdb.Float) #基金运营费
    institutionalrate=webdb.Column(webdb.Float) #机构投资者占比
    individualrate=webdb.Column(webdb.Float) #个人投资者占比
    sizestyle=webdb.Column() #市值风格
    valuationstyle=webdb.Column() #估值风格
    d1price=webdb.Column() #近一日价格
    d7price=webdb.Column() #近一周价格
    m1price=webdb.Column() #近一月价格
    m3price=webdb.Column() #近三月价格
    m6price=webdb.Column() #近六月价格
    y0price=webdb.Column() #今年以来价格
    y1price=webdb.Column() #近一年价格
    y3price=webdb.Column() #近三年价格
    y5price=webdb.Column() #近五年价格
    investmentdate=webdb.Column() #部分投资品种占基金资产净值比对应时间
    web_fundinfo = webdb.relationship("web_fundinfo", backref="web_fundotherinfo", uselist=False)


class datadict_columnvalue(webdb.Model):
    columnvalue = webdb.Column() #基金类型
    symbol = webdb.Column(webdb.String , primary_key =True  ) #基金代码
    fundtypes2 = webdb.Column() #基金类型编号


class curfscode(proddb.Model):
    __tablename__="p_curfscode"
    symbol=proddb.Column(proddb.String,primary_key=True)
    sname=proddb.Column()

    def __repr__(self):
        return json.dumps({"symbol":self.symbol,"sname":self.sname }, ensure_ascii=True, encoding="gbk", cls=MyJSONEncoder)

def query_columnvalue():
    sql_data=webdb.session.query(datadict_columnvalue).from_statement(webdb.text('''
      select b.columnvalue, t.symbol,t.FundTypes2
      from Datadict_ColumnValue@fin b
      join (select a.*,row_number() over(partition by a.symbol order by a.changedate desc) as rn 
      from FundTypes@fin a where a.FundTypes1 = '3') t
      on t.fundtypes2 = b.columncode
      and t.rn = 1
      where b.cid = 17795
    ''')).all()

    return sql_data


def query_curfscode():
    '''同类基金'''
    sql_data = proddb.session.query(curfscode).from_statement(webdb.text('''
          SELECT symbol,sname FROM P_CURFSCODE  where symbol!= symbol_comp
        ''')).all()
    return sql_data


def convert_to_dict(obj):
    '''把Object对象转换成Dict对象'''
    dict = {}
    dict.update(obj.__dict__)
    dict.pop("_sa_instance_state")
    return dict


def mongo_insert():
    datas = webdb.session.query(web_fundotherinfo).all()
    for data in datas:
        try:
            data.web_fundinfo
            data_dict = convert_to_dict(data)
            data_json = json.dumps(data_dict, ensure_ascii=False, encoding="gbk", cls=MyJSONEncoder)
            mongo_data = json.loads(data_json, encoding="gbk")

            _fundinfo = web_fundinfo_col.find_one({"fundid": data.fundid})
            if _fundinfo:
                web_fundinfo_col.delete_one({"fundid": data.fundid})

            web_fundinfo_col.insert_one(mongo_data)

        except Exception as e:
            print(e)


import re
def mongo_find():
    now1=datetime.datetime.now()
    datas=web_fundinfo_col.find(
        {
            "location":{ "$in":["中国大陆","大中华区","发达地区"] } , #投资地域
             "assettype": {"$in": ["债券"]},  #资产类别
            #  "managementstyle":{"$in":["非指数非量化"]}, #管理方式
            #  "structurestyle": {"$in": ["传统开放式"]}, #组织形式
             "exchangeplace":{"$in":["未上市"]}, #交易场所
             # "web_fundinfo.companyid":{"$in":["80053708"]} , #基金公司
            # "web_fundinfo.managerid": {"$in": [ re.compile("30072002")]},  # 基金经理
            # "web_fundinfo.fundst":{"$in":["0","1","2","6","7","8","b"]}, #交易状态
            # "web_fundinfo.tgh":{"$in":["中国银行股份有限公司"]} , #托管单位
            # "web_fundinfo.zxgm":{"$lte":47440318,"$gte":0} , #基金规模
            # "web_fundinfo.setupdate": {"$lte": "2015-06-12 00:00:00", "$gte": "2015-05-12 00:00:00"},  # 成立时间
            # "web_fundinfo.d7rate":{"$lte":0.000787,"$gte":0},# 净值回报率 近一周
            # "web_fundinfo.m1rate":{"$lte":0.000787,"$gte":0}, # 净值回报率 近一个月
            # "web_fundinfo.m3rate":{"$lte":0.000787,"$gte":0}, # 净值回报率 近三个月
            # "web_fundinfo.m6rate":{"$lte":0.000787,"$gte":0} , #净值回报率  近六个月
            # "web_fundinfo.y1rate":{"$lte":0.000787,"$gte":0},#净值回报率 近一年
            # "web_fundinfo.y3rate": {"$lte":0.000787,"$gte":0},  # 净值回报率 近三年
            # "web_fundinfo.y5rate": {"$lte":0.000787,"$gte":0},  # 净值回报率 近五年
            # "web_fundinfo.y1sharprate":{"$lte":0.000787,"$gte":0}, # 净值夏普比(年化) 近一年
            # "y2sharprate": {"$lte": 0.4 , "$gte": 0},  # 净值夏普比(年化) 近二年
            # "web_fundinfo.y5sharprate": {"$lte": 0.000787, "$gte": 0},  # 净值夏普比(年化) 近五年
            # "y1netvolatility":{"$lte": 22, "$gte": 0} , #净值标准差（年化）近一年
            # "y2netvolatility": {"$lte": 0.000787, "$gte": 0},#净值标准差（年化）近二年
            # "y5netvolatility": {"$lte": 0.000787, "$gte": 0} ,#净值标准差（年化）近五年
            # "fundoperatecost": {"$lte": 0.000787, "$gte": 0} ,# 运营费
            # "institutionalrate": {"$lte": 500, "$gte": 0},  # 机构投资者占比
            # "individualrate": {"$lte": 100, "$gte": 0},  # 个人投资者占比

             }).sort([("individualrate",1)])



    sizestyle_data={"giant":[],"broader":[],"middle":[],"small":[],"micro":[]} #giant=[] #巨盘broader=[] #大盘middle=[] #中盘small=[] #小盘micro=[] #微盘
    valuationstyle_data = {"value": [], "partialvalue": [], "equilibrium": [], "partialgrowth": [], "growth": []}# value=[] #价值;partialvalue=[] #偏价值equilibrium=[]  #均衡 partialgrowth=[] #偏成长;growth=[] #成长

    curfscodes = curfscode_col.find() #同系列基金
    curfscodes_all={}
    [ curfscodes_all.update({ data["symbol"]:data["sname"]}) for data in curfscodes]
    # datas_list=list(datas)
    # print(len(datas_list))
    for data in datas:
        print(data["individualrate"])
        if curfscodes_all.has_key(data["fundid"]):
            continue

        # _resultdata={"fundid":data["fundid"],"fundname":data["web_fundinfo"]["fundname"],"sizestyle":data["sizestyle"],"valuationstyle":data["valuationstyle"]}
        #
        # if data["sizestyle"] == "巨盘".decode("utf-8"):
        #     sizestyle_data["giant"].append(_resultdata)
        # elif data["sizestyle"] == "大盘".decode("utf-8"):
        #     sizestyle_data["broader"].append(_resultdata)
        # elif data["sizestyle"] == "中盘".decode("utf-8"):
        #     sizestyle_data["middle"].append(_resultdata)
        # elif data["sizestyle"] == "小盘".decode("utf-8"):
        #     sizestyle_data["small"].append(_resultdata)
        # elif data["sizestyle"] == "微盘".decode("utf-8"):
        #     sizestyle_data["micro"].append(_resultdata)

    # print(len(datas_list))

    # valuationstyle_data["value"]=[val["valuationstyle"] for val in sizestyle_data["small"] if
    #                               val["valuationstyle"] == "价值".decode("utf-8")]


    # print(sizestyle_data)
    print(datetime.datetime.now() - now1)
    return datas


from  bson.json_util  import  loads ,dumps,SON

def mongo_curfscode_insert():
    datas=query_curfscode()
    data_bson = dumps(datas, ensure_ascii=False, encoding="gbk", cls=MyJSONEncoder)
    data_listdict=loads(data_bson,encoding="utf-8")
    for _val in data_listdict:
        curfscode_col.insert_one(_val)

    # for _data in datas:
    #     _data_dict=json.loads(
    #         json.dumps(convert_to_dict(_data),encoding="gbk",ensure_ascii=False,cls=MyJSONEncoder)
    #         ,encoding="gbk")
    #     curfscode_col.insert_one(_data_dict)



if "__main__" == __name__ :
    mongo_find()

