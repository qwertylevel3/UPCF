# coding:utf-8

import csv

ratingFile = 'smallData/ratings.csv'


# ratingFile='data/ratings.csv'


class RMatrix:
    def __init__(self, movieidMap, lenx=0, leny=0):
        # movie id->I id 的映射
        # 用来快速查询某个id的项目的评分在R中的位置
        self.movieidMap = movieidMap
        # 构造一个空的二维数组
        self.matrix = [[]]
        # user id 从1开始
        for i in range(0, lenx + 1):
            self.matrix.append([])
            for j in range(0, leny):
                self.matrix[i].append([])

    def getData(self, i, j):
        ii = i
        jj = self.movieidMap[j]

        return self.matrix[ii][jj]

    def setData(self, data, i, j):
        ii = i
        jj = self.movieidMap[j]
        self.matrix[ii][jj] = data


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
    for i in range(0, len(I)):
        movieidMap[I[i]] = i
    R = RMatrix(movieidMap, len(U), len(I))

    for line in allData:
        userid = int(line[0])
        movieid = int(line[1])

        R.setData(float(line[2]), userid, movieid)
    return U, I, R


U, I, R = initData()
print R.getData(14, 3988)
