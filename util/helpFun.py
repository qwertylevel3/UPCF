# coding:utf-8

import csv


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
