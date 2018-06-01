from sklearn.linear_model import Ridge

import dataset.setbuilder as sb
import models.sklearn.evaluator as eval
import evaluation.evaluation as ev_cust
from preprocessing import preprocessing_utils as preu
from sklearn.pipeline import make_pipeline
import dataset.dataset as ds
import dataset.utility as utils
from sklearn import linear_model
from sklearn import ensemble
from sklearn import tree
import numpy as np
from inspect import getmembers
import preprocessing.imputation as imp
import pandas
import models.sklearn.sklearnlinearclass as skc
from sklearn.preprocessing import PolynomialFeatures


def model():
    return linear_model.Ridge(alpha=200)


if __name__ == '__main__':
    datas = ds.read_dataset("best_for_customers.csv")
    datas = preu.mean_cust_per_shop_if_promotions(datas, utils.get_frame_in_range(datas, 3, 2016, 12, 2017))
    datas = preu.mean_cust_per_shop_if_holiday(datas, utils.get_frame_in_range(datas, 3, 2016, 12, 2017))
    datas = sb.SetBuilder(target='NumberOfCustomers', autoexclude=True, df=datas)\
        .exclude('NumberOfSales', 'Month')\
        .build()
    n = 10
    mods = []
    for i in range(n):
        print(i+1)
        x, y = datas.random_sampling(1.0)
        mod = skc.LinearSklearn(1, model)
        mod.train(x, y)
        mods.append(mod)
        p = mod.predict(x).squeeze()
        print("TRAIN R2: ", eval.r2_score(y, p))
        print("TEST R2: ", eval.r2_score(datas.yts, mod.predict(datas.xts)))
        print("##########################")


    preds = []
    for i in range(n):
        preds.append(mods[i].predict(datas.xts))

    custpred = np.array(preds).mean(axis=0)

    print("TEST R2: ", eval.r2_score(datas.yts, custpred))

    new = pandas.DataFrame()
    new['NumberOfCustomers'] = pandas.Series(custpred)
    ds.save_dataset(new, "cust_ensemble_predictions9.csv")
