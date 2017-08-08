# -*- coding: utf-8 -*-

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

