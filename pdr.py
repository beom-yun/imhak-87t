class PDR:
    def __init__(self):
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

    def set_pdr(self, **kwargs):
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

    def reset_pdr(self):
        self.set_pdr(
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
        )

    def get_pdr(self):
        return {
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
        }

    def cal_crossing_points(self):
        if self.i_low and self.slope_1:
            cross_1 = self.i_low / self.slope_1, self.i_low
        else:
            cross_1 = None

        if self.slope_1 and self.slope_2:
            cross_2 = self.knee_point, self.slope_1 * self.knee_point
        else:
            cross_2 = None

        if self.slope_2 and self.i_high:
            cross_3 = (
                self.i_high - (self.slope_1 - self.slope_2) * self.knee_point
            ) / self.slope_2, self.i_high
        else:
            cross_3 = None

        return cross_1, cross_2, cross_3

    def print_pdr(self):
        print("*" * 50)
        print(f"변압비 {self.v_1}/{self.v_2}/{self.v_3}")
        print(
            f"CT비 {self.ct_ratio_1}/{self.i_n}, {self.ct_ratio_2}/{self.i_n}, {self.ct_ratio_3}/{self.i_n}"
        )
        print(f"I_low {self.i_low}")
        print(f"Knee point {self.knee_point}")
        print(f"Slope1 {self.slope_1}")
        print(f"Slope2 {self.slope_2}")
        print(f"I_high {self.i_high}")
        print(f"Factor {self.factor_1}, {self.factor_2}, {self.factor_3}")
        print("*" * 50)


# pdr = PDR()
# pdr.cal_crossing_points()
# pdr.set_pdr(
#     v_1=22900,
#     v_2=600,
#     v_3=600,
#     ct_ratio_1=200,
#     ct_ratio_2=5000,
#     ct_ratio_3=5000,
#     i_n=5,
#     i_low=0.2,
#     i_high=10,
#     knee_point=1.5,
#     slope_1=0.41,
#     slope_2=0.7,
#     factor_1=1,
#     factor_2=0.66,
#     factor_3=0.66,
# )
# print(pdr.get_pdr())
