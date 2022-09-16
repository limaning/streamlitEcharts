
#存储基本的数据、列表等必要信息



coures8List = ['语文','数学','英语','物理','化学','历史','政治','总分']              #所有 学科名
ranking8List = list(i+'排名' for i in coures8List)                      # 学科排名 列表

coures6List = ['语文','数学','英语','文综','理综','总分']              #所有 学科名
ranking6List = list(i+'排名' for i in coures6List)                      # 学科排名 列表

vipCount = 150                  #存储特别关注的前多少名学生

excelFilePath = './excelData/二模成绩.xlsx'                                        #使用的excel源文件

classesNumber = 10