from sklearn.ensemble import RandomForestRegressor
from lime.lime_tabular import LimeTabularExplainer
import pickle
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import re
import platform

# 한글 폰트 설정
if platform.system() == 'Windows':
    plt.rcParams['font.family'] = 'NanumGothic'
elif platform.system() == 'Darwin':  # macOS
    plt.rcParams['font.family'] = 'AppleGothic'
mpl.rcParams['axes.unicode_minus'] = False


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


def run_lime_analysis(code, start_date, end_date, alpha=0.1, beta=-0.05, output_file='result/lime_explanation.png'):
    print(f"Code: {code}, Start Date: {start_date}, End Date: {end_date}")
    test_data = pd.read_csv(f'data/labeled/{code}.csv', parse_dates=['Date'], index_col='Date')

    # 모델 로드
    with open(f'model/{code}_model.pkl', 'rb') as f:
        model: RandomForestRegressor = pickle.load(f)

    model_feature_names = model.feature_names_in_

    test_features = test_data[model_feature_names]

    pred = model.predict(test_features)
    sr_pred = pd.Series(pred, index=test_data.index)

    buy_dates, sell_dates = signal_marking(code, sr_pred, alpha, beta, start_date, end_date)

    if not buy_dates and not sell_dates:
        print("해당 기간 내에는 매수/매도 시그널이 없음")
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.text(0.5, 0.5, "해당 기간 내에는 매수/매도 시그널이 없음", fontsize=20, ha='center', va='center')
        ax.axis('off')
        plt.savefig(output_file)
        plt.close()
        return output_file

    # LIME 설명 생성
    explanations = []
    instance_dates = []
    predictions = []
    selected_features = []

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

        lime_data = explanation.as_list()
        lime_features = [
            ' '.join([word for word in re.split(r'[\s<><=]+', item[0]) if not re.match(r'^[-+]?\d*\.?\d+$', word)])
            for item in lime_data
        ]
        selected_features.append(lime_features)

        explanations.append(explanation)
        instance_dates.append(instance_date)
        predictions.append(prediction)

    selected_features = list(set(feature for sublist in selected_features for feature in sublist))
    plot_lime(explanations, instance_dates, predictions, output_file)

    print(f"Selected: {selected_features}")

    return output_file, selected_features
