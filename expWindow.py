from module import *
from lime_explanation import *

# import ui file
form_class3 = uic.loadUiType("./EXP_GUI.ui")[0]

class WindowClass3(QDockWidget, form_class3):
    def __init__(self, explanation_dict_lime=None, explanation_dict_shap=None):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Model Explanation")
        self.setWindowIcon(QIcon("./design/exp.png"))
        self.LIME_text.setReadOnly(True)
        self.SHAP_text.setReadOnly(True)
        self.explanation_dict_lime = explanation_dict_lime
        self.explanation_dict_shap = explanation_dict_shap
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
        # explanation_text가 존재한다면 해당 문자열로 설정
        if self.explanation_dict_lime is not None:
            lines = []
            for key, value in self.explanation_dict_lime.items():
                lines.append(f"&gt; <b>{key}</b><br>{value}")
            pretty_text = "<br><br>".join(lines)
            self.LIME_text.setText(pretty_text)

        else:
            self.LIME_text.setText("No explanation available")

        if self.explanation_dict_shap is not None:
            lines = []
            for key, value in self.explanation_dict_shap.items():
                lines.append(f"&gt; <b>{key}</b><br>{value}")
            pretty_text = "<br><br>".join(lines)
            self.SHAP_text.setText(pretty_text)

        else:
            self.SHAP_text.setText("No explanation available")
