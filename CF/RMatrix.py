# -*- coding: utf-8 -*-
import math
from progressbar import *
from util import mycsv
import os


# 评分数据矩阵
class RMatrix:
    def __init__(self, movieidMap, movieidMapR, lenx=0, leny=0):
        # movie id非连续，而且稀疏，故用map来映射到紧凑的序列上
        # 用来快速查询某个id的项目的评分在R中的位置

        # movie id->Matrix id 的映射
        self.movieidMap = movieidMap
        # Matrix id->movie id
        self.movieidMapR = movieidMapR

        # 首行0号用户,真实用户id是从1开始
        self.lenx = lenx + 1
        self.leny = leny

        # 整体均值(initData计算保存)
        self.mean = 0.0

        # 原评分矩阵
        self.matrix = [[]]
        # 填充后的矩阵
        self.filledMatrix = [[]]

        # 经凑数据，去除空评分
        self.tightMatrix = []

        # user id 从1开始,0行空出,方便查找
        for i in range(0, self.lenx):
            self.matrix.append([])
            self.filledMatrix.append([])
            for j in range(0, self.leny):
                self.matrix[i].append(0)
                self.filledMatrix[i].append(0)

    def getData(self, i, j):
        ii = i
        # TODO 防止越界
        if j not in self.movieidMap:
            return 0
        jj = self.movieidMap[j]
        return self.matrix[ii][jj]

    # 初始化matrix数据
    def initData(self, allData):
        # 填充数据
        for line in allData:
            userid = int(line[0])
            movieid = int(line[1])

            self.__setData(float(line[2]), userid, movieid)

        print("r mean")

        # 计算整体均值
        self.__calculateMatrixMean()

        print("r mean over")

        print("start tight matrix...")

        self.calculateTightMatrix()
        mycsv.saveData(self.tightMatrix,"output/UPCF/tightMatrix.csv")
        print("over tight matrix")

        if not os.path.exists("output/UPCF/filledMatrix.csv"):
            print("start fillMatrix")
            # 填充空数据
            self.fillMatrix()
            mycsv.saveData(self.filledMatrix, "output/UPCF/filledMatrix.csv")

        else:
            print("filledMatrix exist,read from file")
            self.filledMatrix = mycsv.readCSV("output/UPCF/filledMatrix.csv")
        print("fillMatrix over")

    def __setData(self, data, i, j):
        ii = i
        jj = self.movieidMap[j]
        self.matrix[ii][jj] = data
        self.filledMatrix[ii][jj] = data

    def getMovieidMap(self):
        return self.movieidMap

    def getMovieidMapR(self):
        return self.movieidMapR

    # 获取一行(某用户的所有项目评分)
    def getRow(self, user):
        return self.matrix[user]

    # 获取紧凑一行
    def getTightRow(self,user):
        return self.tightMatrix[user]

    # 获取某个项目评分向量
    def getFilledCol(self, itemIndex):
        ii = self.movieidMap[itemIndex]
        col = []
        for i in range(1, self.lenx):
            col.append(self.filledMatrix[i][ii])
        return col

    # 计算用户u的评分项目均值
    def getMean(self, user):
        sum = 0.0
        itemList = self.getRow(user)

        count = 0
        for i in range(0, len(itemList)):
            if itemList[i] != 0.0:
                sum += itemList[i]
                count = count + 1

        return sum / count

    # 计算整个矩阵评分均值
    def getMatrixMean(self):
        return self.mean

    # 返回u的评价项目id列表
    def getItemIDList(self, user):
        result = []
        itemList = self.getRow(user)

        for i in range(0, len(itemList)):
            if itemList[i] > 0:
                result.append(self.movieidMapR[i])
        return result

    # 计算整个矩阵均值
    def __calculateMatrixMean(self):
        sum = 0.0
        count = 0
        for i in range(1, self.lenx):
            for j in range(0, self.leny):
                if self.matrix[i][j] > 0:
                    sum += self.matrix[i][j]
                    count = count + 1
        self.mean = sum / count

    # 填充某个空项目
    def __fillItem(self, user, index):
        # 该项目总评分数
        S = 0
        sum = 0.0

        for u in range(1, self.lenx):
            if self.matrix[u][index] > 0:
                sum += self.matrix[u][index]
                S = S + 1
        # 项目流行度权重系数
        w = 1 / (math.log(1 + S))

        meanU = self.getMean(user)
        # 用户u评分均值和总均值的偏差
        bu = meanU - self.mean

        # 项目item评分均值和总均值的偏差
        bi = sum / S - self.mean

        fvalue = self.restrictValue(self.getMatrixMean() + bu + bi * w)

        self.filledMatrix[user][index] = fvalue

    def restrictValue(self, v):
        if v > 5:
            v = 5
        if v < 0:
            v = 0
        return v

    def calculateTightMatrix(self):
        self.tightMatrix.append([])

        for i in range(1, self.lenx):
            self.tightMatrix.append([])
            for j in range(0, self.leny):
                if self.matrix[i][j] > 0:
                    self.tightMatrix[i].append({
                        "value": self.matrix[i][j],
                        "index": j,
                        "item":self.movieidMapR[j]
                    })



    # 项目缺失值预测填充
    def fillMatrix(self):

        widget = [Percentage(), ' ', Bar(marker=RotatingMarker('>-='))]

        total = self.lenx * self.leny

        pbar = ProgressBar(widgets=widget, maxval=total).start()
        count = 0.0
        for i in range(1, self.lenx):
            for j in range(0, self.leny):
                if self.matrix[i][j] == 0:
                    self.__fillItem(i, j)
                count = count + 1.0
                pbar.update(count)
        pbar.finish()
