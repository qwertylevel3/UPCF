# -*- coding: utf-8 -*-



from util import splitData
from CF import BaseCF
from util import kmeans


def main():
    kmeans.testKMeans()



# splitData.extractSample("data/ratings.csv")
# 5次实验，取平均值

#    mae0 = BaseCF.run("temp/BaseCF/test_0.csv",
#                  "temp/BaseCF/check_0.csv",
#                  "temp/BaseCF/forecast_0.csv",
#                  "temp/BaseCF/real_0.csv")




if __name__ == "__main__":
    main()
