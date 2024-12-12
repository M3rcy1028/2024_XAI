from module import *
from stock_chart import StockChart
from infoWindow import WindowClass2
from expWindow import WindowClass3
from lime_explanation import run_lime_analysis

# import ui file
form_class = uic.loadUiType("./XAI_GUI.ui")[0]


class WindowClass(QMainWindow, form_class):
    def __init__(self):
        #### Main Widget Design
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("KW-VIP XAI")  # main widget title
        self.setWindowIcon(QIcon("./design/kwlogo.png"))  # main widget icon
        # self.LLM_text.setReadOnly(True)                  # ReadOnly
        self.SetComboBox()  # set selections
        self.statusBar = self.statusBar()  # access status bar
        #### set/get main widget position
        self.move(400, 200)
        MainWindowSize = self.geometry()
        self.main_x = MainWindowSize.x()
        self.main_y = MainWindowSize.y()
        self.main_width = MainWindowSize.width()
        self.main_height = MainWindowSize.height()
        #### input variables
        self.chart = None
        self.msglog = ""
        self.StockName = "None"
        self.StockPeriod = "None"
        #### default variables
        self.calendarButton.setIcon(QIcon("./design/calendar.png"))
        self.infoButton.setIcon(QIcon("./design/info.png"))
        self.logButton.setIcon(QIcon("./design/log.png"))
        self.Widget1_image = "./result/StockChart.png"
        self.Widget2_image = "./result/lime_explanation.png"
        self.Widget3_image = "./result/LIME_result.png"
        self.force = 0
        #### time
        self.timer = QTimer()
        self.timer.timeout.connect(self.ShowTime)
        self.timer.start(1000)
        self.ShowTime()
        #### default widget
        self.CalendarWidget()
        self.LogWidget()
        self.__initGUI__()
        self.__main__()

    #### connect to external widget ####
    def ShowInfoWidget(self):
        self.infoWidget = WindowClass2()
        self.infoWidget.move(self.main_x - 300, self.main_y + 330)
        self.infoWidget.show()

    def ShowExpWidget(self):
        self.expWidget = WindowClass3()
        self.expWidget.move(self.main_x + self.main_width, self.main_y)
        self.expWidget.show()

    def closeEvent(self, event):  # close external windows
        if hasattr(self, 'infoWidget'):
            self.infoWidget.close()
        if hasattr(self, "expWidget"):
            self.expWidget.close()
        event.accept()

    #### End of connect to external widget ####

    def printLog(self, record="", msgreset=0):  # message logs
        timestamp = time.strftime("[%Y-%m-%d %H:%M:%S] ", time.localtime())
        if msgreset:
            self.msglog = str(timestamp) + "GUI reset"
        else:
            self.msglog = self.msglog + "\n" + str(timestamp) + record
        self.logtext.setText(self.msglog)

    def __initGUI__(self):  # [Reset]
        self.printLog(msgreset=1)
        self.progressBar.setValue(0)  # progressBar initial value
        self.progressBar_label.setText("Ready")
        # self.SetLLM()
        self.SetLabel()
        self.Q0_radioButton.setChecked(True)
        self.SetDateEdit()
        self.StockComboBox.setCurrentIndex(0)
        # widget settings
        self.InitWidet()

    def __exit__(self):  # [Exit]
        self.CloseWidget()
        self.CalendarWidget.close()
        self.LogWidget.close()
        self.close()

    def __main__(self):
        # pushButton
        self.ConfirmButton.clicked.connect(self.InputButton)
        self.ResetButton.clicked.connect(self.__initGUI__)
        self.ExitButton.clicked.connect(self.__exit__)
        self.ShowButton.clicked.connect(self.OutputButton)
        self.CloseButton.clicked.connect(self.CloseWidget)
        self.calendarButton.clicked.connect(self.CalendarWidget_exec)
        self.infoButton.clicked.connect(self.ShowInfoWidget)
        self.logButton.clicked.connect(self.LogWidget_exec)
        self.expButton.clicked.connect(self.ShowExpWidget)
        # checkBox
        self.SelectAll_checkBox.stateChanged.connect(self.SelectCheckBox)
        self.Candle_checkBox.stateChanged.connect(self.DeselectCheckBox)
        self.Chart_checkBox.stateChanged.connect(self.DeselectCheckBox)
        self.LIME_checkBox.stateChanged.connect(self.DeselectCheckBox)
        self.SHAP_checkBox.stateChanged.connect(self.DeselectCheckBox)
        # radioButton
        self.Q0_radioButton.clicked.connect(self.SetDateEdit)
        self.Q1_radioButton.clicked.connect(self.SetDateEdit)
        self.Q2_radioButton.clicked.connect(self.SetDateEdit)
        self.Q3_radioButton.clicked.connect(self.SetDateEdit)
        self.Q4_radioButton.clicked.connect(self.SetDateEdit)

    def SetLabel(self, stock="None", period="None"):  # Set Stock info label
        self.Stockname_label.setText(stock)
        self.Period_label.setText(period)

    # def SetLLM(self, content='데이터를 선택해주세요.'): # print LLM or Error msg
    #     self.LLM_text.setText("\n" + content)

    def SetComboBox(self):  # insert stocks into comboBox
        self.StockComboBox.addItem("삼성전자 (KRX:005930)")
        self.StockComboBox.addItem("엔씨소프트 (KRX:036570)")
        self.StockComboBox.addItem("KB금융 (KRX:105560)")

    def SetDateEdit(self):
        '''
            Initialize Start/End Date based on 
            User Defined Date/Q1/Q2/Q3/Q4
        '''
        CurrentDate = datetime.now()
        year = CurrentDate.year
        d1 = QDate(year - 2, CurrentDate.month, CurrentDate.day)
        d2 = QDate(year, CurrentDate.month, CurrentDate.day)
        if self.Q1_radioButton.isChecked():
            d1 = QDate(year, 1, 1)
            d2 = QDate(year, 3, 31)
        elif self.Q2_radioButton.isChecked():
            d1 = QDate(year, 4, 1)
            d2 = QDate(year, 6, 30)
        elif self.Q3_radioButton.isChecked():
            d1 = QDate(year, 7, 1)
            d2 = QDate(year, 9, 30)
        elif self.Q4_radioButton.isChecked():
            d1 = QDate(year, 10, 1)
            d2 = QDate(year, 12, 31)
        self.StartDate.setDate(d1)
        self.EndDate.setDate(d2)

    def SelectCheckBox(self, state):
        '''
            if [Select All] is True, the others become True.
            (Vice versa)
        '''
        if state == 2:
            self.Candle_checkBox.setChecked(True)
            self.Chart_checkBox.setChecked(True)
            self.LIME_checkBox.setChecked(True)
            self.SHAP_checkBox.setChecked(True)
            self.force = 1
        elif self.force:
            self.Candle_checkBox.setChecked(False)
            self.Chart_checkBox.setChecked(False)
            self.LIME_checkBox.setChecked(False)
            self.SHAP_checkBox.setChecked(False)

    def DeselectCheckBox(self, state):
        '''
            CASE 1) If [Select All] is True and one of the others is False,
            [Select All] becomes false.
            CASE 2) If [Select All] is False and the others are True,
            [Select All] becomes True.
        '''
        if state == 2 and (self.Candle_checkBox.isChecked() and
                           self.Chart_checkBox.isChecked() and
                           self.LIME_checkBox.isChecked() and
                           self.SHAP_checkBox.isChecked()):
            self.SelectAll_checkBox.setChecked(True)
        else:
            self.force = 0
            self.SelectAll_checkBox.setChecked(False)

    def ShowTime(self):  # Display current time in the status bar
        current_date = QDate.currentDate()
        current_time = QTime.currentTime()
        formatted_time = datetime.now().strftime("%A, %B %d, %Y, %I:%M:%S %p")
        self.statusBar.showMessage(formatted_time)

        #### Define Button Function ####

    def InputButton(self):  # [Confirm]
        # self.SetLLM()
        self.CloseWidget()
        self.DataProcessing()
        self.GenerateResult()
        self.ProgressLoading()
        self.printLog(record="Data submitted")

    def DataProcessing(self):  # Process input data
        # get stock name without stock code
        sname = self.StockComboBox.currentText()
        sname = sname.split(' ')
        self.StockName = str(sname[0])
        # get period
        self.sdate = self.StartDate.date()
        self.edate = self.EndDate.date()
        sdate_str = str(self.sdate.day()) + "/" + str(self.sdate.month()) + "/" + str(self.sdate.year())
        edate_str = str(self.edate.day()) + "/" + str(self.edate.month()) + "/" + str(self.edate.year())
        self.StockPeriod = sdate_str + " - " + edate_str
        self.SetLabel(self.StockComboBox.currentText(), self.StockPeriod)

    def GenerateResult(self):  # gernerate results using other files
        try:
            StockChart(stockname=self.StockName, startdate=self.sdate.toPyDate(), enddate=self.edate.toPyDate())
        except Exception as e:
            self.printLog(record=str(e))
            # self.SetLLM(str(e))

    def ProgressLoading(self):  # design Loading bar
        self.progressBar_label.setText("Loading...")
        for i in range(20):
            self.progressBar.setValue(i)
            sleep(0.05)
        for i in range(20, 50):
            self.progressBar.setValue(i)
            sleep(0.01)
        for i in range(50, 101):
            self.progressBar.setValue(i)
            sleep(0.001)
        sleep(0.5)
        self.progressBar_label.setText("Completed")

    def OutputButton(self):  # [Show]
        self.CloseWidget()  # close old result widgets
        try:  # create lightweight chart
            self.chart = StockChart(method='lightweight', stockname=self.StockName, startdate=self.sdate.toPyDate(),
                                    enddate=self.edate.toPyDate())
        except Exception as e:
            self.printLog(record=str(e))
        self.InitWidet()  # update widgets
        self.OpenWidget()  # open new result widgets
        # self.SetLLM(self.StockName)

    #### End of Button Function ####

    def InitWidet(self):
        self.Widget1_init()
        self.Widget2_init()
        self.Widget3_init()

    def OpenWidget(self):  # open selected widgets
        if self.Chart_checkBox.isChecked():
            self.Widget1_exec()
            self.printLog(record="prediction chart selected")
        if self.Candle_checkBox.isChecked() and self.chart:
            self.chart.show(block=False)
            self.printLog(record="candle chart selected")
        if self.LIME_checkBox.isChecked() and self.SHAP_checkBox.isChecked():
            start_date = self.StartDate.date().toString("yyyy-MM-dd")
            end_date = self.EndDate.date().toString("yyyy-MM-dd")

            stock_name = self.StockComboBox.currentText()
            code = re.search(r':(\d+)', stock_name).group(1)

            output_file = "./result/lime_explanation.png"
            try:
                result_image = run_lime_analysis(code, start_date, end_date, output_file=output_file)
                self.Widget2_image = result_image  # 결과 이미지 업데이트
            except Exception as e:
                self.printLog(record=f"LIME 실행 오류: {e}")
                return
            self.Widget2_exec()
            self.Widget3_exec()
            self.printLog(record="LIME/SHAP selected")
        elif self.LIME_checkBox.isChecked() == False and self.SHAP_checkBox.isChecked():
            self.Widget2_exec("SHAP", "./design/shap.png")
            self.printLog(record="SHAP selected")
        elif self.LIME_checkBox.isChecked() and self.SHAP_checkBox.isChecked() == False:
            start_date = self.StartDate.date().toString("yyyy-MM-dd")
            end_date = self.EndDate.date().toString("yyyy-MM-dd")

            stock_name = self.StockComboBox.currentText()
            code = re.search(r':(\d+)', stock_name).group(1)

            output_file = "./result/lime_explanation.png"
            try:
                result_image = run_lime_analysis(code, start_date, end_date, output_file=output_file)
                self.Widget2_image = result_image  # 결과 이미지 업데이트
            except Exception as e:
                self.printLog(record=f"LIME 실행 오류: {e}")
                return
            self.Widget2_exec()
            self.printLog(record="LIME selected")

    def CloseWidget(self):  # close all the opend widgets w/o main
        self.printLog(record="Result widgets are closed")
        self.Widget1.close()
        self.Widget2.close()
        self.Widget3.close()
        '''
            Close lightweight chart
            If a user wants to update or re-display this chart,
            he/she must push [Close] button.
        '''
        if self.chart:
            self.chart.exit()

    #### Define Widgets #####
    def Widget1_init(self):
        self.Widget1 = QWidget()
        self.Widget1.resize(700, 430)
        # Right side of main
        self.Widget1.move(self.main_x + self.main_width, self.main_y)
        self.Widget1.setMinimumSize(100, 100)
        Stocklayout = QVBoxLayout()
        self.Widget1.setLayout(Stocklayout)
        # add image
        Stockpixmap = QPixmap(self.Widget1_image)
        Stocklabel = QLabel()
        Stocklabel.setPixmap(Stockpixmap)
        Stocklabel.setScaledContents(True)
        Stocklayout.addWidget(Stocklabel)  # add new layout
        '''
        image = QPixmap()
        image.load(self.StockLinepath)
        image = image.scaled(710, 300)
        self.StockChartImage.setPixmap(image)
        '''

    def Widget1_exec(self, title="Stock Chart", icon="./design/stockchart.png"):
        self.Widget1.setWindowTitle(title)
        self.Widget1.setWindowIcon(QIcon(icon))
        self.Widget1.show()

    def Widget2_init(self):
        self.Widget2 = QWidget()
        self.Widget2.resize(400, 300)
        self.Widget2.setMinimumSize(100, 100)
        # below main
        self.Widget2.move(self.main_x, self.main_y + self.main_height + 30)
        Widget2layout = QVBoxLayout()
        self.Widget2.setLayout(Widget2layout)
        # add image
        wd2pixmap = QPixmap(self.Widget2_image)
        wd2label = QLabel()
        wd2label.setPixmap(wd2pixmap)
        wd2label.setScaledContents(True)
        Widget2layout.addWidget(wd2label)  # add new layout

    def Widget2_exec(self, title="LIME", icon="./design/lime.png"):
        self.Widget2_image = "./result/lime_explanation.png"

        if hasattr(self, "Widget2") and self.Widget2.isVisible():
            self.Widget2.close()

        self.Widget2 = QWidget()
        self.Widget2.resize(800, 600)
        self.Widget2.setMinimumSize(100, 100)

        lime_pixmap = QPixmap(self.Widget2_image)
        lime_label = QLabel()
        lime_label.setPixmap(lime_pixmap)
        lime_label.setScaledContents(True)

        Widget2layout = QVBoxLayout()
        Widget2layout.addWidget(lime_label)
        self.Widget2.setLayout(Widget2layout)

        self.Widget2.setWindowTitle(title)
        self.Widget2.setWindowIcon(QIcon(icon))
        self.Widget2.show()

    def Widget3_init(self):
        # get position of widget2
        wd2_geometry = self.Widget2.geometry()
        wd2_x = wd2_geometry.x()
        wd2_y = wd2_geometry.y()
        wd2_height = wd2_geometry.height()
        self.Widget3 = QWidget()
        self.Widget3.resize(400, 300)
        self.Widget3.setMinimumSize(100, 100)
        # right side of widget2
        self.Widget3.move(wd2_x + 400, wd2_y)
        Widget3layout = QVBoxLayout()
        self.Widget3.setLayout(Widget3layout)
        # add image
        wd3pixmap = QPixmap(self.Widget3_image)
        wd3label = QLabel()
        wd3label.setPixmap(wd3pixmap)
        wd3label.setScaledContents(True)
        Widget3layout.addWidget(wd3label)  # add new layout

    def Widget3_exec(self, title="SHAP", icon="./design/shap.png"):
        self.Widget3.setWindowTitle(title)
        self.Widget3.setWindowIcon(QIcon(icon))
        self.Widget3.show()

    def CalendarWidget(self):
        self.CalendarWidget = QWidget()
        self.CalendarWidget.resize(300, 300)
        self.CalendarWidget.setMinimumSize(200, 200)
        # left side of main
        self.CalendarWidget.move(self.main_x - 300, self.main_y)
        CalendarLayout = QVBoxLayout()
        self.CalendarWidget.setLayout(CalendarLayout)
        # add calendar widget
        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)
        # set language : en
        QLocale.setDefault(QLocale(QLocale.English))
        self.calendar.setLocale(QLocale(QLocale.English))
        ##
        CalendarLayout.addWidget(self.calendar)  # add layout
        self.CalendarWidget.setWindowTitle("Calendar")
        self.CalendarWidget.setWindowIcon(QIcon("./design/calendar.png"))
        # self.CalendarWidget.show()

    def CalendarWidget_exec(self):
        self.CalendarWidget.show()

    def LogWidget(self):
        self.LogWidget = QWidget()
        self.LogWidget.resize(self.main_width, 100)
        self.LogWidget.setMinimumSize(100, 100)
        # above main 
        self.LogWidget.move(self.main_x, self.main_y - 130)
        LogLayout = QVBoxLayout()
        self.LogWidget.setLayout(LogLayout)
        # add text browser
        self.logtext = QTextEdit()
        self.logtext.setReadOnly(True)
        LogLayout.addWidget(self.logtext)  # add layout
        self.LogWidget.setWindowTitle("Log")
        self.LogWidget.setWindowIcon(QIcon("./design/log.png"))

    def LogWidget_exec(self):
        self.LogWidget.show()
    #### End of Widgets #####
