#专门用于数据处理的文件

import pandas as pd
import basicData

couresList = basicData.coures6List              #所有 学科名
rankingList = list(i+'排名' for i in couresList)                      # 学科排名 列表

excelFilePath = basicData.excelFilePath                                        #使用的excel源文件

def getBaseDf():
    dfFormPath = pd.DataFrame(pd.read_excel(excelFilePath))  # 将原始数据表转化成dataframe
    return dfFormPath


def getClassStuCount():
    # 统计原始数据表中，各班都有多少学生，并出dataframe
    dfFormPath = getBaseDf()
    dfClass = dfFormPath['班级'].value_counts()  # 获取班级中各元素出现的次数
    classDataframe = pd.DataFrame({'班级': dfClass.index, '人数': dfClass.values})  # 用获取的Series的 index和value重新构造dataframe
    classDataframe = classDataframe.sort_values(by='班级', ascending=True)  # 用班级列进行排序
    classDataframe = classDataframe.reset_index(drop=True)  # 重置索引 使其按1-10排列 。将原索引删除
    classDataframe['班级'] = classDataframe['班级'].astype(str)  # 将班级列转化成字符串，
    classDataframe['班级'] = classDataframe['班级'] + '班'  # 将 1-10后面都加上"班"，成为1班 2班这种形式
    xClassName = classDataframe['班级'].tolist()      #获得班级列表
    yClassName = classDataframe['人数'].tolist()      #获得班级人数列表    结果用函数后面[0]或者[1]获取
    return classDataframe                   #

def getAllCourseRanking():
    # 班级 姓名 总分 总分排名，按总分进行排名的df
    dfFormPath = getBaseDf()  # 将原始数据表转化成dataframe
    for i in couresList:
        dfFormPath = dfFormPath.sort_values(by=i, ascending=False)  # 按本学科进行排名，得到新的表格
        dfFormPath = dfFormPath.reset_index(drop=True)  # 索引按总分排名重新布置
        newColTitle = i + '排名'
        dfFormPath[newColTitle] = dfFormPath.index + 1  # 添加科目排名列，名次按index+1来算
        dfFormPath[newColTitle] = dfFormPath[newColTitle].astype(int)  # 将排名数据类型都转化为整整数类型
    return dfFormPath  # 得到的数据表包括了所有学科的成绩和排名

def getStuAllRank(name):
    dfData = getAllCourseRanking()
    getData = dfData.loc[dfData['姓名'] == name]  # 获取姓名是要查找的详细数据
    getDataGet = getData[rankingList]               #获取各科排名
    xList = rankingList
    yList = getDataGet.values.tolist()[0]           #获取各科排名的数值列表
    return xList, yList                              #结果用函数后面[0]或者[1]获取

def getRadarTable(stuName):                     #获取学生、总均分、前150均分、最高分的dataframe
    dfFormPath= getBaseDf()
    mean_df = dfFormPath.drop(labels=['班级'], axis=1).mean().round(0)              #获取各科总分均值
    mean_df = pd.DataFrame(mean_df)
    mean_df['index'] = mean_df.index  # 将索引转换为列
    mean_df.columns = ['总均分', '学科']  # 将dataframe的列名 重新命名

    data150 = dfFormPath.sort_values(by='总分', ascending=False).reset_index(drop=True)  # 获取前150名学生的各科均值
    dataTest = data150[:basicData.vipCount]  # 取前面150名
    dataTest = dataTest.drop(labels=['班级'], axis=1).mean().round(0)
    dataTest = pd.DataFrame(dataTest)
    dataTest.columns = ['前150均分']  # 将dataframe的列名 重新命名
    mean_df = mean_df.join(dataTest)

    dataTheOne = dfFormPath.loc[dfFormPath['姓名'] == stuName]                #获取要查询的学生各项成绩
    dataTheOne = dataTheOne.drop(labels=['班级','姓名'], axis=1)
    dataTheOne = dataTheOne.T
    dataTheOne.columns = [stuName+'成绩']
    mean_df = mean_df.join(dataTheOne)

    dataMax = data150.drop(labels=['姓名','班级'], axis=1).max()            #获取各科的最高成绩
    dataMax = pd.DataFrame(dataMax)
    dataMax.columns = ['最高分']

    mean_df = mean_df.join(dataMax)
    #print(mean_df)
    return mean_df


def getTheStuResults(stuName):                      #获取指定学生各科成绩
    allTable = getBaseDf()                                 #获得所有表格
    stuTable = allTable.loc[allTable['姓名']==stuName]                #选取姓名为所选姓名的整行
    stuTableResult = stuTable.drop(labels=['班级', '姓名'], axis=1)     #删除班级 姓名列
    return stuTableResult

def getTheCourseRank(allCourseTable, courseName):
    # 获取任意学科的成绩和排名
    rankName = courseName + '排名'
    dfFormCR = allCourseTable[['姓名', '班级', courseName, rankName]]  # 姓名 班级 学科名 学科排名
    return dfFormCR

def getTheCourseAvg(courseName, choose=False):                      #各班的平均值
    theCourseScore = getBaseDf()[['班级', '姓名', courseName]]
    if choose:
        theCourseScore = theCourseScore[:basicData.vipCount]             #若choose为真，则选择前150名学生进行数据统计
    groupDF = theCourseScore[courseName].groupby(theCourseScore['班级'])
    groupData = groupDF.mean()
    groupXX = pd.DataFrame({'班级': groupData.index, courseName + '均分': groupData.values})
    groupXX['班级'] = groupXX['班级'].astype(str) + '班'  # 将 1-10后面都加上"班"，成为1班 2班这种形式
    groupXX = groupXX.sort_values(by=courseName + '均分', ascending=False)
    return groupXX


def getTheCourseVariance(courseName, choose=False):                         #得到各班的方差表
    theCourseScore = getBaseDf()[['班级', '姓名', courseName]]
    if choose:
        theCourseScore = theCourseScore[:basicData.vipCount]             #若choose为真，则选择前150名学生进行数据统计
    groupDF = theCourseScore[courseName].groupby(theCourseScore['班级'])
    groupData = groupDF.var()                       #计算方差
    groupXX = pd.DataFrame({'班级': groupData.index, courseName + '方差': groupData.values})
    groupXX['班级'] = groupXX['班级'].astype(str) + '班'  # 将 1-10后面都加上"班"，成为1班 2班这种形式
    groupXX = groupXX.sort_values(by=courseName + '方差', ascending=True)
    return groupXX


def rankSum(courseName,stuName='刘备'):                                    #获得某一学科 每10名1次的人数累积
    dataTest = getBaseDf()[['班级', '姓名', courseName]]
    dataTest = dataTest.sort_values(by=courseName, ascending=False).reset_index(drop=True)  # 根据学科的
    dataTest = dataTest[:basicData.vipCount]  # 取前面150名
    dfNum = pd.DataFrame()
    dfNum['班级'] = list(range(1, basicData.classesNumber + 1))
    yList = []
    for i in range(10, basicData.vipCount + 10, 10):                    #i 是多少名之前
        dataAdd = dataTest[:i]
        dataResult = pd.DataFrame(dataAdd['班级'].value_counts())     #按班级 进行计数 得到的是Series，转换为dataframe
        dataResult['index'] = dataResult.index                          #将索引转换为列
        dataResult.columns = ['人数', '班级']                           #将dataframe的列名 重新命名
        columnName = str(i) + '名前'
        yList.append(columnName)
        for a, b in zip(dataResult['班级'], dataResult['人数']):        #遍历这个dataframe
            dfNum.loc[dfNum['班级'] == a, [columnName]] = b         # 在dfNum表中，班级为a，列为"i名前"，添加数据b
    dfNum = dfNum.fillna(0)  # 将空值都改为0
    return dfNum, yList

def scoreClassSum(courseName,stuName='刘备'):                                    #获得某一学科 每10名1个等级的 分数累加
    dataTest = getBaseDf()[['班级', '姓名', courseName]]
    dataTest = dataTest.sort_values(by=courseName, ascending=False).reset_index(drop=True)  # 根据学科的
    dataTest = dataTest[:basicData.vipCount]  # 取前面150名
    dfSum = pd.DataFrame()
    dfSum['班级'] = list(range(1, basicData.classesNumber + 1))
    yList = []
    for i in range(10, basicData.vipCount + 10, 10):                    #i 是多少名之前
        dataAdd = dataTest[:i]
        dataAdd['总和'] = dataAdd.groupby(['班级'])[courseName].transform('sum')  # 按班级 进行统计
        dataResult = dataAdd.drop(labels=[courseName, '姓名'], axis=1)     #删除班级 姓名列
        dataResult = dataResult.drop_duplicates(subset = '班级')
        columnName = '前'+str(i) + '名'
        yList.append(columnName)
        for a, b in zip(dataResult['班级'], dataResult['总和']):        #遍历这个dataframe
            dfSum.loc[dfSum['班级'] == a, [columnName]] = b         # 在dfNum表中，班级为a，列为"i名前"，添加数据b
    dfSum = dfSum.fillna(0)  # 将空值都改为0
    return dfSum, yList