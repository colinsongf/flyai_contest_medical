# -*- coding: utf-8 -*
import sys
import os

# 训练数据的路径
DATA_PATH = os.path.join(sys.path[0], 'data', 'input')
# 模型保存的路径
MODEL_PATH = os.path.join(sys.path[0], 'data', 'output', 'model')
# 训练log的输出路径
LOG_PATH = os.path.join(sys.path[0], 'data', 'output', 'logs')

QUE_DICT_FILE = os.path.join(DATA_PATH, 'que.dict')
ANS_DICT_FILE = os.path.join(DATA_PATH, 'ans.dict')

QA_MODEL_DIR = "medicalQABot.h5"

