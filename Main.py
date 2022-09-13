import streamlit as st
#import streamlit_echarts
import basicData
import dataToPD
import toChart
#这是整个程序主要的部分，用于将网页分成左右两部分，左侧可以根据输入的名字，查询相应的学生成绩分析
# streamlit run Main.py
st.set_page_config(layout="wide")   #设置屏幕展开方式，宽屏模式布局更好
st.title('成绩分析报表')  #网页标题是 成绩分析报表

title = st.sidebar.text_input(label='请输入', value='刘备', max_chars=15)  # 用st.sidebar.在侧边栏加入搜索框，title返回搜索的值
#在侧边栏加入要 区别展示的部分
add_selectbox = st.sidebar.radio(
    "请选择要展示的部分",
    (basicData.coures6List)
)
#st.write(add_selectbox)             #主页面显示点击的学科
toChart.stuClassRanking(title)  # 绘制排名图表

#班级人数统计在侧边栏
classNumberChar = toChart.toBarChart(title)
st.sidebar.altair_chart(classNumberChar, use_container_width=True)


#年级全部人数的平均值
st.write('年级全部数据')
toChart.avgData(stuName=title, courseName=add_selectbox)


#年级前XX名的数据
st.write('年级前'+str(basicData.vipCount)+'名数据')
toChart.avgData(stuName=title, courseName=add_selectbox, vip=True)


#年级前150的折线图
st.write('年级前'+str(basicData.vipCount)+'名的折线图')
toChart.line_base(add_selectbox)

#学科的线形图
st.write('学生所处位置')
dfCourseRank = dataToPD.getAllCourseRanking()                    #班级 姓名 学科成绩 学科排名
dataCourseRankingDf = dataToPD.getTheCourseRank(dfCourseRank, add_selectbox)
toChart.toChartTheCourse(dataCourseRankingDf, add_selectbox, title)



