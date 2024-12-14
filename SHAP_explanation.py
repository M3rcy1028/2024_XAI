import shap  
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from FinDataLoader import FinDataLoader
import pickle
import matplotlib.pyplot as plt
plt.rcParams['font.family'] ='Malgun Gothic'
plt.rcParams['axes.unicode_minus'] =False


DL = FinDataLoader()
code = '035720'


data = DL(code, 30)
data_len = len(data)

train_data = data.iloc[:int(data_len * 0.6), 1:]
valid_data = data.iloc[int(data_len * 0.6):int(data_len * 0.8), 1:]
test_data = data.iloc[int(data_len * 0.8):, 1:]


with open(f'{code}_model.pkl', 'rb') as f:
    rgr = pickle.load(f)

X = train_data.iloc[:, :-1]



# SHAP 분석----------------------

explainer = shap.Explainer(rgr, X)
shap_values = explainer(X, check_additivity=False)


mean_shap_values = np.abs(shap_values.values).mean(axis=0)  # 절대값의 평균
sorted_indices = np.argsort(-mean_shap_values)  # 중요도 순으로 정렬
sorted_features = X.columns[sorted_indices]  # 정렬된 피처 이름
sorted_shap_values = shap_values.values[:, sorted_indices]  # 정렬된 SHAP 값

# 상위 피처 이름 출력
shaplist = []
for feature, importance in zip(sorted_features[:10], mean_shap_values[sorted_indices][:10]): 
    shaplist.append(feature)
    # print(f"{feature}: {importance}")


print(shaplist[:3])


# 상위 10개 피처의 SHAP 값 시각화
# shap.summary_plot(shap_values[:, top_10_indices], X[top_10_features], plot_type="bar")
shap.summary_plot(shap_values, X, plot_type="dot")
