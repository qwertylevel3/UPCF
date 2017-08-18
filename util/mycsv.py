# -*- coding: utf-8 -*-
import csv

# 写入数组
def saveVector(vector,fileName):
    with open(fileName, 'wb') as csvfile:
        writer = csv.writer(csvfile, dialect='excel')
        for line in vector:
            writer.writerow([line])

def readVector(fileName):
    csv_reader=csv.reader(open(fileName))

    allData=[]
    for line in csv_reader:
        for data in line:
            allData.append(data)
    return allData

# 读取csv文件
def readCSV(fileName):
    # 读入数据
    csv_reader = csv.reader(open(fileName))

    allData = []
    for line in csv_reader:
        allData.append(line)
    return allData

def readCSVnoTitle(fileName):
    # 读入数据
    csv_reader = csv.reader(open(fileName))

    allData = []
    for line in csv_reader:
        allData.append(line)
    # 去除表头
    allData = allData[1:len(allData)]
    return allData




# 写入数据到csv文件中
def saveData(matrix, fileName):
    with open(fileName, 'wb') as csvfile:
        writer = csv.writer(csvfile, dialect='excel')
        for line in matrix:
            writer.writerow(line)


# 写数据某些行
def saveDataRow(matrix, fileName, a, b):
    with open(fileName, 'wb') as csvfile:
        writer = csv.writer(csvfile, dialect='excel')
        i = a
        while i <= b:
            writer.writerow(matrix[i])
            i = i + 1


# 写数据的一部分
def saveDataRowCol(matrix, fileName, a, b, c, d):
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
