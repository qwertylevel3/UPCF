# -*- coding: utf-8 -*-


from CF import CF

from util import splitData
from util import path


# 将源数据切分
def extractSample():
    for i in range(0, 5):
        splitData.extractRatingSample(path.ratingFile,
                                      "temp/sample/check_" + str(i) + ".csv",
                                      "temp/sample/test_" + str(i) + ".csv")


def main():
    extractSample()

if __name__ == "__main__":
    main()
