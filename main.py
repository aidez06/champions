import requests
from PyQt5 import QtCore, QtGui, QtWidgets
import gspread
from oauth2client.service_account import ServiceAccountCredentials


class Ui_MainWindow(object):
    result_data  = []
    set = {}


    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(633, 449)
        MainWindow.setAutoFillBackground(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(60, 60, 61, 16))
        self.label.setObjectName("label")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(140, 60, 72, 20))
        self.comboBox.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContents)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(150, 350, 131, 31))
        self.pushButton_2.setObjectName("pushButton_2")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(250, 20, 131, 31))
        font = QtGui.QFont()
        font.setFamily("MS Gothic")
        font.setPointSize(20)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(20, 100, 601, 231))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, item)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 633, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Extact Data Champions"))
        self.label.setText(_translate("MainWindow", "Select Role:"))
        self.comboBox.setItemText(0, _translate("MainWindow", "MID"))
        self.comboBox.setItemText(1, _translate("MainWindow", "TOP"))
        self.comboBox.setItemText(2, _translate("MainWindow", "JUNGLE"))
        self.comboBox.setItemText(3, _translate("MainWindow", "ADC"))
        self.comboBox.setItemText(4, _translate("MainWindow", "SUPPORT"))

        self.pushButton_2.setText(_translate("MainWindow", "Refresh"))
        self.pushButton_2.clicked.connect(self.extract_data)

        self.label_2.setText(_translate("MainWindow", "CHAMPIONS"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Rank"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Champion Name"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Champion Image"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Tier"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Win Rate"))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "Pick Rate"))
        item = self.tableWidget.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "Ban Rate"))

    def extract_data(self):


        hero_images = []
        heroes_name = []
        ranking_heroes = []
        tier = []
        win_rate = []
        pick_rate = []
        ban_rate = []
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        url = 'https://www.op.gg/_next/data/gisCgnxLkzFo3nRgsahoX/champions.json?region=kr&tier=platinum_plus&position=jungle'
        r = requests.get(url, headers=headers).json()
        for i in r['pageProps']['championMetaList']:
            for x in i['positions']:
                if x['name'] == self.comboBox.currentText():
                    hero_images.append(i['image_url'])
                    ranking_heroes.append(int(x['stats']['tier_data']['rank']))
                    tier.append(int(x['stats']['tier_data']['tier']))
                    win_rate.append('{:,.2%}'.format(x['stats']['win_rate']))
                    pick_rate.append('{:,.2%}'.format(x['stats']['pick_rate']))
                    ban_rate.append('{:,.2%}'.format(x['stats']['ban_rate']))
                    heroes_name.append(i['name'])
            combine = [[ rk,hn,hi,t,wr,pr,br] for rk,hn,hi,t,wr,pr,br in zip(ranking_heroes, heroes_name, hero_images, tier, win_rate, pick_rate, ban_rate)]
            combine_rankings = list(combine)
            sort_of_ranks = sorted(combine_rankings, key=lambda tup: (tup[0]))
            row = 0
            self.tableWidget.setRowCount(len(sort_of_ranks))
            for sort_of_rank in sort_of_ranks:
                self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(str(sort_of_rank[0])))
                self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(sort_of_rank[1]))
                self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(sort_of_rank[2]))
                self.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(str(sort_of_rank[3])))
                self.tableWidget.setItem(row, 4, QtWidgets.QTableWidgetItem(sort_of_rank[4]))
                self.tableWidget.setItem(row, 5, QtWidgets.QTableWidgetItem(sort_of_rank[5]))
                self.tableWidget.setItem(row, 6, QtWidgets.QTableWidgetItem(sort_of_rank[6]))

                row += 1



        self.scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
                 "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
        self.creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', self.scope)
        self.client = gspread.authorize(self.creds)
        try:
            if self.comboBox.currentText() == 'MID':
                self.worksheet = self.client.open('Champions_Data').sheet1
                self.worksheet.update(f'A1:H{len(sort_of_ranks)}',sort_of_ranks, value_input_option='USER_ENTERED')
            elif self.comboBox.currentText() == 'TOP':
                self.worksheet = self.client.open('Champions_Data').worksheet('TOP')
                self.worksheet.update(f'A1:H{len(sort_of_ranks)}',sort_of_ranks, value_input_option='USER_ENTERED')
            elif self.comboBox.currentText() == 'JUNGLE':
                self.worksheet = self.client.open('Champions_Data').worksheet('JUNGLE')
                self.worksheet.update(f'A1:H{len(sort_of_ranks)}',sort_of_ranks, value_input_option='USER_ENTERED')
            elif self.comboBox.currentText() == 'ADC':
                self.worksheet = self.client.open('Champions_Data').worksheet('ADC')
                self.worksheet.update(f'A1:H{len(sort_of_ranks)}',sort_of_ranks, value_input_option='USER_ENTERED')
            elif self.comboBox.currentText() == 'SUPPORT':
                self.worksheet = self.client.open('Champions_Data').worksheet('SUPPORT')
                self.worksheet.update(f'A1:H{len(sort_of_ranks)}',sort_of_ranks, value_input_option='USER_ENTERED')


        except Exception as e:
                pass












if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
