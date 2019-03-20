# -*- coding: utf-8 -*-
# @Time    : 2018/12/26 9:07
# @Author  : dodo8619
# @Email   : lj16888619@gmail.com
# @File    : analyze_db.py

#基金分析工具，生成json

# import cx_Oracle as cx
# conn = cx.connect('cl_fof/cl_fof@192.168.1.242:1521/oru1')
# cursor = conn.cursor ()
# cursor.execute ("select * from ofof_agent")
# row = cursor.fetchone ()
# print (row)
# cursor.close ()
# conn.close ()

from flask_sqlalchemy import SQLAlchemy
from flask import Flask

import json
import decimal,datetime

class MyJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        if isinstance(o, datetime.datetime):
            return datetime.datetime.strftime(o,"%Y-%m-%d %H:%M:%S")
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
fofdb = SQLAlchemy(flask)
fofdb.session.bind = fofdb.get_engine(bind='fof')
dcdb = SQLAlchemy(flask)
dcdb.session.bind = dcdb.get_engine(bind='dc')
proddb = SQLAlchemy(flask)
proddb.session.bind = proddb.get_engine(bind='prod')



def investment10000():
    stmt=webdb.text('''
     select 
        A.FUNDID
        from WEB_FUNDINFO A,WEB_FUNDOTHERINFO B 
        where A.FUNDID = B.FUNDID(+) 
    ''')
    datas=webdb.get_engine(bind='web').execute(stmt).fetchall() #市场所有基金
    for d in datas:
        datas={"Invest10000":None,"TrackingError":None}
        invst10000_data=queryInvst10000(d.fundid)
        ncurachieve_enddata=queryNcurachieve(d.fundid)

        datas["Invest10000"]=invst10000_data
        datas["TrackingError"] = ncurachieve_enddata
        datas_json=json.dumps(datas,cls=MyJSONEncoder)
        with open('fund_detail_%s.js' % (d.fundid) , 'w') as f:
            f.write(datas_json)

        print(datas_json)


def queryInvst10000(fundid):
    '''万元投资'''
    try:
        from analyze_modle import ofof_fund_archives
        invst10000_result = {"benchmark": [], "date": [], "enddate": [], "nav": [], "startdate": None, "enddate": None}
        invst10000s = fofdb.session.query(ofof_fund_archives).filter_by(fundid=fundid).all()  # 万元投资
        invst10000s_dictlist = [dict(zip(result.keys(), result)) for result in invst10000s]

        for _invst in invst10000s_dictlist:
            invst10000_result["benchmark"].append(float(_invst["fundbdy2"]))
            invst10000_result["nav"].append(float(_invst["nav2"]))
            invst10000_result["date"].append(_invst["ttime"])

        invst10000_result["startdate"] = invst10000s_dictlist[0]["tdate"]
        invst10000_result["enddate"] = invst10000s_dictlist[len(invst10000s_dictlist) - 1]["tdate"]
        # invst10000_data = json.dumps(invst10000_result, cls=MyJSONEncoder)
    except Exception as e:
        print(e.message)
    return invst10000_result

def queryNcurachieve(fundid):
    '''跟踪误差'''
    try:
        # ncurachieve_data = proddb.get_engine(bind="prod").execute(proddb.text('''
        #                         select fundid,to_char(enddate, 'yyyy-mm-dd') as enddate,
        #                         nvl(to_char(round( TRACEERRORFDY1 *100 ,4),'fm9999999990.0000'),'0') AS encurnav_064,
        #                         ((to_date(to_char(enddate, 'yyyy-mm-dd'), 'yyyy-MM-dd') - to_date('1970-01-01', 'yyyy-mm-dd')) * 24 * 60 * 60 * 1000) as time
        #                         from P_NCURACHIEVE T
        #                         where to_date(to_char(enddate,'yyyy-mm-dd'),'yyyy-mm-dd') <=sysdate and to_date(to_char(enddate,'yyyy-mm-dd'),'yyyy-mm-dd') >= ADD_MONTHS(sysdate, -18)
        #                         and FUNDID=:fundid
        #                         ORDER BY T.ENDDATE
        #                         '''), fundid=fundid
        # ).fetchall()

        from analyze_modle import p_ncurachieve
        ncurachieve_data =proddb.session.query(p_ncurachieve).from_statement(proddb.text('''
            select fundid,to_char(enddate, 'yyyy-mm-dd') as enddate,
            nvl(to_char(round( TRACEERRORFDY1 *100 ,4),'fm9999999990.0000'),'0') AS encurnav_064,
            ((to_date(to_char(enddate, 'yyyy-mm-dd'), 'yyyy-MM-dd') - to_date('1970-01-01', 'yyyy-mm-dd')) * 24 * 60 * 60 * 1000) as time
            from P_NCURACHIEVE T
            where to_date(to_char(enddate,'yyyy-mm-dd'),'yyyy-mm-dd') <=sysdate and to_date(to_char(enddate,'yyyy-mm-dd'),'yyyy-mm-dd') >= ADD_MONTHS(sysdate, -18)
            and FUNDID=:fundid
            ORDER BY T.ENDDATE
        ''')).params({"fundid":fundid}).all()
        ncurachieve_dictdata = [dict(zip(ncur.keys(), ncur)) for ncur in ncurachieve_data]
        ncurachieve_result = {"date": [], "value": [], "startdate": None, "enddate": None}
        for _ncur in ncurachieve_dictdata:
            ncurachieve_result["date"].append(_ncur["time"])
            ncurachieve_result["value"].append(_ncur["encurnav_064"])
            ncurachieve_result["startdate"] = ncurachieve_dictdata[0]["enddate"]
            ncurachieve_result["enddate"] = ncurachieve_dictdata[len(ncurachieve_dictdata) - 1]["enddate"]

        # ncurachieve_enddata = json.dumps(ncurachieve_result, cls=MyJSONEncoder)
    except Exception as e:
        print(e.message)

    return ncurachieve_result


def bondAllocation(fundid):
    '''券种配置（最近券种配置/历史券种配置）'''
    bond_allocation_data = fofdb.get_engine(bind="fof").execute(fofdb.text(''' 
    select fundid,
    to_char(to_date(enddate,'yyyy-mm-dd'),'yyyy-mm-dd') as enddate,
    substr(enddate, 0, 4) as year,
    ((to_date(enddate, 'yyyy-MM-dd') -to_date('1970-01-01', 'yyyy-mm-dd')) * 24 * 60 * 60 *1000) as time,
    (case substr(enddate, 5, 2) when '12' then 'fourthquarter'  when '09' then 'thirdquarter' when '06' then 'secondquarter' when '03' then 'firstquarter' else ''  end) as enddate_quarter,
    to_char( round(Treasury, 2),'fm9999999990.00') as Treasury,
    to_char(
    round(Central_bank_bills, 2),'fm9999999990.00') as
    Central_bank_bills,
    to_char( round(Financial_debt, 2),'fm9999999990.00') as
    Financial_debt,
    to_char( round(Corporate_bonds, 2),'fm9999999990.00')
    as
    Corporate_bonds,
    to_char( round(Short_melt, 2),'fm9999999990.00') as
    Short_melt,
    to_char( round(Medium_note, 2),'fm9999999990.00') as
    Medium_note,
    to_char( round(Convertible_bonds, 2),'fm9999999990.00') as
    Convertible_bonds,
    to_char( round(other, 2),'fm9999999990.00') as other
    from RESTEST_bond_allocation
    where fundid = :fundid
    order by enddate desc
    '''), fundid=fundid
    ).fetchall()
    bond_allocation_data = [dict(zip(bond.keys(), bond)) for bond in bond_allocation_data]
    bond_result = {"中期票据": [], "企业债": [], "其他": [], "可转债": [], "国债": [], "央行票据": [], "短融": [], "金融债": [],"date":[]}
    for _bond in bond_allocation_data:
        bond_result["国债"].append(_bond["treasury"])
        bond_result["央行票据"].append(_bond["central_bank_bills"])
        bond_result["金融债"].append(_bond["financial_debt"])
        bond_result["企业债"].append(_bond["corporate_bonds"])
        bond_result["短融"].append(_bond["short_melt"])
        bond_result["中期票据"].append(_bond["medium_note"])
        bond_result["可转债"].append(_bond["convertible_bonds"])
        bond_result["其他"].append(_bond["other"])
        bond_result["date"].append(_bond["time"])

    #最新一期
    _latest_bond=bond_allocation_data[len(bond_allocation_data)-1]
    latest_bond_type_allocation={"key":["国债", "央行票据", "金融债", "企业债", "短融", "中期票据", "可转债", "其他"],"value":[]}
    for _val in ["treasury","central_bank_bills","financial_debt","corporate_bonds","short_melt","medium_note","convertible_bonds","other"] :
        latest_bond_type_allocation["value"].append(_latest_bond[_val])

    result={"BOND_TYPE_ALLOCATION":bond_result,"LATEST_BOND_TYPE_ALLOCATION":latest_bond_type_allocation}
    return result


def assetAllocationChart(fundid):
    '''资产配置(最近资产配置/历史资产配置)'''
    asset_allocation_data = fofdb.get_engine(bind="fof").execute(fofdb.text(''' 
        select FUNDID,
		to_char(to_date(enddate,'yyyy-mm-dd'),'yyyy-mm-dd') as enddate,
		to_char( round(stock,2),'fm9999999990.00') as stock,
		to_char(round(bond,2),'fm9999999990.00') as bond,
		to_char(round(cash,2),'fm9999999990.00') as cash,
		to_char( round(Derivative,2),'fm9999999990.00') as Derivative,
		to_char( round(other,2) ,'fm9999999990.00') as other,
        substr(enddate, 0, 4) as year,
        ((to_date(enddate, 'yyyy-MM-dd') -to_date('1970-01-01','yyyy-mm-dd')) * 24 * 60 * 60 * 1000) as time,
        (case substr(enddate,5,2)
        when '12' then 'fourthquarter'
        when '09' then 'thirdquarter'
        when '06' then 'secondquarter'
        when '03'
        then 'firstquarter'
        else substr(enddate,5,2)
        end
        ) as enddate_zw
        from
        RESTEST_asset_allocation
          where fundid=:fundid
        order by enddate desc
        '''), fundid=fundid).fetchall()

    asset_allocation_data = [dict(zip(bond.keys(), bond)) for bond in asset_allocation_data]
    his_asset_allocation_resp={"债券":[],"其他":[],"现金":[],"股票":[],"衍生品":[],"date":[]}
    his_annual_allocation_resp={"key":["股票", "债券", "现金", "衍生品", "其他"],"value":[]}
    for _asset in asset_allocation_data:
        his_asset_allocation_resp["股票"].append(_asset["stock"])
        his_asset_allocation_resp["债券"].append(_asset["bond"])
        his_asset_allocation_resp["现金"].append(_asset["cash"])
        his_asset_allocation_resp["衍生品"].append(_asset["derivative"])
        his_asset_allocation_resp["其他"].append(_asset["other"])
        his_asset_allocation_resp["date"].append(_asset["time"])

    _last_asset=asset_allocation_data[len(asset_allocation_data)-1]
    his_annual_allocation_resp["value"].append(_last_asset["stock"])
    his_annual_allocation_resp["value"].append(_last_asset["bond"])
    his_annual_allocation_resp["value"].append(_last_asset["cash"])
    his_annual_allocation_resp["value"].append(_last_asset["derivative"])
    his_annual_allocation_resp["value"].append(_last_asset["other"])

    result={"HIS_ANNUAL_ALLOCATION":his_asset_allocation_resp,"HIS_ASSET_ALLOCATION":his_annual_allocation_resp} #最近资产，历史资产
    return result

def historyInTubeAssets(fundid):
    '''历史在管资产'''
    assetal_data = fofdb.get_engine(bind="fof").execute(fofdb.text(''' 
        SELECT T.fundid as fundid,T.enddate,substr(T.enddate, 0, 4) as year,
        ((to_date(T.enddate, 'yyyy-MM-dd') -to_date('1970-01-01',
        'yyyy-mm-dd')) * 24 * 60 * 60 *
        1000) as time,
        (case substr(T.enddate,
        5, 2)
        when '12' then
        'fourthquarter'
        when '09' then
        'thirdquarter'
        when '06' then
        'secondquarter'
        when
        '03' then
        'firstquarter'
        else
        ''
        end) as enddate_quarter,
        to_char(
        round(T.AssetAL/100000000,2),'fm9999999990.00') as AssetAL,
        to_char(
        round(T.mean_AssetAL/100000000,2),'fm9999999990.00') as
        mean_AssetAL,
        to_char( round( T.median_AssetAL/100000000,2),'fm9999999990.00') as
        median_AssetAL
        FROM RESTEST_AssetAL T
         where T.fundid =:fundid
        order by T.enddate desc
            '''), fundid=fundid).fetchall()

    assetal_dictdata = [dict(zip(assetal.keys(), assetal)) for assetal in assetal_data]
    his_charging_asset = {"asset": [], "avg": [], "date": [], "median": []}
    for _assetal in assetal_dictdata:
        his_charging_asset["asset"].append(_assetal["asset"])
        his_charging_asset["avg"].append(_assetal["mean_assetal"])
        his_charging_asset["median"].append(_assetal["median_assetal"])
        his_charging_asset["date"].append(_assetal["time"])

    return his_charging_asset


def qureyExcessReturnList(fundid):
    '''基金净值季度超额回报分布 '''
    '''历史在管资产'''
    excess_return_data = fofdb.get_engine(bind="fof").execute(fofdb.text('''
        select FUNDID,
        begin_quarter,
        substr(begin_quarter, 0, 4) as
        begin_quarter_year,
        to_char(to_date(to_char(begin_quarter),'yyyy-mm'),'yyyy-mm') as begin_quarter_jd,
        end_quarter,
        substr(end_quarter, 0, 4) as end_quarter_year,
         to_char(to_date(to_char(end_quarter),'yyyy-mm'),'yyyy-mm') as end_quarter_jd,
        para1,
        para2,
        para3,
        para4,
        para5,
        para6,
        para7,
        para8,
        para9,
        para10,
        para11,
        para12
        from RESTEST_excess_return
       where fundid=:fundid
        '''), fundid=fundid).first()
    excess_dictdata = dict(zip(excess_return_data.keys(), excess_return_data))
    fund_alpha_diagram={"key":["低于-15", "-15--12", "-12--9", "-9--6", "-6--3", "-3-0", "0-3", "3-6", "6-9", "9-12", "12-15", "高于15"],"value":[]}
    for val in ["para1","para2","para3","para4","para5","para6","para7","para8","para9","para10","para11","para12"]:
        fund_alpha_diagram["value"].append(excess_dictdata[val])

    return fund_alpha_diagram

def qureyValueStyleList(fundid):
    '''股票资产估值风格(最近股票资产/历史股票资产)'''
    sql_data = fofdb.get_engine(bind="fof").execute(fofdb.text('''
    select FUNDID ,
    to_char(to_date(enddate, 'yyyy-mm-dd'), 'yyyy-mm-dd')
    as enddate,
    to_char(round(occupy1*100,2),'fm9999999990.00') as occupy1,
    to_char(round( occupy2*100 ,2),'fm9999999990.00') as occupy2,
    to_char(round( occupy3*100 ,2),'fm9999999990.00') as occupy3,
    to_char(round( occupy4*100 ,2),'fm9999999990.00') as occupy4,
    to_char(round( occupy5*100 ,2),'fm9999999990.00') as occupy5,
    substr(enddate, 0, 4) as year,
    (case substr(enddate, 5, 2)
    when '12'
    then
    'fourthquarter'
    when '06' then
    'secondquarter'
    else
    ''
    end) as enddate_zw,
    ((to_date(enddate,
    'yyyy-MM-dd') -to_date('1970-01-01', 'yyyy-mm-dd')) * 24 * 60 * 60 *
    1000) as time
    from RESTEST_value_style
    where FUNDID= :fundid
    order by enddate desc
    '''), fundid=fundid).fetchall()
    sql_dictdata =[ dict(zip(data.keys(), data)) for data in sql_data]

    his_stock_asset_value_style = {"growing": [], "mixing": [], "partialgrowing": [], "partialvalue": [], "value": [],
                                   "date": []}
    for d in sql_dictdata:
        his_stock_asset_value_style["growing"].append(d["occupy1"])
        his_stock_asset_value_style["partialgrowing"].append(d["occupy2"])
        his_stock_asset_value_style["mixing"].append(d["occupy3"])
        his_stock_asset_value_style["partialvalue"].append(d["occupy4"])
        his_stock_asset_value_style["value"].append(d["occupy5"])
        his_stock_asset_value_style["date"].append(d["time"])


    _last_data=sql_dictdata[len(sql_dictdata)-1]
    latest_stock_asset_value_style = {"key": ["成长", "偏成长", "均衡", "偏价值", "价值"], "value": []}
    for val in ["occupy1","occupy2","occupy3","occupy4","occupy5"]:
        latest_stock_asset_value_style["value"].append(_last_data[str(val)])

    result={"LATEST_STOCK_ASSET_VALUE_STYLE":latest_stock_asset_value_style,"HIS_STOCK_ASSET_VALUE_STYLE":his_stock_asset_value_style}
    return result


#最近股票投资行业配置

if "__main__" == __name__:
    queryNcurachieve('000001')