# coding:utf-8

import csv
import math
from RMatrix import *
from util.path import *
from util.helpFun import *


itemFile = 'temp/item.csv'
nearestFile= "temp/nearest.csv"
unknowItemFile = 'temp/unknowItem.csv'
intimacyFile = 'temp/intimacy.csv'
forecastFile= "temp/forecast.csv"


# 初始化数据
#
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


# 计算用户u的评分项目均值
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
        tUp = intimacy[u][v]["value"] * (R.getData(v, q) - Rv)
        tempUp += tUp

        tDown = abs(intimacy[u][v]["value"])
        tempDown += tDown

    if tempDown == 0:
        return Ru

    result = Ru + tempUp / tempDown

    if result < 0:
        result = 0
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


# 获取用户评价项目矩阵
def getItemMatrix(U, R):
    itemMatrix = []

    for u in U:
        itemMatrix.append(getItemList(u, R))
    return itemMatrix


# 获取用户位置项目矩阵
def getUnknowItemMatrix(U, R, nearest):
    unknowMatrix = []
    unknowMatrix.append([])

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
        # 不取第一个，第一个一定是自己
        nearestList = nearestList[1:nearestNum + 1]

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


def getForecastMatrix(unknowItemMatrix, intimacy, nearest, R):
    result = []
    # 对于每一个用户
    for i in range(1, len(unknowItemMatrix)):
        forecastList = []
        # 预测用户的每一个未知项目评分
        for j in range(0, len(unknowItemMatrix[i])):
            f = forecast(i, unknowItemMatrix[i][j], R, intimacy, nearest[i])
            forecastList.append(f)
        result.append(forecastList)
    return result


def run():
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

    saveDataRowCol(intimacyMatrix, intimacyFile,
                   1, len(intimacyMatrix) - 1,
                   1, len(intimacyMatrix[0]) - 1)

    print("calculate intimacy over")

    print("calculate nearest")

    # 最近邻20个人
    nearest = getNearestMatrix(20, len(U), intimacy)

    saveDataRowCol(nearest, nearestFile,
                   1, len(nearest) - 1,
                   0, len(nearest[1]) - 1)

    print("calculate nearest over")

    print("calculate unknowItemMatrix")
    itemMatrix = getItemMatrix(U, R)
    saveData(itemMatrix, itemFile)

    unknowItemMatrix = getUnknowItemMatrix(U, R, nearest)
    saveData(unknowItemMatrix, unknowItemFile)
    print("calculate unknowItemMatrix over")

    forecastMatrix = getForecastMatrix(unknowItemMatrix, intimacy, nearest, R)

    saveData(forecastMatrix, forecastFile)

    print("---end---")
