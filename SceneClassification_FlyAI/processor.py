# -*- coding: utf-8 -*

import numpy
from flyai.processor.base import Base
import os
import cv2
from path import DATA_PATH
import numpy as np

'''
把样例项目中的processor.py件复制过来替换即可
'''
# 所有类别， label_list这里不需要修改
label_list = ['apron', 'bare-land', 'baseball-field', 'basketball-court', 'beach', 'bridge', 'cemetery', 'church', 'commercial-area', 'desert', 'dry-field', 'forest', 'golf-course', 'greenhouse', 'helipad', 'ice-land', 'island', 'lake', 'meadow', 'mine', 'mountain', 'oil-field', 'paddy-field', 'park', 'parking-lot', 'port', 'railway', 'residential-area', 'river', 'road', 'roadside-parking-lot', 'rock-land', 'roundabout', 'runway', 'soccer-field', 'solar-power-plant', 'sparse-shrub-land', 'storage-tank', 'swimming-pool', 'tennis-court', 'terraced-field', 'train-station', 'viaduct', 'wind-turbine', 'works']
label_num = len(label_list)
img_size = [224, 224]

class Processor(Base):

    '''
    参数为csv中作为输入x的一条数据，该方法会被dataset.next_train_batch()
    和dataset.next_validation_batch()多次调用。可在该方法中做数据增强
    该方法字段与app.yaml中的input:->columns:对应
    '''
    def input_x(self, img_path):
        # 根据 img_path 读取图片
        img_path = os.path.join(DATA_PATH, img_path)
        img = cv2.imread(img_path)
        img = cv2.resize(img, (img_size[0], img_size[1]))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return img

    '''
    参数为csv中作为输入y的一条数据，该方法会被dataset.next_train_batch()
    和dataset.next_validation_batch()多次调用。
    该方法字段与app.yaml中的output:->columns:对应
    '''
    def input_y(self, label):
        # 将label转换成 one-hot
        label_onehot = np.zeros((label_num), dtype=int)
        index = label_list.index(label)
        label_onehot[index] = 1
        return label_onehot

    '''
    参数为csv中作为输入x的一条数据，该方c法会被dataset.next_train_batch()
    和dataset.next_validation_batch()多次调用。评估的时候会调用该方法做数据处理
    该方法字段与app.yaml中的input:->columns:对应
    '''

    '''
    输出的结果，会被dataset.to_categorys(data)调用
    '''
    def output_y(self, pred_onehot_label):
        # 将预测的 one-hot类型的输出转换成 具体类别
        pred_onehot_label = pred_onehot_label[0]
        pred_index = np.argmax(pred_onehot_label)
        pred_label = label_list[pred_index]
        return pred_label
