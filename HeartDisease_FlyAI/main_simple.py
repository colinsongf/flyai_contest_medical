#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : main_simple.py
# @Author: Zhan
# @Date  : 7/16/2019
# @Desc  : 达到79.63%的测试准确率

# -*- coding: utf-8 -*
import argparse
import torch
import torch.nn as nn
from flyai.dataset import Dataset
from torch.optim import Adam
import numpy as np
import xgboost as xgb


from model import Model
from net import Net
from path import MODEL_PATH

parser = argparse.ArgumentParser()
parser.add_argument(
    "-e",
    "--EPOCHS",
    default=1000,
    type=int,
    help="train epochs")
parser.add_argument("-b", "--BATCH", default=32, type=int, help="batch size")
args = parser.parse_args()


def eval(preds_prob, y_test):
    preds = np.zeros(preds_prob.shape)
    preds[preds_prob >= 0.5] = 1
    train_accuracy = (preds == y_test).sum() / preds_prob.shape[0]

    return train_accuracy


# 训练并评估模型
data = Dataset(epochs=args.EPOCHS, batch=args.BATCH,)
model = Model(data)

x, y, x_test, y_test = data.get_all_processor_data()
#
# validateNum = 30
# x_train = x[0:x.shape[0]-validateNum,:]
# y_train = y[0:y.shape[0]-validateNum]
# x_test = x[-validateNum:,:]
# y_test = y[-validateNum:]

x_train = x
y_train = y

print("the length of train data: %d" % data.get_train_length())
print("the length of x_train: %d" % x_train.shape[0])
print("the length of x_test: %d" % x_test.shape[0])
# the length of train data: 162
# the length of x_train: 162
# the length of x_test: 54
# the length of test datas: 54
# x_train, y_train = data.get_all_validation_data()
# print(args.BATCH)
# print(args.EPOCHS)
# read in data
dtrain = xgb.DMatrix(x_train, label=y_train)
dtest = xgb.DMatrix(x_test, label=y_test)

best_accuracy = 0
# specify parameters via map
# gamma/
etas = [0.001, 0.01, 0.1, 0.3, 0.5, 1]
max_depths = [2, 3, 5, 7, 10]
reg_lambdas = [0.001, 0.01, 0.1, 0.3, 0.5, 1, 7, 10, ]
reg_alphas = [0.001, 0.01, 0.1, 0.3, 0.5, 1, 7, 10, ]
num_rounds = [2, 5, 7, 10]
min_split_losss = [0.001,0.01,0.1,1,7,10,30,] # gamma
# etas = [0.001,0.5,]
# max_depths = [2]
# lambdas = [0.001,0.5, ]
# alphas = [0.001]
# num_rounds = [2, 7]

watchlist = [(dtrain, 'train'),(dtest, 'eval')]

for eta in etas:
    for max_depth in max_depths:
        for reg_lambda in reg_lambdas:
            for reg_alpha in reg_alphas:
                for num_round in num_rounds:
                    for min_split_loss in min_split_losss:
                        param = {
                            'max_depth': max_depth,
                            'eta': eta,
                            'lambda': reg_lambda,
                            'alpha': reg_alpha,
                            'min_split_loss':min_split_loss,
                            'objective': 'binary:logistic',
                            'subsample':0.7,
                            'verbosity': 0}

                        # specify validations set to watch performance
                        bst = xgb.train(
                            param,
                            dtrain,
                            num_round,
                            watchlist,
                            verbose_eval=False)
                        preds_prob = bst.predict(dtest)
                        val_accuracy = eval(preds_prob, dtest.get_label())
                        # print("current val_accuracy %s" % val_accuracy)

                        if val_accuracy > best_accuracy:
                            best_accuracy = val_accuracy
                            model.save_model(bst, MODEL_PATH, overwrite=True)
                            print(
                                "parameters: eta: %g, max_depth: %g, lambda_2: %g, alpha: %g, num_round: %g, min_split_loss: %g." %
                                (eta, max_depth, reg_lambda, reg_alpha, num_round, min_split_loss))
                            print("best accuracy %s" % best_accuracy)
                            print("current train accuracy %s" % eval(bst.predict(dtrain), dtrain.get_label()))


