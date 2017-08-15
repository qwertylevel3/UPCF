# -*- coding: utf-8 -*-



from util import splitData
from util import mycsv
from CF.UPCF import UPCF
from CF import BaseCF


def run():
    allData = mycsv.readCSVnoTitle("smallData/ratings.csv")

    cf = UPCF(allData)
    print cf.run(
        "output/check_2.csv",
        "output/UPCF/forecast_2.csv",
        "output/UPCF/real_2.csv"
    )


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
