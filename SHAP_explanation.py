import shap  
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import pickle
import matplotlib.pyplot as plt
import matplotlib as mpl
import platform
from time import sleep
from tqdm import tqdm
import FinanceDataReader as fdr
from stockstats import wrap
from FinDataLoader import FinDataLoader
from datetime import datetime
import pandas as pd


# 한글 폰트 설정
if platform.system() == 'Windows':
    plt.rcParams['font.family'] = 'Malgun Gothic'
elif platform.system() == 'Darwin':  # macOS
    plt.rcParams['font.family'] = 'AppleGothic'
mpl.rcParams['axes.unicode_minus'] = False



def load_and_filter_data(code, start_date, end_date):
    data_loader = FinDataLoader(path="data")  # 경로 지정
    data = data_loader(code=code, day_after=30)  # 데이터 로드
    
    # 날짜 인덱스를 datetime 형식으로 변환
    data.index = pd.to_datetime(data.index)
    
    # 날짜 필터링
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    
    filtered_data = data[(data.index >= start_date) & (data.index <= end_date)]
    
    return filtered_data





def run_shap_analysis(code, data):
    data_len = len(data)

    train_data = data.iloc[:int(data_len * 0.6), 1:]
    rgr = RandomForestRegressor()
    rgr = rgr.fit(train_data.iloc[:,:-1],train_data.iloc[:,-1])

    with open(f'model/{code}_model_shap.pkl', 'wb') as f:
        pickle.dump(rgr, f)


    X = train_data.iloc[:, :-1]
    explainer = shap.Explainer(rgr, X)
    shap_values = explainer(X, check_additivity=False)


    mean_shap_values = np.abs(shap_values.values).mean(axis=0)  # 절대값의 평균
    sorted_indices = np.argsort(-mean_shap_values)  # 중요도 순으로 정렬
    sorted_features = X.columns[sorted_indices]  # 정렬된 피처 이름
    sorted_shap_values = shap_values.values[:, sorted_indices]  # 정렬된 SHAP 값

    shaplist = []
    for feature, importance in zip(sorted_features[:10], mean_shap_values[sorted_indices][:10]): 
        shaplist.append(feature)

    print(shaplist[:3])
    shap.summary_plot(shap_values, X, plot_type="dot")


data1 = load_and_filter_data('005930', '2016-02-01', '2022-01-01')
run_shap_analysis('005930', data1)
