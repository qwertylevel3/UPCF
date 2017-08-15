# -*- coding: utf-8 -*-

import csv
from random import sample
from util.mycsv import saveData


# 将评分数据切分为测试集合和训练集合
# 比例为1:4
def extractRatingSample(ratingFile, checkDataFileName, testDataFileName):
    csv_reader = csv.reader(open(ratingFile))
    allData = []
    for line in csv_reader:
        allData.append(line)
    # 去除表头
    allData = allData[1:len(allData)]

    dataLen = len(allData)

    checkData = []
    testData = []

    # 从1开始计数,保存用户i的评分项目数目
    userCount = []
    userCount.append(0)

    # 切分后的用户评分信息
    allUser = []
    allUser.append([])

    # 记录每个用户的评分项目数目
    for line in allData:
        if int(line[0]) > len(userCount) - 1:
            userCount.append(1)
            allUser.append([])
            allUser[int(line[0])].append(line)
        else:
            userCount[int(line[0])] = userCount[int(line[0])] + 1
            allUser[int(line[0])].append(line)

    userCount = [c / 5 for c in userCount]

    for i in range(1, len(userCount)):
        checkList = sample(allUser[i], userCount[i])
        testList = []
        for item in allUser[i]:
            if item not in checkList:
                testList.append(item)

        for item in checkList:
            checkData.append(item)
        for item in testList:
            testData.append(item)

    saveData(checkData, checkDataFileName)
    saveData(testData, testDataFileName)

    return checkData, testData


# 将源数据切分
def extractSample(oriFile):
    for i in range(0, 5):
        extractRatingSample(oriFile,
                            "output/BaseCF/check_" + str(i) + ".csv",
                            "output/BaseCF/test_" + str(i) + ".csv")
