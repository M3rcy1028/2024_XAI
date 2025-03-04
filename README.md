### Data Structure

    2024_XAI/
    │
    ├── data/
    ├── design/             # widget icons
    ├── stock_csv/          # actual OLHCV
    ├── model/              # trained model
    ├── XAI_GUI.ui          # main widget
    ├── lime_explanation.py	# generate lime chart
    ├── SHAP_explanation.py	# generate shap chart
    ├── stock_chart.py      # candle/predict chart
    └── README.md

### Major Libraries
```
pip install pyqt5
pip install lightweight-charts
pip install lime
pip install shap
```

### 프로젝트 설명
 기술적 지표와 재무제표를 기반으로 기업의 미래 수입률을 예측하고, 이를 설명가능한 인공지능(XAI) 기술을 통해 분석한다.
 
 
### 팀원 및 역할

| Name            | GitHub Username                          | Main Contribution Area(s)         |
|------------------|------------------------------------------|-----------------------------------|
| 김다솔       | [@dasolkim7](https://github.com/dasolkim7) | Explanation widget에 Feature 설명 생성  |
| 김민재       | [@CanelE452](https://github.com/CanelE452) | SHAP 설명 생성, Feature 조사 |
| 김태관       | [@KimTaegwan03](https://github.com/KimTaegwan03) | 기술적 지표 수집, 기술적 지표 및 재무제표 전처리, [모델 학습](https://github.com/KimTaegwan03/KW_VIP_Financial_Statements_Analysis.git) |
| 연선우         | [@Nagnero](https://github.com/Nagnero)       | Predict chart 생성 |
| 우나륜    | [@M3rcy1028](https://github.com/M3rcy1028) | PyQt GUI 기능 개발 및 다지안 총괄, Candle chart 생성 |
| 이정현    | [@LEEJH1029](https://github.com/LEEJH1029) | LIME 설명 생성, 재무제표 데이터 제공 |


Project of KW-VIP "그래프 머신러닝과 강화학습을 이용한 투자 알고리즘 개발"

Kwangwoon University 2024.
