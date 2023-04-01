class PDR:
    def __init__(self):
        self.winding = 0  # 변압기 종류(2권선 or 3권선)
        self.v_1 = 0  # 변압비 전압(1권선)
        self.v_2 = 0  # 변압비 전압(2권선)
        self.v_3 = 0  # 변압비 전압(3권선)
        self.ct_ratio_1 = 0  # CT 1차 전류(1권선)
        self.ct_ratio_2 = 0  # CT 1차 전류(2권선)
        self.ct_ratio_3 = 0  # CT 1차 전류(3권선)
        self.i_n = 0  # CT 2차측 정격전류
        self.i_low = 0  # Low(한시) 전류
        self.i_high = 0  # High(순시) 전류
        self.knee_point = 0  # Knee point
        self.slope_1 = 0  # Slope1
        self.slope_2 = 0  # Slope2
        self.factor_1 = 0  # 1권선 Factor
        self.factor_2 = 0  # 2권선 Factor
        self.factor_3 = 0  # 3권선 Factor
        self.cross_1 = None  # Low 전류와 Slope1의 교차점
        self.cross_2 = None  # Slope1과 Slope2의 교차점
        self.cross_3 = None  # Slope2와 High 전류의 교차점
        self.i_d = 0  # 차전류(Id)
        self.i_r = 0  # 억제전류(Ir)
        self.i_1 = 0  # 1차측 전류
        self.i_2 = 0  # 2차측 전류
        self.i_3 = 0  # 3차측 전류

    def set_pdr(self, **kwargs):
        self.winding = kwargs["winding"] if "winding" in kwargs else 0
        self.v_1 = kwargs["v_1"] if "v_1" in kwargs else 0
        self.v_2 = kwargs["v_2"] if "v_2" in kwargs else 0
        self.v_3 = kwargs["v_3"] if "v_3" in kwargs else 0
        self.ct_ratio_1 = kwargs["ct_ratio_1"] if "ct_ratio_1" in kwargs else 0
        self.ct_ratio_2 = kwargs["ct_ratio_2"] if "ct_ratio_2" in kwargs else 0
        self.ct_ratio_3 = kwargs["ct_ratio_3"] if "ct_ratio_3" in kwargs else 0
        self.i_n = kwargs["i_n"] if "i_n" in kwargs else 0
        self.i_low = kwargs["i_low"] if "i_low" in kwargs else 0
        self.i_high = kwargs["i_high"] if "i_high" in kwargs else 0
        self.knee_point = kwargs["knee_point"] if "knee_point" in kwargs else 0
        self.slope_1 = kwargs["slope_1"] if "slope_1" in kwargs else 0
        self.slope_2 = kwargs["slope_2"] if "slope_2" in kwargs else 0
        self.factor_1 = kwargs["factor_1"] if "factor_1" in kwargs else 0
        self.factor_2 = kwargs["factor_2"] if "factor_2" in kwargs else 0
        self.factor_3 = kwargs["factor_3"] if "factor_3" in kwargs else 0
        self.cross_1, self.cross_2, self.cross_3 = self.cal_crossing_points()
        self.i_d = kwargs["i_d"] if "i_d" in kwargs else 0
        self.i_r = kwargs["i_r"] if "i_r" in kwargs else 0
        self.i_1 = kwargs["i_1"] if "i_1" in kwargs else 0
        self.i_2 = kwargs["i_2"] if "i_2" in kwargs else 0
        self.i_3 = kwargs["i_3"] if "i_3" in kwargs else 0

    def reset_pdr(self):
        self.set_pdr(
            winding=0,
            v_1=0,
            v_2=0,
            v_3=0,
            ct_ratio_1=0,
            ct_ratio_2=0,
            ct_ratio_3=0,
            i_n=0,
            i_low=0,
            i_high=0,
            knee_point=0,
            slope_1=0,
            slope_2=0,
            factor_1=0,
            factor_2=0,
            factor_3=0,
            i_d=0,
            i_r=0,
            i_1=0,
            i_2=0,
            i_3=0,
        )

    def get_pdr(self):
        return {
            "winding": self.winding,
            "v_1": self.v_1,
            "v_2": self.v_2,
            "v_3": self.v_3,
            "ct_ratio_1": self.ct_ratio_1,
            "ct_ratio_2": self.ct_ratio_2,
            "ct_ratio_3": self.ct_ratio_3,
            "i_n": self.i_n,
            "i_low": self.i_low,
            "i_high": self.i_high,
            "knee_point": self.knee_point,
            "slope_1": self.slope_1,
            "slope_2": self.slope_2,
            "factor_1": self.factor_1,
            "factor_2": self.factor_2,
            "factor_3": self.factor_3,
            "cross_1": self.cross_1,
            "cross_2": self.cross_2,
            "cross_3": self.cross_3,
            "i_d": self.i_d,
            "i_r": self.i_r,
            "i_1": self.i_1,
            "i_2": self.i_2,
            "i_3": self.i_3,
        }

    def cal_crossing_points(self):
        if self.i_low and self.slope_1:
            cross_1 = self.i_low / self.slope_1, self.i_low
        else:
            cross_1 = (0, 0)

        if self.slope_1 and self.slope_2:
            cross_2 = self.knee_point, self.slope_1 * self.knee_point
        else:
            cross_2 = (0, 0)

        if self.slope_2 and self.i_high:
            cross_3 = (
                self.i_high - (self.slope_1 - self.slope_2) * self.knee_point
            ) / self.slope_2, self.i_high
        else:
            cross_3 = (0, 0)

        return cross_1, cross_2, cross_3

    def cal_factors(self):
        self.factor_1 = 1
        self.factor_2 = (self.ct_ratio_2 / self.ct_ratio_1) / (self.v_1 / self.v_2)
        self.factor_3 = (
            (self.ct_ratio_3 / self.ct_ratio_1) / (self.v_1 / self.v_3)
            if self.winding == 3
            else 0
        )

    def cal_i_d_and_i_r(self):
        i_1 = self.i_1 * self.factor_1
        i_2 = self.i_2 * self.factor_2
        i_3 = self.i_3 * self.factor_3
        self.i_d = abs(i_1 - i_2 - i_3) / 5
        self.i_r = (i_1 + i_2 + i_3) / 5

    def cal_pickup(self):
        if self.cross_3 and self.i_d >= self.i_high:
            # print(f"차전류 {self.i_d}가 순시설정값 {self.i_high}보다 높으므로 순시 동작")
            return "동작", "순시(87INST)"
        if self.cross_2[0] < self.i_r:
            graph_i_d = (
                self.slope_2 * self.i_r
                + (self.slope_1 - self.slope_2) * self.cross_2[0]
            )
            if self.i_d >= graph_i_d:
                # print(
                #     f"차전류 {self.i_d}가 그래프 위의 점 ({self.i_r}, {graph_i_d}) 보다 높으므로 한시 동작(slope2 영역)"
                # )
                return "동작", "한시(87R, Slope2)"
        if self.cross_1[0] < self.i_r <= self.cross_2[0]:
            graph_i_d = self.slope_1 * self.i_r
            if self.i_d >= graph_i_d:
                # print(
                #     f"차전류 {self.i_d}가 그래프 위의 점 ({self.i_r}, {graph_i_d}) 보다 높으므로 한시 동작(slope1 영역)"
                # )
                return "동작", "한시(87R, Slope1)"
        if self.i_r <= self.cross_1[0]:
            if self.i_d >= self.i_low:
                # print(
                #     f"차전류 {self.i_r}가 그래프 위의 점 ({self.i_r}, {self.i_low}) 보다 높으므로 한시 동작(i_low 영역)"
                # )
                return "동작", "한시(87R)"
        return "미동작", "-"
