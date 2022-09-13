from pandas import DataFrame

import dataToPD
import pandas as pd
import numpy as np
import altair as alt
import streamlit as st
import basicData
import streamlit as st
import toChart

import streamlit_echarts
import pyecharts.options as opts
from pyecharts.charts import Line
import streamlit.components.v1 as components        #将要展示的 弄成html

path = './excelData/二模成绩.xlsx'
courseName = '数学'
dfNum = dataToPD.rankSum(courseName=courseName)
attr = dfNum[1]                                 #x轴的列表
c = Line().add_xaxis(attr).set_global_opts(
        title_opts=opts.TitleOpts(title="", subtitle=""),
        tooltip_opts=opts.TooltipOpts(trigger="axis"),toolbox_opts=opts.ToolboxOpts(is_show=False),
       )
    #c.set_global_opts(opts.InitOpts(width='900px', height='1200px')
        #axispointer_opts=opts.AxisTickOpts(is_show= True),
c.height = '800px'                                                           #注意要先设置好这个图，然后再添加数据
for row in dfNum[0].iterrows():                 #遍历dataframe
    rowAllList = row[1].tolist()
    className = str(int(rowAllList[0]))+'班'                 #str(int(rowAllList[0]))+'班'是 1-10班
    rowData = rowAllList[1:]                    #选取除了第1个元素之外的其他元素，因为rowAllList[0]是班级
    c.add_yaxis(series_name=className, y_axis=rowData, label_opts=opts.LabelOpts(is_show=True))
    #c.render()
    #container = st.container()
    #container= st.set_global_opts(opts.InitOpts(width='900px', height='500px'))
    #container.write(

print(c.render_embed())
streamlit_echarts.st_pyecharts(c)

#line = line_base()
# #line.show_config()
# streamlit_echarts.st_pyecharts(
#             line
#         )
# streamlit run test.py

# from vega_datasets import data
#
# source = data.wheat()
# print(source)