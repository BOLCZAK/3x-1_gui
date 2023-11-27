from PyQt5.QtCore import QPropertyAnimation, QPoint, QSize
from PyQt5.QtWidgets import QFrame
from matplotlib import pyplot as plt

from main import *
from compute_function import func
from MplCanvas import MplCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from time import perf_counter

## FUNKCJA ODPOWIADAJĄCA ZA UMOŻLIWIENIE KLIKNIĘCIA W "NIEKLIKALNY OBIEKT"


def clickable(widget):
    class Filter(QtCore.QObject):

        clicked = QtCore.pyqtSignal()

        def eventFilter(self, obj, event):

            if obj == widget:
                if event.type() == QtCore.QEvent.MouseButtonRelease:
                    if obj.rect().contains(event.pos()):
                        self.clicked.emit()
                        # The developer can opt for .emit(obj) to get the object within the slot.
                        return True

            return False

    filter = Filter(widget)
    widget.installEventFilter(filter)
    return filter.clicked


def reconnect(signal, newhandler=None, oldhandler=None):
    try:
        if oldhandler is not None:
            while True:
                signal.clicked.disconnect(oldhandler)
        else:
            signal.clicked.disconnect()
    except TypeError:
        pass
    if newhandler is not None:
        signal.clicked.connect(newhandler)


def delay(time_in_sec: float):
    die_time = QtCore.QTime = QtCore.QTime.currentTime().addMSecs(int(time_in_sec*1000))
    while QtCore.QTime.currentTime() < die_time:
        QtCore.QCoreApplication.processEvents(QtCore.QEventLoop.AllEvents, 100)


def normalize(arr, t_min, t_max):
    norm_arr = []
    diff = t_max - t_min
    diff_arr = max(arr) - min(arr)
    for i in arr:
        temp = (((i - min(arr))*diff)/diff_arr) + t_min
        norm_arr.append(int(temp))
    return norm_arr


class UIFunctions(Ui_MainWindow):

    # FLAGA KONTROLUJĄCA POJAWIANIE SIĘ TOOLBARA
    toolbar_flag_page1 = False
    toolbar_flag_page2 = False
    menu_flag = None

    def toggle_menu(self, max_width, enable):
        icon_colapse = QtGui.QIcon()
        if enable:
            width = self.frame_left_menu.width()
            default = 70

            if self.lineEdit_page2_clearplot.size().width() == 0:
                self.lineEdit_page2_clearplot.setMaximumSize(QSize(0, 20))
            if self.lineEdit_page2_stopsteps.size().width() == 0:
                self.lineEdit_page2_stopsteps.setMaximumSize(QSize(0, 20))
            if self.lineEdit_page2_stopvalue.size().width() == 0:
                self.lineEdit_page2_stopvalue.setMaximumSize(QSize(0, 20))

            if width == 70:
                UIFunctions.menu_flag = True
                width_extended = max_width
                visibility = True
                icon_colapse.addPixmap(QtGui.QPixmap("assets/icons/chevron-left.svg"), QtGui.QIcon.Normal,
                                       QtGui.QIcon.Off)

            else:
                UIFunctions.menu_flag = False
                width_extended = default
                visibility = False
                icon_colapse.addPixmap(QtGui.QPixmap("assets/icons/menu.svg"), QtGui.QIcon.Normal,
                                       QtGui.QIcon.Off)

            self.animation = QPropertyAnimation(self.frame_left_menu, b"minimumWidth")
            self.button_animation = QPropertyAnimation(self.frame_toggle, b"minimumWidth")

            # TOOLBAR DO WYKRESÓW
            if not UIFunctions.toolbar_flag_page1:
                self.sc = MplCanvas(self, width=5, height=4, dpi=100)
                self.toolbar = NavigationToolbar(self.sc, self.frame_page1_result_plot)
                self.layout = QtWidgets.QVBoxLayout()
                UIFunctions.toolbar_flag_page1 = True
            if not UIFunctions.toolbar_flag_page2:
                self.sc2 = MplCanvas(self, width=5, height=4, dpi=100)
                self.toolbar2 = NavigationToolbar(self.sc2, self.frame_page2_result_plot)
                self.layout2 = QtWidgets.QVBoxLayout()
                UIFunctions.toolbar_flag_page2 = True

            self.pushButton_menu_1.setVisible(visibility)
            self.pushButton_menu_2.setVisible(visibility)
            self.pushButton_menu_homepage.setVisible(visibility)
            self.pushButton_menu_help.setVisible(visibility)
            self.pushButton_menu_1.clicked.connect(lambda: UIFunctions.set_page1(self))
            self.pushButton_menu_2.clicked.connect(lambda: UIFunctions.set_page2(self))
            self.pushButton_menu_homepage.clicked.connect(lambda: UIFunctions.set_startup_page(self))
            self.pushButton_menu_help.clicked.connect(lambda: UIFunctions.set_help_page(self))
            self.label_creator.setVisible(visibility)
            clickable(self.label_creator).connect(lambda: UIFunctions.set_swamp(self))

            self.animation.setDuration(100)
            self.button_animation.setDuration(100)
            self.animation.setStartValue(width)
            self.button_animation.setStartValue(width)
            self.animation.setEndValue(width_extended)
            self.button_animation.setEndValue(width_extended)
            self.animation.start()
            self.button_animation.start()
            self.pushButton_toggle_menu.setIcon(icon_colapse)

    def set_startup_page(self):
        self.frame_oblicz.setVisible(False)
        self.frame_top_right.setVisible(False)
        self.stackedWidget.setCurrentWidget(self.page_start)

    def set_help_page(self):
        self.frame_oblicz.setVisible(False)
        self.frame_top_right.setVisible(False)
        self.stackedWidget.setCurrentWidget(self.page_help)

    def set_swamp(self):
        self.frame_oblicz.setVisible(False)
        self.frame_top_right.setVisible(False)
        self.stackedWidget.setCurrentWidget(self.page_mojebagno)

    def set_page1(self):
        self.frame_top_right.setVisible(False)
        self.stackedWidget.setCurrentWidget(self.page)
        reconnect(self.pushButton_oblicz, lambda: UIFunctions.plot_graph(self))
        # self.pushButton_oblicz.clicked.connect(lambda: UIFunctions.plot_graph(self))
        self.frame_oblicz.setVisible(True)
        self.frame_page1_settings.move(940, self.frame_page1_settings.y())
        self.frame_page1_result.move(940, self.frame_page1_result.y())
        UIFunctions.toggle_content(self, 200, 'page1')

    def set_page2(self):
        if not self.checkBox_page2_clearplot.isChecked():
            self.lineEdit_page2_clearplot.setMaximumSize(0, 20)
        self.checkBox_page2_clearplot.setStyleSheet("color: rgb(0, 120, 0);")
        self.lineEdit_page2_stopsteps.setMaximumSize(0, 20)
        self.lineEdit_page2_stopvalue.setMaximumSize(0, 20)

        self.stackedWidget.setCurrentWidget(self.page_2)
        self.frame_top_right.setVisible(True)
        reconnect(self.pushButton_oblicz, lambda: UIFunctions.plot_graph_page2(self))
        # self.pushButton_oblicz.clicked.connect(lambda: print('druga stroniczka'))
        self.frame_oblicz.setVisible(True)
        self.frame_page2_settings.move(940, self.frame_page2_settings.y())
        self.frame_page2_result.move(940, self.frame_page2_result.y())
        UIFunctions.toggle_content(self, 200, 'page2')

    def toggle_content(self, duration, frame_name: str):
        if frame_name == 'page1':
            self.animation1 = QPropertyAnimation(self.frame_page1_settings, b"pos")
            self.animation2 = QPropertyAnimation(self.frame_page1_result, b"pos")
        else:
            self.animation1 = QPropertyAnimation(self.frame_page2_settings, b"pos")
            self.animation2 = QPropertyAnimation(self.frame_page2_result, b"pos")
        self.animation1.setDuration(duration)
        self.animation2.setDuration(duration)
        if frame_name == 'page1':
            new_point = QPoint(1, self.frame_page1_settings.y())
            new_point2 = QPoint(1, self.frame_page1_result.y())
        else:
            new_point = QPoint(1, self.frame_page2_settings.y())
            new_point2 = QPoint(1, self.frame_page2_result.y())
        self.animation1.setEndValue(new_point)
        self.animation2.setEndValue(new_point2)
        # self.animation1.setStartValue(new_point)
        # self.frame_page1_settings.move(940, self.frame_page1_settings.y())
        self.animation1.start()
        self.animation2.start()

    def plot_graph(self):
        # ZBIERANIE WPROWADZONYCH PRZEZ UŻYTKOWNIKA DANYCH
        # toolbar_flag = False
        starting_value = int(self.lineEdit_page1_lpoczatkowa.text())
        print(starting_value)
        time_start = perf_counter()
        result, steps = func(starting_value)
        x_values = list(range(len(result)))

        # RYSOWANIE WYKRESU
        self.sc.axes.cla()  # CZYSZCZENIE WYKRESU
        if self.checkBox_page1_scatterplot.isChecked():
            self.sc.axes.scatter(x_values, result)
        else:
            self.sc.axes.plot(x_values, result)
        self.sc.axes.grid()
        self.sc.axes.set_facecolor('#2d2d2d')
        self.sc.fig.set_facecolor('#2d2d2d')
        self.sc.axes.set_xlabel('KROKI')
        self.sc.axes.set_ylabel('WARTOŚCI')
        self.sc.axes.set_title(f'3x+1 DLA L.P. = {starting_value}')
        if self.checkBox_page1_logarytmicscale.isChecked():
            self.sc.axes.set_yscale('log')
        self.sc.draw()
        # self.sc.show()
        # if not UIFunctions.toolbar_flag:
        #     UIFunctions.toolbar = NavigationToolbar(self.sc, self.frame_page1_result_plot)
        #     UIFunctions.toolbar_flag = True

        self.toolbar._nav_stack.clear()
        self.toolbar._update_view()

        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.sc)

        self.frame_page1_result_plot.setLayout(self.layout)
        time_end = perf_counter()
        self.lineEdit_page1_info_ymax.setText(str(max(result)))
        self.lineEdit_page1_info_stepmax.setText(str(steps-1))
        self.lineEdit_page1_info_time.setText(f'{time_end-time_start:.05f} [s]')

        print('Drukowanie na ekranie')

    def plot_graph_page2(self):
        # ZBIERANIE WPROWADZONYCH PRZEZ UŻYTKOWNIKA DANYCH
        # toolbar_flag = False
        start_value = int(self.lineEdit_page2_start.text())
        end_value = int(self.lineEdit_page2_end.text())
        time = float(self.lineEdit_page2_time.text())
        whole_time_start = perf_counter()
        attempts = [x for x in range(start_value, end_value, 1)]
        grid = False
        normalized_array = normalize(attempts, 0, 100)
        self.sc2.axes.set_facecolor('#2d2d2d')
        self.sc2.fig.set_facecolor('#2d2d2d')
        self.sc2.axes.cla()

        for i, attempt in enumerate(attempts, start=1):
            time = float(self.lineEdit_page2_time.text())
            iteration_time_start = perf_counter()
            y_values, steps = func(attempt)
            x_values = [x for x in range(len(y_values))]
            max_of_y_values = max(y_values)
            # plt.show()

            if self.checkBox_page2_scatterplot.isChecked():
                self.sc2.axes.scatter(x_values, y_values, s=8)
            else:
                self.sc2.axes.plot(x_values, y_values)
            if not grid:
                self.sc2.axes.grid()
                grid = True
            if self.checkBox_page2_stopsteps.isChecked():
                if steps > int(self.lineEdit_page2_stopsteps.text()):
                    self.sc2.axes.set_title(
                        f'3x+1 dla l.pocz. = {attempt} | KROKI = {steps - 1}\nMax Wartość = {max_of_y_values} | STOPPED steps exceeded {self.lineEdit_page2_stopsteps.text()}')
                    # input(f"Wartość przekroczyła {self.lineEdit_page2_stopsteps.text()} kroków -> Wciśnij dowolny klawisz...")
                    loop = QtCore.QEventLoop()
                    self.pushButton_page2_stepstop.clicked.connect(loop.exit)
                    self.lineEdit_page2_lastplot_ymax.setText(str(max_of_y_values))
                    self.lineEdit_page2_lastplot_stepmax.setText(str(steps - 1))
                    loop.exec()
                else:
                    self.sc2.axes.set_title(
                        f'3x+1 dla l.pocz. = {attempt} | KROKI = {steps - 1}\nMax Wartość = {max_of_y_values}')
            else:
                self.sc2.axes.set_title(f'3x+1 dla l.pocz. = {attempt} | KROKI = {steps - 1}\nMax Wartość = {max_of_y_values}', fontsize=8)
            if self.checkBox_page2_stopvalue.isChecked():
                if max_of_y_values > int(self.lineEdit_page2_stopvalue.text()):
                    self.sc2.axes.set_title(
                        f'3x+1 dla l.pocz. = {attempt} | KROKI = {steps - 1}\nMax Wartość = {max_of_y_values} | STOPPED value exceeded {self.lineEdit_page2_stopvalue.text()}')
                    # input(f"Wartość przekroczyła {self.lineEdit_page2_stopvalue.text()} -> Wciśnij dowolny klawisz...")
                    loop2 = QtCore.QEventLoop()
                    self.pushButton_page2_valuestop.clicked.connect(loop2.exit)
                    self.lineEdit_page2_lastplot_ymax.setText(str(max_of_y_values))
                    self.lineEdit_page2_lastplot_stepmax.setText(str(steps - 1))
                    loop2.exec()
                else:
                    self.sc2.axes.set_title(
                        f'3x+1 dla l.pocz. = {attempt} | KROKI = {steps - 1}\nMax Wartość = {max_of_y_values}')
            # else:
            #     self.sc2.axes.set_title(f'3x+1 dla l.pocz. = {attempt} | KROKI = {steps - 1}\nMax Wartość = {max_of_y_values}')
            self.sc2.axes.set_xlabel("KROKI")
            self.sc2.axes.set_ylabel("WARTOŚCI")
            if self.checkBox_page2_logarytmicscale.isChecked(): self.sc2.axes.set_yscale('log')
            self.sc2.draw()
            # plt.pause(time)
            # sleep(time)
            delay(time)
            # QtCore.QThread.msleep(int(time*1000))
            if self.checkBox_page2_clearplot.isChecked():
                if i % int(self.lineEdit_page2_clearplot.text()) == 0 and i + start_value != end_value:
                    self.sc2.axes.cla()
                    grid = False
                print(f"""
                            #####################
                            # i = {i + start_value} | b = {end_value} #
                            #####################""")
            if self.lineEdit_page2_time.text() == '':
                self.lineEdit_page2_time.setText('0.1')

            self.toolbar2._nav_stack.clear()
            self.toolbar2._update_view()

            self.layout2.addWidget(self.toolbar2)
            self.layout2.addWidget(self.sc2)

            self.frame_page2_result_plot.setLayout(self.layout2)

            self.progressBar.setValue(normalized_array[i-1])
            iteration_time_end = perf_counter()
            self.lineEdit_page2_lastplot_ymax.setText(str(max_of_y_values))
            self.lineEdit_page2_lastplot_stepmax.setText(str(steps-1))
            self.lineEdit_page2_lastplot_time.setText(f'{iteration_time_end-iteration_time_start:.05f} [s]')

        whole_time_end = perf_counter()
        self.lineEdit_page2_wholeiteration_time.setText(f'{whole_time_end-whole_time_start:.05f} [s]')

            # plt.close()
            # sleep(1)
