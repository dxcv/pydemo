# -*- coding: utf-8 -*-
# @Time    : 2018/12/27 9:13
# @Author  : dodo8619
# @Email   : lj16888619@gmail.com
# @File    : analyze_modle.py

from analyze_db import db,webdb ,fofdb,dcdb,proddb

ofof_fund_archives=fofdb.Table('ofof_fund_archives',
                         fofdb.Column('fundid'), #基金代码
                         fofdb.Column('nav2'), #复权净值*10000
                         fofdb.Column('tdate'), #净值日期
                         fofdb.Column('fundbdy2'),#基准值
                         fofdb.Column('ttime'), #毫秒时间
                         )

p_ncurachieve=proddb.Table('p_ncurachieve',
                           proddb.Column('fundid'),  # 基金代码
                           proddb.Column('enddate'),  #截止日期 ENDDATE
                           proddb.Column('encurnav_064'),  #日跟踪误差_指数基金(近1年)
                           proddb.Column('time'),  #截止日期 ENDDATE
)


