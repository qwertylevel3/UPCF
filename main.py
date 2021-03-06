# -*- coding: utf-8 -*-



from util import splitData
from util import mycsv
from CF.UPCF import UPCF
from CF.FuckCF import FuckCF
from CF import BaseCF
import multiprocessing
from evaluate import evaluate
from util import cluster
from util import neighbor

from util import path


def runFuckCF():
    print("run start")

    allData = mycsv.readCSVnoTitle(path.smallSampleDir + "test_0.csv")
    checkData = mycsv.readCSV(path.smallSampleDir + "check_0.csv")
#    allData=mycsv.readCSV("data/input/old/test_0.csv")
#    checkData=mycsv.readCSV("data/input/old/check_0.csv")


    print("read allData over")

    cf = FuckCF(allData, checkData)

    print("init upcf over")

    print(cf.runMuliprocess(4))


def runUPCFMuli():
    print("run start")
    allData = mycsv.readCSVnoTitle(path.smallSampleDir + "test_0.csv")
    checkData = mycsv.readCSV(path.smallSampleDir + "check_0.csv")

    print("read allData over")

    cf = UPCF(allData, checkData)

    print("init upcf over")

    print(cf.runMuliprocess(4))


def runUPCF():
    print("run start")
    allData = mycsv.readCSVnoTitle(path.smallSampleDir + "test_0.csv")
    checkData = mycsv.readCSV(path.smallSampleDir + "check_0.csv")
    print("read allData over")

    cf = UPCF(allData, checkData)

    print("init upcf over")

    print(cf.run())


def makeSmallData():
    splitData.extractSample(path.smallOriDir + "ratings.csv", path.smallSampleDir)


def makeOldSmallData():
    splitData.extractSample("data/input/old/rattingsSmall.csv",
                            "data/input/old/")


def runBaseCF():
    print(BaseCF.run(
        path.smallSampleDir + "test_0.csv",
        path.smallSampleDir + "check_0.csv",
        "data/output/BaseCF/forecastData.csv",
        "data/output/BaseCF/realData.csv"
    ))


def main():
    runFuckCF()




    # splitData.extractSample("data/ratings.csv")
    # 5次实验，取平均值

    #    mae0 = BaseCF.run("output/BaseCF/test_0.csv",
    #                  "output/BaseCF/check_0.csv",
    #                  "output/BaseCF/forecast_0.csv",
    #                  "output/BaseCF/real_0.csv")


if __name__ == "__main__":
    main()
