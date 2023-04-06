import matplotlib.pyplot as plt


def draw_graph(settings, canvas, new_dialog):
    if new_dialog:
        ax = plt
        plt.connect("motion_notify_event", mouse_cursor)
    else:
        canvas.figure.clf()
        ax = canvas.figure.subplots()
        canvas.mpl_connect("motion_notify_event", mouse_cursor)
    point1 = (0, settings["i_low"])
    point2 = settings["cross_1"]
    point3 = settings["cross_2"]
    point4 = settings["cross_3"]
    x = [point1[0], point2[0], point3[0], point4[0]]
    y = [point1[1], point2[1], point3[1], point4[1]]

    ax.plot(
        [0, 9999],
        [settings["i_high"], settings["i_high"]],
        color="gold",
        linestyle="dotted",
        label="87INST",
    )
    ax.fill_betweenx(
        [point4[1], 9999],
        [9999, 9999],
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

    if new_dialog:
        ax.xlabel("Ir", loc="right")
        ax.ylabel("Id", loc="top")
        ax.xlim([0, point4[0] + settings["i_high"] / 2])
        ax.ylim([0, point4[1] + settings["i_high"] / 2])
        ax.legend(loc="lower right")
        ax.title("87T Operation Area")
        ax.show()
    else:
        ax.set_xlabel("Ir", loc="right")
        ax.set_ylabel("Id", loc="top")
        ax.set_xlim([0, point4[0] + settings["i_high"] / 2])
        ax.set_ylim([0, point4[1] + settings["i_high"] / 2])
        ax.legend(loc="lower right")
        ax.set_title("87T Operation Area")
        canvas.draw()


def mouse_cursor(event):
    print(event)
