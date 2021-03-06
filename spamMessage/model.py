# -*- coding: utf-8 -*
import os

import tensorflow as tf
from flyai.model.base import Base
from tensorflow import keras
from tensorflow.python.saved_model import tag_constants

from path import MODEL_PATH
from processor import Processor

TENSORFLOW_MODEL_DIR = "dpNet.ckpt"

def create_model(vocab_size):
    # region 模型超参数
    e_dim = 200
    filters_num = 64
    kernel_size = 5

    fc1_dim = 128
    drop_ratio = 0.2

    # endregion

    model = keras.Sequential()
    model.add(keras.layers.Embedding(vocab_size, e_dim))
    model.add(keras.layers.Conv1D(filters_num,kernel_size))
    model.add(keras.layers.GlobalAveragePooling1D())
    model.add(keras.layers.Dense(fc1_dim, activation=tf.nn.relu))
    model.add(keras.layers.Dropout(rate=drop_ratio))
    model.add(keras.layers.Dense(1, activation=tf.nn.sigmoid))

    model.summary()

    model.compile(optimizer=tf.train.AdamOptimizer(),
                  loss='binary_crossentropy',
                  metrics=['accuracy'])

    return  model

class Model(Base):
    def __init__(self, data,):
        self.data = data
        self.model_path = os.path.join(MODEL_PATH, TENSORFLOW_MODEL_DIR)
        self.vocab_size = Processor().getWordsCount()
        self.dpNet = create_model(self.vocab_size)
        if os.path.isfile(self.model_path):
            self.dpNet.load_weights(self.model_path)

    def predict(self, **data):
        '''
        使用模型
        :param path: 模型所在的路径
        :param name: 模型的名字
        :param data: 模型的输入参数
        :return:
        '''
        # latest = tf.train.latest_checkpoint(self.model_path)
        x_data = self.data.predict_data(**data)
        predict = self.dpNet.predict_classes(x_data)
        predict = self.data.to_categorys(predict)
        return predict

    def predict_all(self, datas):
        # latest = tf.train.latest_checkpoint(self.model_path)
        predicts = []
        for data in datas:
            x_data = self.data.predict_data(**data)
            predict = self.dpNet.predict_classes(x_data)
            predict = self.data.to_categorys(predict)
            predicts.append(predict)

        return predicts
