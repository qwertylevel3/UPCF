# -*- coding: utf-8 -*-

from RMatrix import RMatrix
from util import mycsv



# 初始化数据
#
# ret:
# U:所有用户id列表
# I:所有项目id列表
# R:评分矩阵(r(i,j)=>用户i对项目j的评分)
def initData(allData):
    U = []
    I = []

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

    R.initData(allData)
    mycsv.saveData(R.matrix,"temp/matrix.csv")
    mycsv.saveData(R.filledMatrix,"temp/filledMatrix.csv")

    return U, I, R

