from module import *
from lime_explanation import *

# import ui file
form_class3 = uic.loadUiType("./EXP_GUI.ui")[0]

class WindowClass3(QDockWidget, form_class3):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Model Explanation")      # main widget title
        self.setWindowIcon(QIcon("./design/exp.png")) # main widget icon
        self.LIME_text.setReadOnly(True)                  # ReadOnly
        self.SHAP_text.setReadOnly(True)                  # ReadOnly
        self.initText()
        self.__main__()

    def initText(self):
        self.LIME_text.setText("Select stock")
        self.SHAP_text.setText("Select stock")

    def __main__(self):
        self.resetButton.clicked.connect(self.initText)
        self.pushButton.clicked.connect(self.createText)

    def createText(self):
        # lime 및 shap 설명 나오도록
        # 괄호 안에 설명 추가 
        self.LIME_text.setText("설명 추가")
        self.SHAP_text.setText("설명 추가")
