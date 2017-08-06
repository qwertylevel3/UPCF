# coding:utf-8

import csv
import math

ratingFile = 'smallData/ratings.csv'
itemMatrixFile = 'temp/itemMatrix.csv'
unknowItemMatrixFile = 'temp/unknowItemMatrix.csv'
intimacyMatrixFile = 'temp/intimacyMatrix.csv'


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
# ret:
# U:所有用户id列表
# I:所有项目id列表
# R:评分矩阵(r(i,j)=>用户i对项目j的评分)
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


def mean(u, R):
    Ru = 0.0
    Du = R.getRow(u)
    # 计算均值
    count = 0
    for i in range(0, len(Du)):
        if Du[i] != 0.0:
            Ru += Du[i]
            count = count + 1
    return Ru / count


# 预测用户u对q的评分
def forecast(u, q, R, intimacy, Nu):
    Ru = mean(u, R)

    tempUp = 0.0
    tempDown = 0.0
    for v in Nu:
        Rv = mean(v, R)
        tUp = intimacy[u][v] * (R.getData(v, q) - Rv)
        tempUp += tUp

        tDown = abs(intimacy[u][v])
        tempDown += tDown

    if tempDown == 0:
        return Ru

    result = Ru + tempUp / tempDown

    if result > 5:
        result = 5
    return result


# 返回u的评价项目id列表
def getItemList(u, R):
    result = []
    movieidMapR = R.getMovieidMapR()
    itemList = R.getRow(u)

    for i in range(0, len(itemList)):
        if itemList[i] > 0:
            result.append(movieidMapR[i])
    return result


# 获取u的未知项目列表
def getUnknowItem(u, R, nearest):
    nearestList = nearest[u]
    itemSet = []

    # 当前用户的已评分项目列表
    userItemList = getItemList(u, R)

    # 找到所有当前用户没见过的项目
    for nearestUserId in nearestList:
        # 找到user的所有评分项目id
        tempItemList = getItemList(nearestUserId, R)
        for item in tempItemList:
            if item not in userItemList and \
                            item not in itemSet:
                itemSet.append(item)

    return itemSet


# 写入一个二维数组到csv文件中
def writeMatrix(matrix, fileName):
    with open(fileName, 'wb') as csvfile:
        writer = csv.writer(csvfile, dialect='excel')
        for line in matrix:
            writer.writerow(line)


def writeMatrixPart(matrix, fileName, a, b, c, d):
    with open(fileName, 'wb') as csvfile:
        writer = csv.writer(csvfile, dialect='excel')
        i = a
        while i <= b:
            temp = []
            j = c
            while j <= d:
                temp.append(matrix[i][j])
                j = j + 1
            writer.writerow(temp)
            i = i + 1


# 获取用户评价项目矩阵
def getItemMatrix(U, R):
    itemMatrix = []

    for u in U:
        itemMatrix.append(getItemList(u, R))
    return itemMatrix


# 获取用户位置项目矩阵
def getUnknowItemMatrix(U, R, nearest):
    unknowMatrix = []

    for u in U:
        tempList = getUnknowItem(u, R, nearest)
        unknowMatrix.append(tempList)
    return unknowMatrix


# 获取用户最近邻矩阵
def getNearestMatrix(nearestNum, userNum, intimacy):
    nearest = []
    nearest.append([])

    for i in range(1, userNum + 1):
        # 去除第一个
        nearestList = intimacy[i][1:userNum + 1]
        nearestList.sort(cmp=None, key=lambda intim: intim["value"], reverse=True)
        # 取前nearestNum个
        nearestList = nearestList[0:nearestNum]

        nearestIdList = []

        for intim in nearestList:
            nearestIdList.append(intim["v"])
        nearest.append(nearestIdList)
    return nearest


# 获取用户相似度矩阵
def getIntimacyMatrix(U, R):
    userNum = len(U)
    intimacy = []
    # 用户id从1开始，首行空出
    intimacy.append([])

    # 填充首行
    for i in range(0, userNum + 1):
        intimacy[0].append({
            "value": -1,
            "u": i,
            "v": 0,
        })

    for i in range(1, userNum + 1):
        intimacy.append([])
        intimacy[i].append({
            "value": -1,
            "u": i,
            "v": 0,
        })
        for j in range(1, userNum + 1):
            intimacy[i].append({
                "value": -1,
                "u": i,
                "v": j,
            })

    # TODO 对称矩阵，计算可优化
    for i in range(1, userNum + 1):
        for j in range(1, userNum + 1):
            if i == j:
                intimacy[i][j] = {
                    "value": 2,
                    "u": i,
                    "v": j,
                }
            else:
                intimacy[i][j] = {
                    "value": sim(i, j, R),
                    "u": i,
                    "v": j,
                }
    return intimacy


print("---start---")

print("initData...")
U, I, R = initData()
print("initData over")

print("calculate intimacy")

intimacy = getIntimacyMatrix(U, R)

intimacyMatrix = []
for i in range(0, len(intimacy)):
    line = intimacy[i]
    intimacyMatrix.append([])
    for item in line:
        intimacyMatrix[i].append(item["value"])

# writeMatrixPart(intimacyMatrix, intimacyMatrixFile,
#           1,len(intimacyMatrix)-1,
#           1,len(intimacyMatrix[0])-1)

print("calculate intimacy over")

print("calculate nearest")

# 最近邻5个人
nearest = getNearestMatrix(15, len(U), intimacy)

# writeMatrixPart(nearest, "temp/nearestMatrix.csv",
#                1, len(nearest) - 1,
#                0, len(nearest[1]) - 1)

print("calculate nearest over")

itemMatrix = getItemMatrix(U, R)
# writeMatrix(itemMatrix, "temp/itemMatrix.csv")

unknowItemMatrix = getUnknowItemMatrix(U, R, nearest)
# writeMatrix(unknowItemMatrix, "temp/unknowItemMatrix.csv")

print("---end---")
