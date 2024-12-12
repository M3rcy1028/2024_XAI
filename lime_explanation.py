from sklearn.ensemble import RandomForestRegressor
from lime.lime_tabular import LimeTabularExplainer
import pickle
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import re

# 한글 폰트 설정
# plt.rcParams['font.family'] = 'NanumGothic'  # Windows
plt.rcParams['font.family'] = 'AppleGothic'  # Mac
mpl.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지

def signal_marking(code, pred: pd.Series, alpha, beta, start_date=None, end_date=None):
    # 가격 데이터 로드 및 기간 필터링
    df_price = pd.read_csv(f"data/price/{code}.csv", index_col=[0], parse_dates=True)['Close']
    df_price = df_price[pred.index]

    if start_date:
        df_price = df_price[df_price.index >= start_date]
        pred = pred[pred.index >= start_date]
    if end_date:
        df_price = df_price[df_price.index <= end_date]
        pred = pred[pred.index <= end_date]

    # 매수/매도 시그널 생성
    buy_signal = pd.Series([0] * len(pred), index=pred.index)
    sell_signal = pd.Series([0] * len(pred), index=pred.index)

    for date, date_pred in pred.items():
        if date_pred >= alpha:
            buy_signal[date] = 1
        if date_pred <= beta:
            sell_signal[date] = 1

    buy_signal = buy_signal[buy_signal == 1]
    sell_signal = sell_signal[sell_signal == 1]

    # 매수/매도 시그널 날짜 출력
    buy_dates = [date.strftime('%Y-%m-%d') for date in buy_signal.index]
    sell_dates = [date.strftime('%Y-%m-%d') for date in sell_signal.index]

    print("매수 시그널 날짜:")
    print(buy_dates)

    print("매도 시그널 날짜:")
    print(sell_dates)

    return buy_dates, sell_dates


def plot_lime(explanations, instance_dates, predictions, output_path):
    fig, axes = plt.subplots(2, 2, figsize=(18, 12))
    axes = axes.flatten()

    for i, (explanation, instance_date, prediction) in enumerate(zip(explanations, instance_dates, predictions)):
        lime_data = explanation.as_list()
        features = [
            ' '.join([word for word in re.split(r'[\s<><=]+', item[0]) if not re.match(r'^[-+]?\d*\.?\d+$', word)])
            for item in lime_data
        ]

        contributions = [item[1] for item in lime_data]
        positive_contrib = [c if c > 0 else 0 for c in contributions]
        negative_contrib = [c if c < 0 else 0 for c in contributions]

        signal = "매수" if prediction > 0 else "매도"

        axes[i].barh(features, positive_contrib, color='orange', label='Positive')
        axes[i].barh(features, negative_contrib, color='blue', label='Negative')
        axes[i].axvline(0, color='black', linewidth=0.5)
        axes[i].set_title(
            f'{instance_date}\n({signal}를 추천)'
        )
        axes[i].set_xlabel('기여도')
        if i % 2 == 0:
            axes[i].set_ylabel('피처')

    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])

    fig.tight_layout()
    plt.legend(loc='upper center', bbox_to_anchor=(-0.1, -0.1), ncol=2)
    plt.savefig(output_path)
    plt.close()
    print(f"Saved {output_path}!")

# code = '000660'
#
# # test할 csv 로드
# test_data = pd.read_csv(f'data/labeled/{code}.csv', parse_dates=['Date'], index_col='Date')
#
# # 모델 로드
# with open(f'model/{code}_model.pkl', 'rb') as f:
#     model: RandomForestRegressor = pickle.load(f)
#
# model_feature_names = model.feature_names_in_
#
# test_features = test_data[model_feature_names]
# test_labels = test_data.iloc[:, -1]
#
# pred = model.predict(test_features)
# sr_pred = pd.Series(pred, index=test_data.index)
#
# # 사용자가 지정한 날짜 기간
# start_date = "2022-02-01"
# end_date = "2023-07-06"
#
# # 매수/매도 시그널 시각화 및 날짜 반환
# buy_dates, sell_dates = signal_marking(code, sr_pred, 0.1, -0.05, start_date, end_date)
#
# # LIME 설명 생성
# explanations = []
# instance_dates = []
# predictions = []
# actual_labels = []
#
# signal_dates = list(set(buy_dates + sell_dates))
# signal_dates = sorted(signal_dates)[-4:]  # 최근 4개 데이터 선택
#
# explainer = LimeTabularExplainer(
#     test_features.values,
#     mode="regression",
#     feature_names=model_feature_names.tolist(),
#     verbose=True,
#     random_state=42
# )
#
# for signal_date in signal_dates:
#     instance_index = test_data.index.get_loc(signal_date)
#     instance = test_features.iloc[instance_index].values
#     instance_date = signal_date
#     prediction = model.predict([instance])[0]
#     actual = test_labels.iloc[instance_index]
#     explanation = explainer.explain_instance(instance, model.predict, num_features=5)
#
#     explanations.append(explanation)
#     instance_dates.append(instance_date)
#     predictions.append(prediction)
#
# output_file = 'result/lime_explanation.png'
# plot_lime(explanations, instance_dates, predictions, output_file)

def run_lime_analysis(code, start_date, end_date, alpha=0.1, beta=-0.05, output_file='result/lime_explanation.png'):
    print(f"Running LIME Analysis for code: {code}, Start Date: {start_date}, End Date: {end_date}")
    # test할 csv 로드
    test_data = pd.read_csv(f'data/labeled/{code}.csv', parse_dates=['Date'], index_col='Date')

    # 모델 로드
    with open(f'model/{code}_model.pkl', 'rb') as f:
        model: RandomForestRegressor = pickle.load(f)

    model_feature_names = model.feature_names_in_

    test_features = test_data[model_feature_names]
    test_labels = test_data.iloc[:, -1]

    pred = model.predict(test_features)
    sr_pred = pd.Series(pred, index=test_data.index)

    # 매수/매도 시그널 시각화 및 날짜 반환
    buy_dates, sell_dates = signal_marking(code, sr_pred, alpha, beta, start_date, end_date)

    # LIME 설명 생성
    explanations = []
    instance_dates = []
    predictions = []

    signal_dates = list(set(buy_dates + sell_dates))
    signal_dates = sorted(signal_dates)[-4:]  # 최근 4개 데이터 선택

    explainer = LimeTabularExplainer(
        test_features.values,
        mode="regression",
        feature_names=model_feature_names.tolist(),
        verbose=True,
        random_state=42
    )

    for signal_date in signal_dates:
        instance_index = test_data.index.get_loc(signal_date)
        instance = test_features.iloc[instance_index].values
        instance_date = signal_date
        prediction = model.predict([instance])[0]
        explanation = explainer.explain_instance(instance, model.predict, num_features=5)

        explanations.append(explanation)
        instance_dates.append(instance_date)
        predictions.append(prediction)

    plot_lime(explanations, instance_dates, predictions, output_file)
    return output_file
