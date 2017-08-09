# -*- coding: utf-8 -*-


# 计算MAE值,对预测结果评价,MAE值越低越好
def getMAE(p, r):
    N = len(p)
    tempUp = 0.0
    for i in range(0, N):
        tempUp += abs(p[i] - r[i])
    return tempUp / N
