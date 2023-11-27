from PyQt5 import QtCore, QtGui, QtWidgets
import main
from ui_functions import UIFunctions
from PyQt5.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect,
                          QSize, QTime, QUrl, Qt, QEvent)
from PyQt5.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence,
                         QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PyQt5.QtWidgets import *
from typing import List

from MplCanvas import MplCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


class MyQtApp(main.Ui_MainWindow, QtWidgets.QMainWindow):

    def __init__(self):
        super(MyQtApp, self).__init__()
        self.setupUi(self)
        # self.show() DRUGI SPOSÓB WYŚWIETLENIA APLIKACJI
        ## WYŁĄCZENIE TITLE BAR'A
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.pushButton_toggle_menu.clicked.connect(lambda: UIFunctions.toggle_menu(self, 150, True))
        self.pushButton_menu_1.setVisible(False)
        self.pushButton_menu_2.setVisible(False)
        self.pushButton_menu_homepage.setVisible(False)
        self.pushButton_menu_help.setVisible(False)
        self.label_creator.setVisible(False)
        self.pushButton_minimize.clicked.connect(lambda: ui.showMinimized())
        self.pushButton_maximize.clicked.connect(self.maximize_minimize)
        self.pushButton_exit.clicked.connect(lambda: sys.exit(0))  # Kiedyś ui.close()
        self.stackedWidget.setCurrentWidget(self.page_start)
        self.frame_oblicz.setVisible(False)
        self.frame_top_right.setVisible(False)

        # KOLOROWANIE CHECKBOXÓW
        # STRONA 1
        self.checkBox_page1_logarytmicscale.clicked.connect(lambda: self.checkbox_color(self.checkBox_page1_logarytmicscale))
        self.checkBox_page1_scatterplot.clicked.connect(lambda: self.checkbox_color(self.checkBox_page1_scatterplot))
        # STRONA 2
        self.checkBox_page2_logarytmicscale.clicked.connect(lambda: self.checkbox_color(self.checkBox_page2_logarytmicscale))
        self.checkBox_page2_scatterplot.clicked.connect(lambda: self.checkbox_color(self.checkBox_page2_scatterplot))
        self.checkBox_page2_clearplot.clicked.connect(lambda: self.checkbox_color_and_appear(self.checkBox_page2_clearplot))
        self.checkBox_page2_stopsteps.clicked.connect(lambda: self.checkbox_color_and_appear(self.checkBox_page2_stopsteps))
        self.checkBox_page2_stopvalue.clicked.connect(lambda: self.checkbox_color_and_appear(self.checkBox_page2_stopvalue))

        # JEDEN ZE SPOSOBÓW WALIDACJI LICZB
        # valid = QtGui.QIntValidator(1, 999)

        # WALIDACJA WPROWADZONYCH DANYCH POPRZEZ RegEx
        valid = QtGui.QRegularExpressionValidator(QtCore.QRegularExpression("[-]?[1-9]\\d{0,100}"))
        self.lineEdit_page1_lpoczatkowa.setValidator(valid)

        # PREDEFINIOWANE WARTOŚCI ROZMIARU LINEEDITÓW DLA KAŻDEGO STANU OKNA
        self.lineedit_size_menuon = {'clearplot': QSize(115, 20),
                                     'stop': QSize(162, 20)}

        self.lineedit_size_menuoff = {'clearplot': QSize(155, 20),
                                      'stop': QSize(162, 20)}

        self.lineedit_size_menuon_fs = {'clearplot': QSize(517, 20),
                                        'stop': QSize(306, 20)}

        self.lineedit_size_menuoff_fs = {'clearplot': QSize(543, 20),
                                         'stop': QSize(306, 20)}

        self.oldPos = self.pos()
        self.show()

    def checkbox_color_and_appear(self, object: QCheckBox):
        object_name = object.objectName().split('_')[-1]  # Zwraca ostatnią część nazwy lineedita
        if object.isChecked():
            object.setStyleSheet("color: rgb(0, 120, 0);")
            if object_name == 'clearplot':
                if self.checkBox_page2_clearplot.isChecked():
                    self.lineEdit_page2_clearplot.setMaximumSize(16777215, 20)
                else:
                    self.lineEdit_page2_clearplot.setMaximumSize(0, 20)
                if not self.checkBox_page2_stopsteps.isChecked():
                    self.lineEdit_page2_stopsteps.setMaximumSize(0, 20)
                else:
                    self.lineEdit_page2_stopsteps.setMaximumSize(16777215, 20)
                if not self.checkBox_page2_stopvalue.isChecked():
                    self.lineEdit_page2_stopvalue.setMaximumSize(0, 20)
                else:
                    self.lineEdit_page2_stopvalue.setMaximumSize(16777215, 20)
                print(UIFunctions.menu_flag)
                if UIFunctions.menu_flag:
                    if ui.isMaximized():
                        self.lineedit_smooth_show(self.lineEdit_page2_clearplot, QSize(self.lineedit_size_menuon_fs['clearplot']))
                    else:
                        self.lineedit_smooth_show(self.lineEdit_page2_clearplot, QSize(self.lineedit_size_menuon['clearplot']))
                else:
                    if ui.isMaximized():
                        self.lineedit_smooth_show(self.lineEdit_page2_clearplot, QSize(self.lineedit_size_menuoff_fs['clearplot']))
                    else:
                        self.lineedit_smooth_show(self.lineEdit_page2_clearplot, QSize(self.lineedit_size_menuoff['clearplot']))
                # self.lineEdit_page2_clearplot.setVisible(True)
            elif object_name == 'stopsteps':
                if not self.checkBox_page2_clearplot.isChecked():
                    self.lineEdit_page2_clearplot.setMaximumSize(0, 20)
                else:
                    self.lineEdit_page2_clearplot.setMaximumSize(16777215, 20)
                if self.checkBox_page2_stopsteps.isChecked():
                    self.lineEdit_page2_stopsteps.setMaximumSize(16777215, 20)
                else:
                    self.lineEdit_page2_stopsteps.setMaximumSize(0, 20)
                if not self.checkBox_page2_stopvalue.isChecked():
                    self.lineEdit_page2_stopvalue.setMaximumSize(0, 20)
                else:
                    self.lineEdit_page2_stopvalue.setMaximumSize(16777215, 20)
                if UIFunctions.menu_flag:
                    if ui.isMaximized():
                        self.lineedit_smooth_show(self.lineEdit_page2_stopsteps, QSize(self.lineedit_size_menuon_fs['stop']))
                    else:
                        self.lineedit_smooth_show(self.lineEdit_page2_stopsteps, QSize(self.lineedit_size_menuon['stop']))
                else:
                    if ui.isMaximized():
                        self.lineedit_smooth_show(self.lineEdit_page2_stopsteps, QSize(self.lineedit_size_menuoff_fs['stop']))
                    else:
                        self.lineedit_smooth_show(self.lineEdit_page2_stopsteps, QSize(self.lineedit_size_menuoff['stop']))
                # self.lineEdit_page2_stopsteps.setVisible(True)
            elif object_name == 'stopvalue':
                if not self.checkBox_page2_clearplot.isChecked():
                    self.lineEdit_page2_clearplot.setMaximumSize(0, 20)
                else:
                    self.lineEdit_page2_clearplot.setMaximumSize(16777215, 20)
                if not self.checkBox_page2_stopsteps.isChecked():
                    self.lineEdit_page2_stopsteps.setMaximumSize(0, 20)
                else:
                    self.lineEdit_page2_stopsteps.setMaximumSize(16777215, 20)
                if self.checkBox_page2_stopvalue.isChecked():
                    self.lineEdit_page2_stopvalue.setMaximumSize(16777215, 20)
                else:
                    self.lineEdit_page2_stopvalue.setMaximumSize(0, 20)
                if UIFunctions.menu_flag:
                    if ui.isMaximized():
                        self.lineedit_smooth_show(self.lineEdit_page2_stopvalue, QSize(self.lineedit_size_menuon_fs['stop']))
                    else:
                        self.lineedit_smooth_show(self.lineEdit_page2_stopvalue, QSize(self.lineedit_size_menuon['stop']))
                else:
                    if ui.isMaximized():
                        self.lineedit_smooth_show(self.lineEdit_page2_stopvalue, QSize(self.lineedit_size_menuoff_fs['stop']))
                    else:
                        self.lineedit_smooth_show(self.lineEdit_page2_stopvalue, QSize(self.lineedit_size_menuoff['stop']))
                # self.lineEdit_page2_stopvalue.setVisible(True)
        else:
            object.setStyleSheet("color: black;")
            if object_name == 'clearplot':
                if self.checkBox_page2_clearplot.isChecked():
                    self.lineEdit_page2_clearplot.setMaximumSize(16777215, 20)
                else:
                    self.lineEdit_page2_clearplot.setMaximumSize(0, 20)
                if not self.checkBox_page2_stopsteps.isChecked():
                    self.lineEdit_page2_stopsteps.setMaximumSize(0, 20)
                else:
                    self.lineEdit_page2_stopsteps.setMaximumSize(16777215, 20)
                if not self.checkBox_page2_stopvalue.isChecked():
                    self.lineEdit_page2_stopvalue.setMaximumSize(0, 20)
                else:
                    self.lineEdit_page2_stopvalue.setMaximumSize(16777215, 20)
                print(UIFunctions.menu_flag)
                # lineedit_size['clearplot'] = self.lineEdit_page2_clearplot.size()
                self.lineedit_smooth_show(self.lineEdit_page2_clearplot, QSize(0, self.lineedit_size_menuon['clearplot'].height()))

                # self.lineEdit_page2_clearplot.setVisible(False)
            elif object_name == 'stopsteps':
                if not self.checkBox_page2_clearplot.isChecked():
                    self.lineEdit_page2_clearplot.setMaximumSize(0, 20)
                else:
                    self.lineEdit_page2_clearplot.setMaximumSize(16777215, 20)
                if self.checkBox_page2_stopsteps.isChecked():
                    self.lineEdit_page2_stopsteps.setMaximumSize(16777215, 20)
                else:
                    self.lineEdit_page2_stopsteps.setMaximumSize(0, 20)
                if not self.checkBox_page2_stopvalue.isChecked():
                    self.lineEdit_page2_stopvalue.setMaximumSize(0, 20)
                else:
                    self.lineEdit_page2_stopvalue.setMaximumSize(16777215, 20)
                # lineedit_size['stopsteps'] = self.lineEdit_page2_stopsteps.size()
                self.lineedit_smooth_show(self.lineEdit_page2_stopsteps, QSize(0, self.lineedit_size_menuon['stop'].height()))
                # self.lineEdit_page2_stopsteps.setVisible(False)
            elif object_name == 'stopvalue':
                if not self.checkBox_page2_clearplot.isChecked():
                    self.lineEdit_page2_clearplot.setMaximumSize(0, 20)
                else:
                    self.lineEdit_page2_clearplot.setMaximumSize(16777215, 20)
                if not self.checkBox_page2_stopsteps.isChecked():
                    self.lineEdit_page2_stopsteps.setMaximumSize(0, 20)
                else:
                    self.lineEdit_page2_stopsteps.setMaximumSize(16777215, 20)
                if self.checkBox_page2_stopvalue.isChecked():
                    self.lineEdit_page2_stopvalue.setMaximumSize(16777215, 20)
                else:
                    self.lineEdit_page2_stopvalue.setMaximumSize(0, 20)
                # lineedit_size['stopvalue'] = self.lineEdit_page2_stopvalue.size()
                self.lineedit_smooth_show(self.lineEdit_page2_stopvalue, QSize(0, self.lineedit_size_menuon['stop'].height()))
                # self.lineEdit_page2_stopvalue.setVisible(False)

    def lineedit_smooth_show(self, object: QLineEdit, end_size: QSize):
        object.setMaximumSize(QSize(16777215, 16777215))
        self.animation1 = QPropertyAnimation(object, b"size")
        size = QSize(object.size())
        self.animation1.setStartValue(size)
        self.animation1.setEndValue(end_size)
        self.animation1.setDuration(200)
        self.animation1.start()


    def checkbox_color(self, object: QCheckBox):
        if object.isChecked():
            object.setStyleSheet("color: rgb(0, 120, 0);")
        else:
            object.setStyleSheet("color: black;")

    def lineedit_color(self, object: QLineEdit, label: QLabel):
        # Obsługa wszystkich danych wejściowych
        # print(self.lineedit_size)
        # print('LEFT = ', self.lineEdit_page2_time.size())
        # print('RIGHT = ', self.lineEdit_page2_stopvalue.size())
        # print('FRAME = ', self.groupBox_page2_settings_stop.size())
        if object.text() != '':
            try:
                int(object.text())
                label.setStyleSheet("color: rgb(0, 120, 0);")
                self.pushButton_oblicz.setEnabled(True)

            except ValueError:
                label.setStyleSheet("color: rgb(120, 0, 0);")
                self.pushButton_oblicz.setEnabled(False)
        else:
            label.setStyleSheet("color: black;")
            self.pushButton_oblicz.setEnabled(False)

    def page2_button_enable(self, object_lineedit_list: List[QLineEdit], object_label_list: List[QLabel]):
        button_flag_list = []
        for lineedit, label in zip(object_lineedit_list, object_label_list):
            if lineedit.text() != '':
                try:
                    float(lineedit.text())
                    label.setStyleSheet("color: rgb(0, 120, 0);")
                    button_flag_list.append(True)

                except ValueError:
                    label.setStyleSheet("color: rgb(120, 0, 0);")
                    button_flag_list.append(False)
            else:
                label.setStyleSheet("color: black;")
                button_flag_list.append(False)

        if all(button_flag_list):
            self.pushButton_oblicz.setEnabled(True)
        else:
            self.pushButton_oblicz.setEnabled(False)

    ## KOD ODPOWIEDZIALNY ZA PRZECIĄGANIE OKNA MYSZKĄ [MouseEvents]
    def mousePressEvent(self, event):
        if not ui.isMaximized():
            self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        if not ui.isMaximized():
            delta = QPoint(event.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()

    def maximize_minimize(self):
        if ui.isMaximized():
            ui.showNormal()
            self.groupBox_page2_settings_stop.setMinimumSize(400, 0)
        else:
            ui.showMaximized()
            self.groupBox_page2_settings_stop.setMinimumSize(544, 222)
        if self.checkBox_page2_clearplot.isChecked():
            self.lineEdit_page2_clearplot.setMaximumSize(QSize(16777215, 20))
        else:
            self.lineEdit_page2_clearplot.setMaximumSize(QSize(0, 20))
        if self.checkBox_page2_stopsteps.isChecked():
            self.lineEdit_page2_stopsteps.setMaximumSize(QSize(16777215, 20))
        else:
            self.lineEdit_page2_stopsteps.setMaximumSize(QSize(0, 20))
        if self.checkBox_page2_stopvalue.isChecked():
            self.lineEdit_page2_stopvalue.setMaximumSize(QSize(16777215, 20))
        else:
            self.lineEdit_page2_stopvalue.setMaximumSize(QSize(0, 20))

    def timer_button(self):
        # print('RIGHT = ', self.lineEdit_page2_stopvalue.size())
        if self.stackedWidget.currentWidget().objectName() == 'page':
            self.lineedit_color(self.lineEdit_page1_lpoczatkowa, self.label_page1_lpoczatkowa)
        elif self.stackedWidget.currentWidget().objectName() == 'page_2':
            self.page2_button_enable([self.lineEdit_page2_start, self.lineEdit_page2_end, self.lineEdit_page2_time],
                                     [self.label_page2_start, self.label_page2_end, self.label_page2_time])


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    # with open('style.css', 'r') as f:
    #     app.setStyleSheet(f.read())
    ui = MyQtApp()

    ## KOD ODPOWIADAJĄCY ZA ZMIANĘ KOLORU LABELI WPROWADZANYCH DANYCH
    timer = QtCore.QTimer()
    # timer.timeout.connect(lambda: ui.lineedit_color(ui.lineEdit_page1_lpoczatkowa, ui.label_page1_lpoczatkowa))
    # timer.timeout.connect(lambda: ui.page2_button_enable([ui.lineEdit_page2_start, ui.lineEdit_page2_end, ui.lineEdit_page2_time],
    #                                  [ui.label_page2_start, ui.label_page2_end, ui.label_page2_time]))
    timer.timeout.connect(lambda: ui.timer_button())
    timer.setInterval(100)
    timer.start()

    ui.show()
    sys.exit(app.exec_())

    ##DRUGI SPOSÓB WYŚWIETLENIA APLIKACJI##

    # window = MyQtApp()
    # sys.exit(app.exec_())

    #######################################
