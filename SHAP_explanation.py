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
import csv
import os

# 한글 폰트 설정
if platform.system() == 'Windows':
    plt.rcParams['font.family'] = 'Malgun Gothic'
elif platform.system() == 'Darwin':  # macOS
    plt.rcParams['font.family'] = 'AppleGothic'
mpl.rcParams['axes.unicode_minus'] = False

shaplist = [] # SHAP 중요도 순서 리스트
stockindex = [] #주가 지표 리스트
f_s = [] #재무제표 리스트


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


def run_shap_analysis(code, data, output_file='result/SHAP_bar_result.png'):
    data_len = len(data)

    # 데이터 분할 및 모델 학습
    train_data = data.iloc[:int(data_len * 0.6), 1:]
    rgr = RandomForestRegressor()
    rgr = rgr.fit(train_data.iloc[:, :-1], train_data.iloc[:, -1])

    X = train_data.iloc[:, :-1]
    explainer = shap.Explainer(rgr, X)
    shap_values = explainer(X, check_additivity=False)

    # SHAP 값 계산 및 정렬 (절대값 사용하지 않음)
    mean_shap_values = shap_values.values.mean(axis=0)
    sorted_indices = np.argsort(np.abs(mean_shap_values))
    sorted_features = X.columns[sorted_indices]

    # SHAP 중요도 평균 절댓값 계산
    shap_importance = shap_values.abs.mean(axis=0).values

    # 중요도 순서를 나타내는 피처 이름 정렬
    feature_names = X.columns
    shap_importance_dict = dict(zip(feature_names, shap_importance))

    # 정렬된 피처를 shaplist에 하나씩 추가
    for feature in sorted(shap_importance_dict, key=shap_importance_dict.get, reverse=True):
        shaplist.append(feature)
    

    top_features = shaplist[:5]  # 상위 5개 피처 이름

    top_shap_values = [mean_shap_values[X.columns.get_loc(feature)] for feature in top_features]  # top_features에 맞는 SHAP 값 추출

    # SHAP 값에 따른 색상 계산
    feature_colors = calculate_feature_colors(top_features, shap_values, X, mean_shap_values)
    
    # SHAP 바 그래프 저장
    plt.figure(figsize=(8, 5))  # 저장을 위한 전체 그래프 크기 설정
    plt.barh(
        top_features[::-1],
        top_shap_values[::-1],
        color=feature_colors[::-1],
    )
    plt.xlabel("Mean SHAP Value")
    plt.ylabel("Features")
    plt.title("Top 5 SHAP Feature Importances")
    plt.tight_layout()
    plt.savefig(output_file, bbox_inches='tight')  # 그래프 저장
    plt.close()
    print(f"SHAP bar graph saved to: {output_file}")

    # shap.summary_plot(shap_values, X)
    return output_file




def show_chart(code, start_date, end_date, output_chart='result/SHAP_char_result.png'):
    # stockindex 생성
    for item in shaplist:
        if item in ['sma_10', 'sma_20', 'sma_60', 'ema_10', 'ema_20', 'ema_60']:
            stockindex.append(item)
        else:
            f_s.append(item)

    # 데이터 로드 및 날짜 필터링
    df = pd.read_csv(f"data/price/{code}.csv", parse_dates=["Date"], index_col="Date")
    filtered_data = df[(df.index >= start_date) & (df.index <= end_date)]

    # Close 데이터와 stockindex 중 앞 3개 값만 사용
    selected_columns = ["Close"] + stockindex[:3]
    filtered_data = filtered_data[selected_columns]

    # 그래프 그리기
    plt.figure(figsize=(12, 6))
    for column in stockindex[:3]:
        plt.plot(filtered_data.index, filtered_data[column], label=column, linestyle='--')
    plt.plot(filtered_data.index, filtered_data["Close"], label="Close Price", color='red', linestyle='-')

    # 그래프 설정 및 저장
    plt.title(f"{code} Stock Chart ({start_date} - {end_date})")
    plt.xlabel("Date")
    plt.ylabel("Price (KRW)")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig(output_chart)
    plt.close()
    print(f"Stock chart saved to: {output_chart}")


def show(code, start_date, end_date):
    # 결과 저장 경로
    output_bar = 'result/SHAP_bar_result.png'
    output_chart = 'result/SHAP_char_result.png'

    # 폴더 생성 (없을 경우)
    os.makedirs('result', exist_ok=True)

    # SHAP 분석 및 저장
    run_shap_analysis(code, load_and_filter_data(code, start_date, end_date), output_bar)
    print("SHAP:",shaplist[:5])
    selected_features = shaplist[:5]

        # CSV 파일에서 설명을 딕셔너리에 담기
    explanation_dict = {}
    with open('data/feature_explain.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) < 2:
                continue
            feature = row[0].strip()
            explanation = row[1].strip()

            if feature in selected_features:
                explanation_dict[feature] = explanation

    print(f"Selected: {selected_features}")
    print(f"Selected2: {explanation_dict}")

    # 선 그래프 생성 및 저장
    show_chart(code, start_date, end_date, output_chart)

    return output_bar, output_chart, explanation_dict

def calculate_color_from_values(feature_values, shap_values):

    norm = plt.Normalize(vmin=np.min(feature_values), vmax=np.max(feature_values))  # 정규화

    # 양수와 음수 SHAP 값 분리
    positive_mask = shap_values > 0
    negative_mask = shap_values < 0

    # 평균값 계산
    positive_mean = feature_values[positive_mask].mean() if np.any(positive_mask) else 0
    negative_mean = feature_values[negative_mask].mean() if np.any(negative_mask) else 0

    # 평균값에 따라 색상 결정
    positive_color = plt.cm.coolwarm(norm(positive_mean))
    negative_color = plt.cm.coolwarm(norm(negative_mean))

    return positive_color, negative_color

def calculate_feature_colors(top_features, shap_values, X, mean_shap_values):
    feature_colors = []

    for feature in top_features:
        feature_index = X.columns.get_loc(feature)
        feature_shap_values = shap_values.values[:, feature_index]
        feature_values = X.iloc[:, feature_index].values

        # 양수와 음수 색상 계산
        positive_color, negative_color = calculate_color_from_values(feature_values, feature_shap_values)

        if mean_shap_values[feature_index] > 0:
            feature_colors.append(positive_color)
        else:
            feature_colors.append(negative_color)
    
    return feature_colors


# show("005930", "2022-07-01", "2024-07-01")