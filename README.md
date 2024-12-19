### Data Structure

    2024_XAI/
    │
    ├── design/            # widget icons 
    ├── result/            # displayed images
    ├── stock_csv/         # 
    ├── stock_logo/
    ├── XAI_GUI.ui
	├── module.py
    ├── main.py
	├── mainWindow.py
    ├── stock_chart.py
    └── README.md

### Major Libraries
```
pip install pyqt5
pip install lightweight-charts
pip install lime
pip install shap
```

### 과제 설명
 본 과제는 인터넷 중고장터 웹 애플리케이션을 개발하는 것이다. 따라서 <그린마켓>이라는 이름의 
중고 장터 웹 애플리케이션을 node.js와 mysql을 사용하여 이를 구현하였다. 
그린마켓은 사용자 기능과 관리자 기능으로 나뉜다. 사용자는 물건을 판매하기 위해 게시글을 작성
하거나 다른 사용자의 게시글을 조회하고, 문의하여 웹 애플리케이션 내 화폐로 구매할 수 있다. 또
한, 마이페이지에서 자신이 게시한 게시물, 조회한 게시물, 구매한 상품의 게시물을 확인할 수 있다. 
관리자는 공지를 작성하고 유저의 문의를 확인할 수 있다. 또한, 유저의 정보, 게시판 정보 등을 
수정하는 등 웹 애플리케이션을 전반적으로 관리할 수 있다.

### 설명 및 시연 영상
https://youtu.be/RSHVBHfslwM

### 팀원 및 역할

| Name            | GitHub Username                          | Main Contribution Area(s)         |
|------------------|------------------------------------------|-----------------------------------|
| 김다솔       | [@dasolkim7](https://github.com/dasolkim7) | Explanation widget에 Feature 설명 생성, 최종영상촬영  |
| 김민재       | [@CanelE452](https://github.com/CanelE452) | SHAP 설명 생성, Feature 조사 |
| 김태관       | [@KimTaegwan03](https://github.com/KimTaegwan03) | 기술적 지표 수집, 기술적 지표 및 재무제표 전처리, 모델 학습 |
| 연선우         | [@Nagnero](https://github.com/Nagnero)       | Predict chart 생성 |
| 우나륜    | [@M3rcy1028](https://github.com/M3rcy1028) | PyQt GUI 기능 개발 및 다지안 총괄, Candle chart 생성 |
| 이정현    | [@LEEJH1029](https://github.com/LEEJH1029) | LIME 설명 생성, 재무제표 데이터 제공 |


Project of KW-VIP "그래프 머신러닝과 강화학습을 이용한 투자 알고리즘 개발"

Kwangwoon University 2024.
