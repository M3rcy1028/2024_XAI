from module import *

# import ui file
form_class2 = uic.loadUiType("./INFO_GUI.ui")[0]

class WindowClass2(QDockWidget, form_class2):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Information")                # main widget title
        self.setWindowIcon(QIcon("./design/info.png")) # main widget icon