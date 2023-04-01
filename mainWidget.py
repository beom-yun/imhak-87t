import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from pdr import PDR
from drawGraph import draw_graph

form_class = uic.loadUiType("form.ui")[0]


class MainWidget(QWidget, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btn_cal.clicked.connect(self.btn_cal_clicked)
        self.pdr = PDR()

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
        draw_graph(settings)

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
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWidget = MainWidget()
    myWidget.show()
    app.exec_()
