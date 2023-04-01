import os
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import uic
from pdr import PDR
from matplotlib.backends.backend_qt5agg import FigureCanvas as FigureCanvas
from matplotlib.figure import Figure

########################################
def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


form = resource_path("form.ui")
form_class = uic.loadUiType(form)[0]
########################################

# form_class = uic.loadUiType("form.ui")[0]


class MainWidget(QWidget, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btn_cal.clicked.connect(self.btn_cal_clicked)
        self.pdr = PDR()

        icon = resource_path("icon.ico")
        self.setWindowIcon(QIcon(icon))
        logo = resource_path("logo.gif")
        self.lbl_logo.setPixmap(QPixmap(logo))

        self.radio_2.clicked.connect(self.radio_clicked)
        self.radio_3.clicked.connect(self.radio_clicked)

        self.canvas = FigureCanvas(Figure(figsize=(555, 555)))
        self.formLayout.addWidget(self.canvas)
        ax = self.canvas.figure.subplots()
        ax.set_title("87T Operation Area")

    def radio_clicked(self):
        if self.radio_2.isChecked():
            self.edit_v_3.setValue(0)
            self.edit_v_3.setEnabled(False)
            self.edit_ct_ratio_3.setValue(0)
            self.edit_ct_ratio_3.setEnabled(False)
            self.edit_factor_3.setValue(0)
            self.edit_factor_3.setEnabled(False)
            self.edit_i_3_r.setValue(0)
            self.edit_i_3_r.setEnabled(False)
            self.edit_i_3_s.setValue(0)
            self.edit_i_3_s.setEnabled(False)
            self.edit_i_3_t.setValue(0)
            self.edit_i_3_t.setEnabled(False)
        elif self.radio_3.isChecked():
            self.edit_v_3.setValue(600)
            self.edit_v_3.setEnabled(True)
            self.edit_ct_ratio_3.setValue(5000)
            self.edit_ct_ratio_3.setEnabled(True)
            self.edit_factor_3.setValue(0)
            self.edit_factor_3.setEnabled(True)
            self.edit_i_3_r.setValue(0)
            self.edit_i_3_r.setEnabled(True)
            self.edit_i_3_s.setValue(0)
            self.edit_i_3_s.setEnabled(True)
            self.edit_i_3_t.setValue(0)
            self.edit_i_3_t.setEnabled(True)

    def btn_cal_clicked(self):
        # PDR 리셋
        self.pdr.reset_pdr()

        # UI로부터 세팅값 받아오기 & PDR 세팅값 설정
        settings = self.get_settings()
        self.pdr.set_pdr(**settings)

        # factor1~3 계산하기
        self.pdr.cal_factors()
        self.edit_factor_1.setValue(self.pdr.factor_1)
        self.edit_factor_2.setValue(self.pdr.factor_2)
        self.edit_factor_3.setValue(self.pdr.factor_3)

        # Id, Ir 계산하기
        self.pdr.cal_i_d_and_i_r()
        self.edit_i_d.setValue(self.pdr.i_d)
        self.edit_i_r.setValue(self.pdr.i_r)

        # 동작여부, 동작요소 계산하기
        pickup_result = self.pdr.cal_pickup()
        self.edit_result_1.setText(pickup_result[0])
        self.edit_result_2.setText(pickup_result[1])

        # 그래프 그리기
        settings = self.pdr.get_pdr()
        self.draw_graph(settings)

    def get_settings(self):
        if self.radio_2.isChecked():
            winding = 2
        elif self.radio_3.isChecked():
            winding = 3
        v_1 = int(self.edit_v_1.text())
        v_2 = int(self.edit_v_2.text())
        v_3 = int(self.edit_v_3.text())
        ct_ratio_1 = int(self.edit_ct_ratio_1.text())
        ct_ratio_2 = int(self.edit_ct_ratio_2.text())
        ct_ratio_3 = int(self.edit_ct_ratio_3.text())
        i_n = int(self.edit_i_n.text())
        i_low = float(self.edit_i_low.text())
        slope_1 = float(int(self.edit_slope_1.text()) / 100)
        slope_2 = float(int(self.edit_slope_2.text()) / 100)
        knee_point = float(self.edit_knee_point.text())
        i_high = float(self.edit_i_high.text())
        i_1 = float(self.edit_i_1_r.text())
        i_2 = float(self.edit_i_2_r.text())
        i_3 = float(self.edit_i_3_r.text())

        return {
            "winding": winding,
            "v_1": v_1,
            "v_2": v_2,
            "v_3": v_3,
            "ct_ratio_1": ct_ratio_1,
            "ct_ratio_2": ct_ratio_2,
            "ct_ratio_3": ct_ratio_3,
            "i_n": i_n,
            "i_low": i_low,
            "slope_1": slope_1,
            "slope_2": slope_2,
            "knee_point": knee_point,
            "i_high": i_high,
            "i_1": i_1,
            "i_2": i_2,
            "i_3": i_3,
        }

    def draw_graph(self, settings):
        self.canvas.figure.clf()
        ax = self.canvas.figure.subplots()
        point1 = (0, settings["i_low"])
        point2 = settings["cross_1"]
        point3 = settings["cross_2"]
        point4 = settings["cross_3"]
        x = [point1[0], point2[0], point3[0], point4[0]]
        y = [point1[1], point2[1], point3[1], point4[1]]

        ax.plot(
            [0, point4[0] + settings["i_high"] / 2],
            [settings["i_high"], settings["i_high"]],
            color="gold",
            linestyle="dotted",
            label="87INST",
        )
        ax.fill_betweenx(
            [point4[1], point4[1] + settings["i_high"] / 2],
            [point4[0] + settings["i_high"] / 2, point4[0] + settings["i_high"] / 2],
            color="gold",
            alpha=0.1,
            label="87INST Oper.",
        )
        ax.plot(
            x,
            y,
            color="plum",
            linestyle="dotted",
            marker=".",
            label="87R",
        )
        ax.fill_betweenx(
            y[:4],
            x[:4],
            color="plum",
            alpha=0.1,
            label="87R Oper.",
        )
        ax.plot(
            [settings["i_r"]],
            [settings["i_d"]],
            color="red",
            marker="x",
        )
        ax.text(
            settings["i_r"] + 0.1,
            settings["i_d"] + 0.1,
            "("
            + str(round(settings["i_r"], 2))
            + ", "
            + str(round(settings["i_d"], 2))
            + ")",
        )
        ax.set_xlabel("Ir", loc="right")
        ax.set_ylabel("Id", loc="top")
        ax.set_xlim([0, point4[0] + settings["i_high"] / 2])
        ax.set_ylim([0, point4[1] + settings["i_high"] / 2])
        ax.legend(loc="lower right")
        ax.set_title("87T Operation Area")
        self.canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWidget = MainWidget()
    myWidget.show()
    app.exec_()
