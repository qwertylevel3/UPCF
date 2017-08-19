# -*- coding: utf-8 -*-



from util import splitData
from util import mycsv
from CF.UPCF import UPCF
import multiprocessing
from evaluate import evaluate


def run():
    print("run start")
    allData = mycsv.readCSVnoTitle("output/small/test_0.csv")
    print("read allData over")

    cf = UPCF(allData)
    print("init upcf over")
    checkData = mycsv.readCSV("output/small/check_0.csv")
    pool = multiprocessing.Pool(processes=4)

    result = pool.map(cf.forecastJob, checkData)

    realValue = []
    forecastValue = []
    forecastMatrix = []
    realMatrix = []

    for r in result:
        f=r["f"]
        if f>0:
            forecastValue.append(r["f"])
            realValue.append(r["r"])
            forecastMatrix.append(r["fd"])
            realMatrix.append(r["rd"])
    print(evaluate.getMAE(forecastValue, realValue))


def makeData():
    splitData.extractSample("smallData/ratings.csv")


def main():
    run()







    # splitData.extractSample("data/ratings.csv")
    # 5次实验，取平均值

    #    mae0 = BaseCF.run("output/BaseCF/test_0.csv",
    #                  "output/BaseCF/check_0.csv",
    #                  "output/BaseCF/forecast_0.csv",
    #                  "output/BaseCF/real_0.csv")


if __name__ == "__main__":
    main()
