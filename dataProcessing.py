import basicData
import pandas as pd

'''此文件专门用于数据处理，获得各种图表的原始dataframe或list等数据
'''


class GetDF:
    def __init__(self):
        self.excelFileDf = pd.DataFrame(pd.read_excel(basicData.excelFilePath))  # 传入参数：原始excel的dataframe文件

    def getClassStuCountDF(self):           #获取班级及班级人数的数据
        dfClass = self.excelFileDf['班级'].value_counts()  # 获取班级中各元素出现的次数
        dfClass = pd.DataFrame({'班级': dfClass.index, '人数': dfClass.values}).sort_values(by='班级',
                                       ascending=True)  # 用获取的Series的 index和value重新构造dataframe  # 用班级列进行排序
        dfClass['班级'] = dfClass['班级'].astype(str)  # 将班级列转化为str字符串
        dfClass['班级'] = dfClass['班级'] + '班'  # 在班级列的名称后面加"班"成为x班
        return dfClass

    def getTheStuResults(self, stuName, courseList=basicData.coures8List):  # 获取指定学生各科成绩
        allTable = self.excelFileDf  # 获得所有表格
        stuTable = allTable.loc[allTable['姓名'] == stuName]  # 选取姓名为所选姓名的整行
        stuTableResult = stuTable[courseList]  # 删除班级 姓名列
        return stuTableResult

    def getAllCourseRanking(self, courseList=basicData.coures8List):  # 获取所有成绩和所有学科排名 # 班级 姓名 各科分数 各科排名，按总分进行排名的df
        dfFormPath = self.excelFileDf
        for i in courseList:
            dfFormPath = dfFormPath.sort_values(by=i, ascending=False)  # 按本学科进行排名，得到新的表格
            dfFormPath = dfFormPath.reset_index(drop=True)  # 索引按总分排名重新布置
            newColTitle = i + '排名'
            dfFormPath[newColTitle] = dfFormPath.index + 1  # 添加科目排名列，名次按index+1来算
            dfFormPath[newColTitle] = dfFormPath[newColTitle].astype(int)  # 将排名数据类型都转化为整整数类型
        return dfFormPath  # 得到的数据表包括了所有学科的成绩和排名

    def getStuAllRank(self, stuName, rankList=basicData.ranking8List):            #获取各科排名的数值
        rankList.insert(0, '姓名')
        dfData = self.getAllCourseRanking()[rankList]
        getData = dfData.loc[dfData['姓名'] == stuName]       # 获取姓名是要查找的详细数据
        rankList.remove('姓名')
        getDataGet = getData[rankList]                # 获取各科排名
        return rankList, getDataGet.values.tolist()[0]                # 获取各科排名的名称和排名数值列表，通过列表的[0][1]获取

    def getRadarTable(self, stuName):  # 获取学生、总均分、前150均分、最高分的dataframe
        dfFormPath = self.excelFileDf
        mean_df = dfFormPath.drop(labels=['班级'], axis=1).mean(numeric_only=True)  # 获取各科总分均值round(0),只有数值列执行均值操作
        mean_df = pd.DataFrame(mean_df).round(1)
        mean_df['index'] = mean_df.index  # 将索引转换为列
        mean_df.columns = ['总均分', '学科']  # 将dataframe的列名 重新命名

        data150 = dfFormPath.sort_values(by='总分', ascending=False).reset_index(drop=True)  # 获取前150名学生的各科均值
        dataTest = data150[:basicData.vipCount]  # 取前面150名
        dataTest = dataTest.drop(labels=['班级'], axis=1).mean(numeric_only=True)
        dataTest = pd.DataFrame(dataTest).round(1)
        dataTest.columns = ['前150均分']  # 将dataframe的列名 重新命名
        mean_df = mean_df.join(dataTest)

        dataTheOne = dfFormPath.loc[dfFormPath['姓名'] == stuName]  # 获取要查询的学生各项成绩
        dataTheOne = dataTheOne.drop(labels=['班级', '姓名'], axis=1)
        dataTheOne = dataTheOne.T
        dataTheOne.columns = [stuName + '成绩']
        mean_df = mean_df.join(dataTheOne)

        dataMax = data150.drop(labels=['姓名', '班级'], axis=1).max()  # 获取各科的最高成绩
        dataMax = pd.DataFrame(dataMax)
        dataMax.columns = ['最高分']

        mean_df = mean_df.join(dataMax)
        return mean_df

    def classAvgAndVariance(self, choose=False, courseList=basicData.coures8List):          #获得 班级 全部学科的均分 全部学科的方差
        df = self.excelFileDf  # 获得全部原始的数据表格
        allDF = pd.DataFrame({'班级': basicData.classList})  # 构造班级列的空dataframe
        for courseName in courseList:  # 遍历学科，每遍历一个学科，将均值和方差计算出，并添加到原来的空dataframe
            if choose:
                df = df.sort_values(by=courseName, ascending=False).reset_index(
                    drop=True)  # 将前150名重新排序，重建索引
                df = df[:basicData.vipCount]  # 若choose为真，则选择前150名学生进行数据统计
            courseDf = df[['班级', courseName]]
            groupDF = courseDf.groupby(['班级'], as_index=False).mean()  # 无索引形式 返回根据班级分组计算的均分
            groupAvg = pd.DataFrame({'班级': basicData.classList, courseName + '均分': groupDF[courseName]})
            allDF = pd.merge(allDF, groupAvg, on=['班级'], how='left')  # 左连接的形式，以班级为基础 加入总表

            groupVar = courseDf.groupby(['班级'], as_index=False).var()  # 无索引形式 返回根据班级分组计算的方差
            groupXX = pd.DataFrame({'班级': basicData.classList, courseName + '方差': groupVar[courseName]})
            allDF = pd.merge(allDF, groupXX, on=['班级'], how='left').round(1)  # 左连接的形式，以班级为基础 加入总表
        return allDF

    def getTheCourseAvg(self, courseName, choose=False):  # 各班的平均值
        theClassScoreAvg = self.classAvgAndVariance()[['班级', courseName + '均分']]
        theClassScoreAvg = theClassScoreAvg.sort_values(by=courseName + '均分', ascending=False).reset_index(drop=True)
        return theClassScoreAvg

    def getTheCourseVariance(self, courseName, choose=False):  # 得到各班的方差表
        theClassScoreVar = self.classAvgAndVariance()[['班级', courseName + '方差']]
        theClassScoreVar = theClassScoreVar.sort_values(by=courseName + '方差', ascending=True).reset_index(drop=True)
        return theClassScoreVar


    def rankSum(self, courseName):  # 获得某一学科 每10名1次的人数累积
        dataTest = self.excelFileDf[['班级', '姓名', courseName]]
        dataTest = dataTest.sort_values(by=courseName, ascending=False).reset_index(drop=True)  # 根据学科的
        dataTest = dataTest[:basicData.vipCount]  # 取前面150名
        dfNum = pd.DataFrame()
        dfNum['班级'] = basicData.classList
        yList = []
        for i in range(basicData.classesNumber, basicData.vipCount + basicData.classesNumber, basicData.classesNumber):  # i 是多少名之前
            dataAdd = dataTest[:i][['班级', courseName]]
            dataResult = dataAdd.groupby(['班级'], as_index=False).count()                #将前多少名进行计数
            columnName = str(i) + '名前'
            yList.append(columnName)  # 表头
            dataResult.columns = ['班级', columnName]  # 将dataframe的列名 重新命名 并
            dataResult['班级'] = dataResult['班级'].astype('str') + '班' #将班级列由1234改为 1班 2班 3班 4班这种格式
            dfNum = pd.merge(dfNum, dataResult, on=['班级'], how='left')  # 将dataResult 结果表格，左连接到数据总表 dfNum里
        dfNum = dfNum.fillna(0)  # 将空值都改为0
        dfNum.loc[:, dfNum.columns != '班级'] = dfNum.loc[:, dfNum.columns != '班级'].astype("int")  # 将除了班级列以外的列进行取整
        return dfNum,yList

    def scoreClassSum(self, courseName):  # 获得某一学科 每10名1个等级的 分数累加
        dataTest = self.excelFileDf[['班级', '姓名', courseName]]
        dataTest = dataTest.sort_values(by=courseName, ascending=False).reset_index(drop=True)  # 根据学科的
        dataTest = dataTest[:basicData.vipCount]  # 取前面150名
        dfSum = pd.DataFrame()
        dfSum['班级'] = basicData.classList
        yList = []
        for i in range(basicData.classesNumber, basicData.vipCount + basicData.classesNumber,
                       basicData.classesNumber):  # i 是多少名之前
            dataAdd = dataTest[:i][['班级', courseName]]
            dataResult = dataAdd.groupby(['班级'], as_index=False).sum()  # 将前多少名进行计数
            columnName = str(i) + '名前'
            yList.append(columnName)  # 表头
            dataResult.columns = ['班级', columnName]  # 将dataframe的列名 重新命名 并
            dataResult['班级'] = dataResult['班级'].astype('str') + '班'  # 将班级列由1234改为 1班 2班 3班 4班这种格式
            dfSum = pd.merge(dfSum, dataResult, on=['班级'], how='left')  # 将dataResult 结果表格，左连接到数据总表 dfNum里
        dfSum = dfSum.fillna(0)  # 将空值都改为0
        dfSum.loc[:, dfSum.columns != '班级'] = dfSum.loc[:, dfSum.columns != '班级'].astype("int")  # 将除了班级列以外的列进行取整
        return dfSum, yList

