import os
import pandas as pd
from fancyimpute import SoftImpute
import FinanceDataReader as fdr
from stockstats import wrap
from time import sleep
from tqdm import tqdm

class FinDataLoader:
    def __init__(self,path="data"):
        self.path = path
        self.stock_list = {}
        
        with open(f"{path}/kospi_50.txt", 'r') as f:
            for line in f:
                code, name = line.strip().split(',')
                self.stock_list[code] = name
                
    def __call__(self,code,day_after):
        data = pd.read_csv(f"{self.path}/labeled/{code}.csv",index_col=[0])
        data.drop(columns=['연도','분기'],inplace=True)
        
        return data
                
    def get_statement(self, code, year, quarter):
        
        if os.path.isfile(f"{self.path}/{code}.csv"):
            df_fs = pd.read_csv(f"{self.path}/{code}.csv")
            
            df_fs = df_fs[df_fs['분기'] == quarter]
            df_fs = df_fs[df_fs['연도'] == year]
            
            return df_fs
        else:
            print(f"파일이 존재하지 않습니다: {self.path}/{code}.csv")
            return pd.DataFrame()
        
    def load_price_data(self):
        for code,_ in tqdm(self.stock_list.items()):
            sleep(0.2)
            
            df_ta = pd.DataFrame()
            
            df_price = fdr.DataReader(code,"2015-01-01")
            
            close = df_price['Close']
            
            df_stat = wrap(df_price)
            
            df_ta['Close'] = close
            df_ta['sma_10'] = df_stat['close_10_sma']/close
            df_ta['sma_20'] = df_stat['close_20_sma']/close
            df_ta['sma_60'] = df_stat['close_60_sma']/close
            df_ta['ema_10'] = df_stat['close_10_ema']/close
            df_ta['ema_20'] = df_stat['close_20_ema']/close
            df_ta['ema_60'] = df_stat['close_60_ema']/close
            
            df_ta.to_csv(f"{self.path}/price/{code}.csv", encoding='utf-8-sig')
            
    # 샘플 데이터 구조 기반 매핑 코드 설계
    def map_financial_to_price(self):
        for code,_ in tqdm(self.stock_list.items()):
            price_data = pd.read_csv(f"{self.path}/price/{code}.csv")
            financial_data = pd.read_csv(f"{self.path}/preprocessed/{code}.csv")
            
            # 날짜 및 분기 처리
            price_data['연도'] = pd.to_datetime(price_data['Date']).dt.year
            price_data['분기'] = (pd.to_datetime(price_data['Date']).dt.month - 1) // 3 + 1
            price_data['분기'] = "Q" + price_data['분기'].astype(str)
            
            # 매핑 진행 (외부 합병)
            merged_data = pd.merge(price_data, financial_data, how='left', on=['연도', '분기'])
            merged_data.dropna().to_csv(f"{self.path}/merged/{code}.csv",index=False, encoding='utf-8-sig')
            
    def labeling(self, day_after):
        if os.path.exists(f"{self.path}/labeled") is False:
            os.mkdir(f"{self.path}/labeled")
            
        if os.path.exists(f"{self.path}/labeled") is False:
            os.mkdir(f"{self.path}/labeled")
            
        for code,_ in tqdm(self.stock_list.items()):
            close_data = pd.read_csv(f"{self.path}/price/{code}.csv",index_col = [0])['Close']
            merged_data = pd.read_csv(f"{self.path}/merged/{code}.csv",index_col = [0])
            
            change_data = close_data.pct_change(day_after).shift(-day_after)
            
            merged_data['label'] = change_data.dropna()
            
            merged_data.dropna().to_csv(f"{self.path}/labeled/{code}.csv",encoding='utf-8-sig')
    
        
    def data_processing(self, code):
        if os.path.isfile(f"{self.path}/{code}.csv"):
            df_fs = pd.read_csv(f"{self.path}/{code}.csv")
            
            df_yq = pd.DataFrame(df_fs.loc[:,["연도","분기"]])
            
            df_fs.drop(columns=["연도","분기"],inplace=True)
            
            col = df_fs.columns
            
            impute = SoftImpute(verbose=False)
            
            df_impute = impute.fit_transform(df_fs)
            
            df_impute = pd.DataFrame(df_impute, columns=col).pct_change()
            
            df_concat = pd.concat([df_yq, df_impute],axis=1).dropna()
            
            df_concat.to_csv(f"{self.path}/preprocessed/{code}.csv",index=False, encoding='utf-8-sig')
        
        
if __name__ == "__main__":
    data = FinDataLoader("data")
    
    # data.load_price_data()
    data.labeling(30)
    
    # for code,_ in data.stock_list.items():
    #     data.data_processing(code)