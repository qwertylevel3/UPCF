# -*- coding: utf-8 -*-



from util import splitData
from CF import CF


def main():
    #    splitData.extractSample("data/ratings.csv")
    # 5次实验，取平均值

    mae0 = CF.run("temp/sample/test_0.csv",
                  "temp/sample/check_0.csv",
                  "temp/sample/forecast_0.csv",
                  "temp/sample/real_0.csv")

    mae1 = CF.run("temp/sample/test_1.csv",
                  "temp/sample/check_1.csv",
                  "temp/sample/forecast_1.csv",
                  "temp/sample/real_1.csv")

    mae2 = CF.run("temp/sample/test_2.csv",
                  "temp/sample/check_2.csv",
                  "temp/sample/forecast_2.csv",
                  "temp/sample/real_2.csv")

    mae3 = CF.run("temp/sample/test_3.csv",
                  "temp/sample/check_3.csv",
                  "temp/sample/forecast_3.csv",
                  "temp/sample/real_3.csv")

    mae4 = CF.run("temp/sample/test_4.csv",
                  "temp/sample/check_4.csv",
                  "temp/sample/forecast_4.csv",
                  "temp/sample/real_4.csv")

    print (mae0+mae1+mae2+mae3+mae4)/5

if __name__ == "__main__":
    main()
