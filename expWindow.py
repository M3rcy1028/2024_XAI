from module import *

# import ui file
form_class3 = uic.loadUiType("./EXP_GUI.ui")[0]

class WindowClass3(QDockWidget, form_class3):
    def __init__(self, explanation_dict=None):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Model Explanation")
        self.setWindowIcon(QIcon("./design/exp.png"))
        self.LIME_text.setReadOnly(True)
        self.SHAP_text.setReadOnly(True)
        self.explanation_dict = explanation_dict
        self.__main__()

    def initText(self):
        # explanation_text가 존재한다면 해당 문자열로 설정
        if self.explanation_dict is not None:
            lines = []
            for key, value in self.explanation_dict.items():
                lines.append(f"{key}: {value}")
            pretty_text = "\n".join(lines)
            self.LIME_text.setText(pretty_text)

        else:
            self.LIME_text.setText("No explanation available")
            self.SHAP_text.setText("No explanation available")

    def __main__(self):
        self.resetButton.clicked.connect(self.initText)