# 利用pyecharts将数据转化为图表 并显示的文件
from pyecharts.charts import Bar
import streamlit_echarts
from pyecharts import options as opts
import dataToPD
import streamlit as st
import altair as alt
from pyecharts.charts import Line
import streamlit.components.v1 as components        #将要展示的 弄成html

@st.cache(persist=True)                             #缓存，提高速度
def stuNameIsIn(stuName):
    dfBase = dataToPD.getBaseDf()
    nameList = dfBase['姓名'].values.tolist()  # 将姓名列转化成列表
    if stuName in nameList:
        return True
    else:
        return False


def toBarChart(stuName):
    dfBase = dataToPD.getBaseDf()
    x = '班级'
    dfData = dataToPD.getClassStuCount()
    classNameList = dfData['班级'].tolist()  # 班级名称列表
    if stuNameIsIn(stuName):
        stuClass = str(int(dfBase.loc[dfBase['姓名'] == stuName, x].values))  # 获取查找的stuName这位学生的班级
        stuClassStr = stuClass + '班'
        #st.write(stuClassStr + stuName)
        colorPara = alt.condition(
            alt.datum[x] == stuClassStr,  # 此处字符串判断是否相同
            alt.value('red'),  # 若符合条件，显示这个颜色
            alt.value('steelblue')  # 若不符合条件 则显示这个颜色
        )
        altairClass = alt.Chart(dfData).mark_bar().encode(
            x=alt.X('班级', sort=classNameList),  # x轴是班级，同时排序的时候强制按1-10班进行排序
            y='人数',
            color=colorPara
        ).properties(title='班级人数统计')
        text = alt.Chart(dfData).mark_text(
            align='center',
            baseline='top',
            color='white'
        ).encode(
            x=alt.X('班级', sort=classNameList),  # x轴是班级，同时排序的时候强制按1-10班进行排序
            y='人数',
            text=alt.Text(
                '人数:Q', )
        )
        # kfd = alt.layer(altairClass, text).interactive()
        kfd = altairClass + text
        altairClass = kfd.configure_axisX(labelAngle=0)  # 标签旋转角度，保证x轴标签横向显示 必须在结合之后统一改

    else:
        altairClass = alt.Chart(dfData).mark_bar().encode(
            x=alt.X('班级', sort=classNameList),  # x轴是班级，同时排序的时候强制按1-10班进行排序
            y='人数').properties(title='班级人数统计')
        text = alt.Chart(dfData).mark_text(
            align='center',
            baseline='top',
            color='white'
        ).encode(
            x=alt.X('班级', sort=classNameList),  # x轴是班级，同时排序的时候强制按1-10班进行排序
            y='人数',
            text=alt.Text(
                '人数:Q', )
        )
        kfd = altairClass + text
        altairClass = kfd.configure_axisX(labelAngle=0)  # 标签旋转角度，保证x轴标签横向显示 必须在结合之后统一改
    return altairClass


def stuClassRanking(stuName):
    if stuNameIsIn(stuName):
        bar = Bar()
        bar.add_xaxis(dataToPD.getStuAllRank(stuName)[0])
        bar.add_yaxis(stuName + ' 年级排名', dataToPD.getStuAllRank(stuName)[1])
        bar.set_global_opts(yaxis_opts=opts.AxisOpts(is_inverse=True))  # 反转y轴，y轴改为自上而下依此增大
        bar.set_global_opts(xaxis_opts=opts.AxisOpts(position="top"))  # 设置x轴的位置在顶部
        bar.set_global_opts(opts.InitOpts(width='900px', height='500px'))
        bar.set_series_opts(opts.LabelOpts(position="insideBottom"))  # 设置数据标签的位置在条形的底部
        streamlit_echarts.st_pyecharts(
            bar
        )
    else:
        pass
    return


def toChartTheCourse(dfData, courseName, stuName):
    # 将姓名 班级 学科 学科排名 转化为带状图
    x = courseName + '排名'
    if stuNameIsIn(stuName):
        rankValue = int(dfData.loc[dfData['姓名'] == stuName, x].values)  # 获取要查询的学生的某学科排名
        colorPara = alt.condition(  # 显示图形的特点
            alt.datum[x] - rankValue,  # 此处不能用== 必须用-=0这种写法；来判断是否有这个值
            alt.value('blue'),  # 若符合条件，显示这个颜色
            alt.value('red')  # 若不符合条件 则显示这个颜色
        )

        altChart = alt.Chart(dfData).mark_tick().encode(
            alt.X(x + ':Q'),
            alt.Y('班级', scale=alt.Scale(domain=(0, 11))),  # 班级配置，由1到10班 但刻度由0-11
            color=colorPara
        )
    else:
        altChart = alt.Chart(dfData).mark_tick().encode(
            alt.X(x + ':Q'),  # encode编码的 :Q指定为数值的数据类型
            alt.Y('班级', scale=alt.Scale(domain=(0, 11))),  # 班级配置，由1到10班 但刻度由0-11
        )
        altChart = altChart.configure_mark(
            color='blue'  # opacity=0.2,   不透明度
        )
    return st.altair_chart(altChart, use_container_width=True)



def avgData(stuName, courseName,vip=False):                     #学科均分的柱状图
    dfBase = dataToPD.getBaseDf()
    x = '班级'
    if vip:
        groupXX = dataToPD.getTheCourseAvg(courseName, choose=True)
    else:
        groupXX = dataToPD.getTheCourseAvg(courseName)
    #dfData = dataToPD.getClassStuCount()
    sortList = list(groupXX[x])
    if stuNameIsIn(stuName):
        stuClass = str(int(dfBase.loc[dfBase['姓名'] == stuName, x].values))  # 获取查找的stuName这位学生的班级
        stuClassStr = stuClass + '班'
        colorPara = alt.condition(
            alt.datum[x] == stuClassStr,  # 此处字符串判断是否相同
            alt.value('orange'),  # 若符合条件，显示这个颜色
            alt.value('steelblue')  # 若不符合条件 则显示这个颜色
        )
        altairClass = alt.Chart(groupXX).mark_bar(size=30).encode(
            #x=alt.X('班级', sort=dataToPD.couresList),  # x轴是班级，同时排序的时候强制按1-10班进行排序
            x=alt.X('班级', sort=sortList),             # x轴是班级，同时排序的时候强制按班级平均分从高到低
            y=courseName + '均分',
            color=colorPara
        ).properties(title=courseName + ' 均分')

        text = alt.Chart(groupXX).mark_text(
            align='center',
            baseline='top',
            color='white'
        ).encode(
            #x=alt.X('班级', sort=dataToPD.couresList),  # x轴是班级，同时排序的时候强制按1-10班进行排序
            x=alt.X('班级', sort=sortList),              # x轴是班级，同时排序的时候强制按班级平均分从高到低
            y=courseName + '均分',
            text=alt.Text(
                courseName + '均分' + ':Q',
                format='.1f')
        )
        kfd = altairClass + text
        kfd = kfd.configure_axisX(labelAngle=0)  # 标签旋转角度，保证x轴标签横向显示 必须在结合之后统一改
        st.altair_chart(kfd, use_container_width=True)
    else:
        altairClass = alt.Chart(groupXX, mark=True).mark_bar(size=30).encode(
            x=alt.X('班级', sort=sortList),  # x轴是班级，同时排序的时候强制按班级平均分从高到低
            y=courseName + '均分').properties(title=courseName + ' 均分')
        text = altairClass.mark_text(
            align='center',
            baseline='top',
            color='white'
        ).encode(
            text=alt.Text(
                courseName + '均分' + ':Q',
                format='.1f')
        )
        kfd = alt.layer(altairClass, text).interactive()
        kfd = kfd.configure_axisX(labelAngle=0)  # 标签旋转角度，保证x轴标签横向显示 必须在结合之后统一改
        st.altair_chart(kfd, use_container_width=True)

    return


def line_base(courseName):                                      #某学科 多少名之前的趋势
    dfNum = dataToPD.rankSum(courseName=courseName)
    attr = dfNum[1]                                 #x轴的列表
    c = Line().add_xaxis(attr).set_global_opts(
        title_opts=opts.TitleOpts(title="", subtitle=""),
        tooltip_opts=opts.TooltipOpts(trigger="axis"),toolbox_opts=opts.ToolboxOpts(is_show=False),
       )
    c.height = '600px'                              #设置高度
    c.width = '1300px'                              #设置宽度
    #c.set_global_opts(opts.InitOpts(width='900px', height='1200px')
        #axispointer_opts=opts.AxisTickOpts(is_show= True),
                                                           #注意要先设置好这个图，然后再添加数据
    for row in dfNum[0].iterrows():                 #遍历dataframe
        rowAllList = row[1].tolist()
        className = str(int(rowAllList[0]))+'班'                 #str(int(rowAllList[0]))+'班'是 1-10班
        rowData = rowAllList[1:]                    #选取除了第1个元素之外的其他元素，因为rowAllList[0]是班级
        c.add_yaxis(series_name=className, y_axis=rowData, label_opts=opts.LabelOpts(is_show=True))

    cHtml = c.render_embed()                    #将图表渲染成html的文本文件
    components.html(cHtml,height=700,width=1400)          #在主页面用streamlit静态组件的方式渲染pyecharts

    return
