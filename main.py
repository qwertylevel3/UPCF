# coding:utf-8

import csv
import math

ratingFile = 'smallData/ratings.csv'


# ratingFile='data/ratings.csv'


class RMatrix:
    def __init__(self, movieidMap, movieidMapR, lenx=0, leny=0):
        # movie id->I id 的映射
        # 用来快速查询某个id的项目的评分在R中的位置
        self.movieidMap = movieidMap
        # I id->movie id
        self.movieidMapR = movieidMapR

        # 构造一个空的二维数组
        self.matrix = [[]]
        # user id 从1开始
        for i in range(0, lenx + 1):
            self.matrix.append([])
            for j in range(0, leny):
                self.matrix[i].append(0)

    def getData(self, i, j):
        ii = i
        jj = self.movieidMap[j]
        return self.matrix[ii][jj]

    def setData(self, data, i, j):
        ii = i
        jj = self.movieidMap[j]
        self.matrix[ii][jj] = data

    def getMovieidMap(self):
        return self.movieidMap

    def getMovieidMapR(self):
        return self.movieidMapR

    def getRow(self, index):
        return self.matrix[index]


# 初始化数据
def initData():
    U = []
    I = []

    # 读入数据
    csv_reader = csv.reader(open(ratingFile))

    allData = []
    for line in csv_reader:
        allData.append(line)
    # 去除表头
    allData = allData[1:len(allData)]

    # 填充数据
    for line in allData:
        userid = int(line[0])
        movieid = int(line[1])

        if userid not in U:
            U.append(userid)
        if int(movieid) not in I:
            I.append(movieid)

    I = sorted(I)

    movieidMap = {}
    movieidMapR = {}
    for i in range(0, len(I)):
        movieidMap[I[i]] = i
        movieidMapR[i] = I[i]
    R = RMatrix(movieidMap, movieidMapR, len(U), len(I))

    for line in allData:
        userid = int(line[0])
        movieid = int(line[1])

        R.setData(float(line[2]), userid, movieid)
    return U, I, R

# 计算 u,v之间的相似度 u,v是用户id
def sim(u, v, R):
    # Du,Dv是u，v各自评分向量
    Du = R.getRow(u)
    Dv = R.getRow(v)

    # Iu,Iv是u，v各自的项目id集合
    Iu = []
    Iv = []
    # Iu,Iv交集
    Iuv = []

    # 评分向量均值
    Ru = 0.0
    Rv = 0.0

    # 计算均值
    for i in range(0, len(Du)):
        if Du[i] != 0.0:
            Ru += Du[i]
            Iu.append(R.getMovieidMapR()[i])

    for i in range(0, len(Dv)):
        if Dv[i] != 0.0:
            Rv += Dv[i]
            Iv.append(R.getMovieidMapR()[i])
    Ru = Ru / len(Iu)
    Rv = Rv / len(Iv)

    # 计算交集
    for iu in Iu:
        if iu in Iv:
            Iuv.append(iu)

    tempUp = 0.0
    tempDown1 = 0.0
    tempDown2 = 0.0
    tempDown = 0.0

    for iuv in Iuv:
        tup = (R.getData(u, iuv) - Ru) * (R.getData(v, iuv) - Rv)
        tempUp += tup

        tdown1 = (R.getData(u, iuv) - Ru) * (R.getData(u, iuv) - Ru)
        tempDown1 += tdown1
        tdown2 = (R.getData(v, iuv) - Rv) * (R.getData(v, iuv) - Rv)
        tempDown2 += tdown2

    tempDown = math.sqrt(tempDown1) * math.sqrt(tempDown2)
    if tempDown == 0:
        return 0
    return tempUp / tempDown

#TODO
## 预测用户u对q的评分
#def forecast(u,q,intimacy):
#    Ru=


print("---start---")

print("initData...")
U, I, R = initData()
print("initData over")

print("calculate intimacy")
userNum = len(U)

intimacy = [[]]

for i in range(0, userNum):
    intimacy.append([])
    for j in range(0, userNum):
        intimacy[i].append({
            "value": -1,
            "u": i,
            "v": j,
        })

# TODO 对称矩阵，计算可优化
for i in range(1, userNum):
    for j in range(1, userNum):
        intimacy[i][j] = {
            "value": sim(i, j, R),
            "u": i,
            "v": j,
        }

print("calculate intimacy over")

print("calculate nearest")

# 最近邻3个人
nearestNum = 3
nearest = []
nearest.append([])

for i in range(1, userNum):
    intimacy[i].sort(cmp=None, key=lambda intim: intim["value"], reverse=True)
    nearestList = intimacy[i][0:nearestNum]

    nearestIdList = []

    for intim in nearestList:
        nearestIdList.append(intim["v"])
    nearest.append(nearestIdList)

print("calculate nearest over")


for i in range(1, userNum):
    print nearest[i]

print("---end---")
