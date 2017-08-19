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

    tempCheckData = []
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

    userCount = [int(c / 5) for c in userCount]

    # test集合中所有项目列表
    allTestItem = []

    for i in range(1, len(userCount)):
        checkList = sample(allUser[i], userCount[i])
        testList = []
        for item in allUser[i]:
            if item not in checkList:
                testList.append(item)
                if int(item[1]) not in allTestItem:
                    allTestItem.append(int(item[1]))

        for item in checkList:
            tempCheckData.append(item)
        for item in testList:
            testData.append(item)

    # 去除在check中存在但是test中不存在的项目
    for i in tempCheckData:
        if int(i[1]) in allTestItem:
            checkData.append(i)

    saveData(checkData, checkDataFileName)
    saveData(testData, testDataFileName)


# 将源数据切分
def extractSample(oriFile):
    for i in range(0, 5):
        extractRatingSample(oriFile,
                            "output/small/check_" + str(i) + ".csv",
                            "output/small/test_" + str(i) + ".csv")
