import pickle
import pickle5
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
def get_level(lst):
  # X_train 경로
  path = '/content/drive/MyDrive/CP1/modeling/'
  X_train = pd.read_csv(path+'X_train.csv')
  # #모델 경로
  # model_path = 'C:/Users/User/Desktop/AIB_13/CP1/model/'

  model_path = '/content/drive/MyDrive/CP1/modeling/'
  #꼭 두개다 할 필요는 없음 에러나지 않고 정상적으로 작동하는 것만 채택
  # #pickle ver 4
  # with open(model_path + 'random_model_pickle_ver4.pickle', 'rb') as file:
  #   model = pickle.load(file)
  #pickle ver 5
  with open(model_path + 'random_model_pickle_ver5.pickle', 'rb') as file:
    model = pickle5.load(file)

  columns = X_train.columns
  
  data=pd.DataFrame(columns=columns, data=[lst])

  encoder = LabelEncoder()
  for column in columns:
    encoder.fit(X_train[column])
    data[column] = encoder.transform(data[column])

  predict = model.predict(data)

  return predict[0]