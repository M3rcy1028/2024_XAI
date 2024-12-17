from module import *
from mainWindow import WindowClass

# PyQT 실행
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = WindowClass()   
    mainWindow.show()
    app.exec_()