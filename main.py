# -*- coding: utf-8 -*-



from util import splitData
from util import mycsv
from CF.UPCF import UPCF
from CF import BaseCF


def run():
    print("run start")
    allData = mycsv.readCSVnoTitle("output/small/test_0.csv")
    print("read allData over")

    cf = UPCF(allData)
    print("init upcf over")
    print cf.run(
        "output/small/check_0.csv",
        "output/UPCF/forecast_0.csv",
        "output/UPCF/real_0.csv"
    )


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
