# -*- coding: utf-8 -*-

import csv
import math
from RMatrix import *
from util.path import *
from util.mycsv import *

from evaluate import evaluate
from sklearn.cluster import KMeans
from progressbar import *


class UPCF():
    def __init__(self, allData):
        # U:所有用户id列表
        # I:所有项目id列表
        # R:评分矩阵(r(i,j)=>用户i对项目j的评分)
        # iiMap:item index -> index
        # iiMapR:index -> item index
        self.U = []
        self.I = []

        # 填充数据
        for line in allData:
            userid = int(line[0])
            movieid = int(line[1])

            if userid not in self.U:
                self.U.append(userid)
            if int(movieid) not in self.I:
                self.I.append(movieid)

        self.I = sorted(self.I)

        self.iiMap = {}
        self.iiMapR = {}
        for i in range(0, len(self.I)):
            self.iiMap[self.I[i]] = i
            self.iiMapR[i] = self.I[i]
        self.R = RMatrix(self.iiMap, self.iiMapR, len(self.U), len(self.I))

        # 评分矩阵初始化
        self.R.initData(allData)

        # 项目聚类
        # 项目特征向量(评分向量)
        itemFeature = []

        for item in self.I:
            itemFeature.append(self.R.getFilledCol(item))

        saveData(itemFeature, "output/itemFeature.csv")

        print("start kmeans")
        # k-means聚类，k=20
        self.tagList = KMeans(20, n_jobs=-1).fit_predict(itemFeature)
        print("kmeans over")

        self.itemClusterCache = {}
        print("calculate item cluster cache")
        self.calculateItemCluster()
        print("calculate item cluster cache over")


    # 计算用户user在item下的近邻用户组,取最近的num个
    def getUserCluster(self, user, item, num):
        # 项目的聚类簇
        itemCluster = self.getItemCluster(item)
        userList = []
        for u in self.U:
            if u == user:
                continue
            userList.append({
                "userID": u,
                "sim": self.sim(user, u, item, itemCluster)
            })
        userList.sort(cmp=None, key=lambda sim: sim["sim"], reverse=True)
        result = []
        for i in range(0, num):
            if userList[i]["sim"] != -100:
                result.append(userList[i])
        return result

    # 计算 u,v之间在item下的相似度 u,v是用户id
    # 如果无法计算，返回-100
    def sim(self, u, v, item, itemCluster):
        # Du,Dv是u，v各自评分向量
        Du = self.R.getRow(u)
        Dv = self.R.getRow(v)

        # Iu,Iv是u，v各自的项目id集合
        # UPCF中这里的项目必须是项目簇中的项目
        Iu = []
        Iv = []
        # Iu,Iv交集
        Iuv = []

        # 评分向量均值
        Ru = 0.0
        Rv = 0.0

        # 设置Iu
        for i in range(0, len(Du)):
            # 如果有评分，且该评分的项目在项目簇中,保存这个项目
            if Du[i] > 0.0 and (self.iiMapR[i] in itemCluster):
                Ru += Du[i]
                Iu.append(self.iiMapR[i])

        # 设置Iv
        for i in range(0, len(Dv)):
            # 如果有评分，且该评分的项目在项目簇中,保存这个项目
            if Dv[i] != 0.0 and (self.iiMapR[i] in itemCluster):
                Rv += Dv[i]
                Iv.append(self.iiMapR[i])

        # 如果没有评分项目，跳过
        if len(Iu) == 0 or len(Iv) == 0:
            return -100

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
            tup = (self.R.getData(u, iuv) - Ru) * (self.R.getData(v, iuv) - Rv)
            tempUp += tup

            tdown1 = (self.R.getData(u, iuv) - Ru) * (self.R.getData(u, iuv) - Ru)
            tempDown1 += tdown1
            tdown2 = (self.R.getData(v, iuv) - Rv) * (self.R.getData(v, iuv) - Rv)
            tempDown2 += tdown2

        tempDown = math.sqrt(tempDown1) * math.sqrt(tempDown2)
        if tempDown == 0:
            return -100
        return tempUp / tempDown

    # 计算用户u的评分项目均值
    def mean(self, u):
        return self.R.getMean(u)

    # 预测用户u对q的评分
    def forecast(self, u, q):
        Ru = self.mean(u)

        # 最近10个用户
        # userCluster:{"userID":"sim"}
        userCluster = self.getUserCluster(u, q, 10)

        # 如果没有近邻用户，返回0
        if len(userCluster) == 0:
            return 0

        # 项目簇
        itemCluster = self.getItemCluster(q)

        tempUp = 0.0
        tempDown = 0.0
        for v in userCluster:
            # 用户u和v的相似度
            simuv = v["sim"]

            Rv = self.mean(v["userID"])
            tUp = simuv * (self.R.getData(v["userID"], q) - Rv)
            tempUp += tUp

            tDown = abs(simuv)
            tempDown += tDown

        if tempDown == 0:
            return Ru

        result = Ru + tempUp / tempDown

        if result < 0:
            result = 0
        if result > 5:
            result = 5
        return result

    def calculateItemCluster(self):
        for i in self.I:
            cluster = self.__calculateItemCluster(i)
            self.itemClusterCache[i] = cluster

    def __calculateItemCluster(self, item):
        # 获取项目在列表中的编号
        index = self.iiMap[item]
        # 获取项目聚类编号
        tag = self.tagList[index]

        # 该项目聚类项目簇
        cluster = []
        for i in range(0, len(self.I)):
            tempTag = self.tagList[i]
            if tempTag == tag:
                cluster.append(self.I[i])
        return cluster

    # 获取项目i的聚类簇
    # item:item 编号
    def getItemCluster(self, item):
        return self.itemClusterCache[item]


    def run(self, checkDataFile, forecastDataFile, realDataFile):
        print("into run")
        # 预测
        # 对每个待预测的项目，找近邻用户中有这个项目评分的，作为预测依据
        checkData = readCSV(checkDataFile)
        realValue = []
        forecastValue = []
        forecastMatrix = []
        realMatrix = []

        print("start")

        widget = [Percentage(), ' ', Bar(marker=RotatingMarker('>-='))]
        pbar = ProgressBar(widgets=widget, maxval=len(checkData)).start()

        count = 0.0

        for line in checkData:
            u = int(line[0])
            item = int(line[1])
            real = float(line[2])

            f = self.forecast(u, item)
            if f > 0:
                forecastValue.append(f)
                realValue.append(real)
                forecastMatrix.append([u, item, f])
                realMatrix.append([u, item, real])
            count = count + 1.0
            pbar.update(count)
        pbar.finish()

        saveData(forecastMatrix, forecastDataFile)
        saveData(realMatrix, realDataFile)

        return evaluate.getMAE(forecastValue, realValue)
