from module import *
from openCSV import getData

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

def plotLineChart(df, title, sdate, edate, 
                    outputfile = './result/StockChart.png'):
    # data filtering
    df.set_index('Date', inplace=True)
    filtered_df = df.loc[sdate:edate]
    title = title + " (" + str(sdate) + ' - ' + str(edate) + ")"
    # Plotting
    plt.figure(figsize=(12, 6)) 
    # Close
    plt.plot(filtered_df.index, filtered_df['Close'], label='Close Price', color='r', linewidth=2, linestyle='--') 
    # Open
    plt.plot(filtered_df.index, filtered_df['Open'], label='Open Price', color='b', linewidth=2, linestyle='--') 
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel('Price (KRW)')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.legend(loc='best')
    # save file
    plt.tight_layout()
    plt.savefig(outputfile, dpi=600)  
    # plt.show()

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

