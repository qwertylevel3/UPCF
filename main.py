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


if __name__ == "__main__":
    main()
