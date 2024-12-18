from module import *
from openCSV import getData, getLabel
from sklearn.ensemble import RandomForestRegressor
import pickle
import numpy as np

def StockChart(stockname, startdate, enddate, 
                close=0, method='plotLineChart', 
                openpath = './stock_csv/', savepath = './result/'):
    # get data info
    title, path, sdate, edate = getData(stockname, startdate, enddate)
    # read .csv file
    df = pd.read_csv(openpath + path + ".csv")
    df['Date'] = pd.to_datetime(df['Date'])
    ##
    if method == 'plotLineChart':
        plotLineChart(df, title, sdate, edate)
        printINFO(stockname, sdate, edate)
    if method == 'mplfinance':
        mplfinanceChart(df, title, sdate, edate)
        printINFO(stockname, sdate, edate)
    elif method == 'lightweight':
        print('lightweightChart')
        return lightweightChart(df, title, sdate, edate)

# https://pypi.org/project/lightweight-charts/
# https://github.com/louisnw01/lightweight-charts-python
def lightweightChart(df, title, sdate, edate):
    filtered_df = df[(df['Date'] >= pd.to_datetime(sdate)) 
                    & (df['Date'] <= pd.to_datetime(edate))]
    # chart design
    chart = Chart(title=title + ' Candle Chart', toolbox=True)
    chart.grid(vert_enabled = True, horz_enabled = True)
    chart.layout(
        background_color='#131722', 
        #font_family='Trebuchet MS', 
        font_size = 16
    )
    # display ohlc, ratio of percentage (%)
    chart.legend(visible=True, ohlc=True, percent=True)
    chart.set(filtered_df)
    # create SMA 20 line
    sma20_line = chart.create_line(
        color='#ffeb3b', 
        width=1, 
        price_label=True
    )
    sma20 = pd.DataFrame({
        'Date': filtered_df['Date'],
        'Value': filtered_df['Close'].rolling(window=20).mean()
    })
    sma20_line.set(sma20.dropna())
    # create SMA 50 line
    sma50_line = chart.create_line(
        color='#26c6da', 
        width=1, 
        price_label=True
    )
    sma50 = pd.DataFrame({
        'Date': filtered_df['Date'],
        'Value': filtered_df['Close'].rolling(window=50).mean()
    })
    sma50_line.set(sma50.dropna())
    sma20_line.legend = "SMA 20"
    sma50_line.legend = "SMA 50"
    return chart # return object

def plotLineChart(df, stockname, sdate, edate, outputfile = './result/StockChart.png'):
    label_title, label_code, label_sdate, label_edate = getLabel(stockname, sdate, edate)

    # read .csv file
    label_df = pd.read_csv('./data/labeled/' + label_code + '.csv')
    label_df.set_index('Date', inplace=True)
    label_df.index = pd.to_datetime(label_df.index)
    label_df = label_df.sort_index()

    # sdate 기준 30 거래일 전 데이터부터 필터링
    if label_sdate < sdate:
        sdate = pd.to_datetime(sdate)
    else:
        sdate = pd.to_datetime(label_sdate)
    if label_edate < edate:
        edate = pd.to_datetime(label_edate)
    else:
        edate = pd.to_datetime(edate)
    sdate_index = label_df.index.get_indexer([sdate], method='nearest')[0]

    # 30 거래일 전 인덱스 확인
    if sdate_index - 30 >= 0:  # 인덱스 범위 확인
        sdate_30days_before = label_df.index[sdate_index - 30]
    else:
        raise ValueError("Not enough data to go 30 trading days before sdate.")

    # edate 기준 30 거래일 전 인덱스 확인
    edate_index = label_df.index.get_indexer([edate], method='nearest')[0]

    if edate_index + 30 < len(label_df.index):  # 인덱스 범위 확인
        edate_30days_before = label_df.index[edate_index - 30]
    else:
        raise ValueError("Not enough data to go 30 trading days after edate.")


    filtered_label_df = label_df.loc[sdate_30days_before:edate_30days_before]

    # Original data filtering
    df.set_index('Date', inplace=True)
    df.index = pd.to_datetime(df.index)

    # actual_df: 실제 종가만 sdate ~ edate
    output_actual_df = df.loc[sdate:edate, ['Close']].copy()
    actual_df_shifted = df.loc[sdate_30days_before:edate].shift(30).dropna()

    # 모델 로드
    with open(f'model/{label_code}_model.pkl', 'rb') as f:
        model: RandomForestRegressor = pickle.load(f)

    model_feature_names = model.feature_names_in_
    test_features = filtered_label_df[model_feature_names]
    pred = model.predict(test_features)

    predicted_close = actual_df_shifted['Close'].iloc[:len(pred)] * (1 + np.array(pred))

    # predict_df 구성: 예측 종가 저장
    predict_df = pd.DataFrame(index=actual_df_shifted.index[:len(pred)])
    predict_df['Predicted_Close'] = predicted_close

    # 결과 확인 및 그래프 시각화
    plt.figure(figsize=(12, 6))

    # 실제 종가
    plt.plot(output_actual_df.index, output_actual_df['Close'], label='Actual Close Price', color='r', linewidth=2, linestyle='--')

    # 예측 종가
    plt.plot(predict_df.index, predict_df['Predicted_Close'], label='Predicted Close', color='g', linewidth=2)

    plt.title(label_title + f" ({sdate} - {edate})")
    plt.xlabel('Date')
    plt.ylabel('Price (KRW)')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.legend(loc='best')

    # Save and Show
    plt.tight_layout()
    plt.savefig(outputfile, dpi=600)

def mplfinanceChart(df, title, sdate, edate, 
                    outputfile = './result/StockChart.png'):
    df.set_index('Date', inplace=True)
    filtered_df = df.loc[sdate:edate] 
    title = title + " (" + str(sdate) + ' - ' + str(edate) + ")"
    # image setting
    style = mpf.make_mpf_style(base_mpf_style='yahoo', gridcolor='lightgrey')
    mpf.plot(
        filtered_df,
        type='candle',        # candle chart
        mav=(10, 20),         # 이동평균선 (10일, 20일)
        volume=True,          # 거래량 추가
        title=title,
        style=style,
        figsize=(12, 6),      # 가로로 긴 비율 설정
        figratio=(12, 6),     # 그래프의 가로/세로 비율 조정
        figscale=1.5,         # 그래프 크기 확대
        savefig=dict(fname=outputfile, dpi=600, pad_inches=0.4, bbox_inches='tight')  # 고해상도로 저장
    )


def printINFO(name, sdate, edate):
    print("==================================================")
    print("## [Stock]  " + name)
    print("## [Period] FROM <" + str(sdate) + "> TO <" + str(edate) + ">")
    # print("## <" + file + "> successfully created")
    print("==================================================")

