import matplotlib.pyplot as plt


def draw_graph(settings):
    # print("settings", settings)
    point1 = (0, settings["i_low"])
    point2 = settings["cross_1"]
    point3 = settings["cross_2"]
    point4 = settings["cross_3"]
    x = [point1[0], point2[0], point3[0], point4[0]]
    y = [point1[1], point2[1], point3[1], point4[1]]
    # print(point1, point2, point3, point4)

    plt.plot(
        [0, point4[0] + settings["i_high"] / 2],
        [settings["i_high"], settings["i_high"]],
        color="gold",
        linestyle="dotted",
        label="87INST",
    )
    plt.fill_betweenx(
        [point4[1], point4[1] + settings["i_high"] / 2],
        [point4[0] + settings["i_high"] / 2, point4[0] + settings["i_high"] / 2],
        color="gold",
        alpha=0.1,
        label="87INST Oper.",
    )
    plt.plot(
        x,
        y,
        color="plum",
        linestyle="dotted",
        marker=".",
        label="87R",
    )
    plt.fill_betweenx(
        y[:4],
        x[:4],
        color="plum",
        alpha=0.1,
        label="87R Oper.",
    )
    plt.plot(
        [settings["i_r"]],
        [settings["i_d"]],
        color="red",
        marker="x",
    )
    plt.text(
        settings["i_r"] + 0.2,
        settings["i_d"] + 0.2,
        "("
        + str(round(settings["i_r"], 2))
        + ", "
        + str(round(settings["i_d"], 2))
        + ")",
    )
    plt.xlabel("Ir", loc="right")
    plt.ylabel("Id", loc="top")
    plt.xlim([0, point4[0] + settings["i_high"] / 2])
    plt.ylim([0, point4[1] + settings["i_high"] / 2])
    plt.legend(loc="lower right")
    plt.show()
