import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, RadioButtons, Button
import numpy as np
import threading
from .mandelbrot import mandelbrot_set
from .julia import julia_set

def plot_fractal() -> None:
    """
    Spustí GUI pro vizualizaci Mandelbrotovy a Juliovy množiny.

    Funkce:
    - úprava rozsahu výřezu (x_min, x_max, y_min, y_max)
    - změna parametrů fraktálu (počet iterací, konstantu c)
    - přepínání mezi Mandelbrotovou a Juliovou množinou
    - změna barevného schématu vykreslení
    - použítí tlačítka + / − pro přiblížení a oddálení
    - reset na výchozí hodnoty
    """

    width, height = 600, 600
    update_timer = [None]

    default_params: dict[str, float | str] = {
        "x_min": -2.0, "x_max": 2.0,
        "y_min": -2.0, "y_max": 2.0,
        "max_iter": 100,
        "c_re": -0.8, "c_im": 0.156,
        "cmap": "plasma"
    }
    cmap_list = ["plasma", "inferno", "hot", "turbo", "twilight", "viridis"]

    fig, ax = plt.subplots(figsize=(8, 8))
    plt.subplots_adjust(bottom=0.55)

    # === Slidery ===
    sliders: dict[str, Slider] = {
        "x_min": Slider(plt.axes([0.25, 0.42, 0.65, 0.02]), "x_min", -3.0, 0.0, valinit=default_params["x_min"]),
        "x_max": Slider(plt.axes([0.25, 0.39, 0.65, 0.02]), "x_max", 0.0, 3.0, valinit=default_params["x_max"]),
        "y_min": Slider(plt.axes([0.25, 0.36, 0.65, 0.02]), "y_min", -2.0, 0.0, valinit=default_params["y_min"]),
        "y_max": Slider(plt.axes([0.25, 0.33, 0.65, 0.02]), "y_max", 0.0, 2.0, valinit=default_params["y_max"]),
        "iter": Slider(plt.axes([0.25, 0.30, 0.65, 0.02]), "Iterace", 10, 1000, valinit=default_params["max_iter"], valstep=10),
        "c_re": Slider(plt.axes([0.25, 0.24, 0.65, 0.02]), "Re(c)", -1.5, 1.5, valinit=default_params["c_re"]),
        "c_im": Slider(plt.axes([0.25, 0.21, 0.65, 0.02]), "Im(c)", -1.5, 1.5, valinit=default_params["c_im"]),
    }

    # === Nadpisy sekcí ===
    fig.text(0.025, 0.76, "Typ:", fontsize=10, fontweight="bold")
    fig.text(0.025, 0.61, "Barva:", fontsize=10, fontweight="bold")
    fig.text(0.025, 0.435, "Přiblížení:", fontsize=10, fontweight="bold")

    # === Radio Buttons ===
    ax_type = plt.axes([0.025, 0.65, 0.15, 0.1])
    radio_type = RadioButtons(ax_type, ["Mandelbrotova", "Juliova"])

    ax_cmap = plt.axes([0.025, 0.5, 0.15, 0.1])
    radio_cmap = RadioButtons(ax_cmap, cmap_list)

    # === Tlačítka pro úpravu přiblížení ===
    ax_zoom_in = plt.axes([0.025, 0.38, 0.07, 0.04])
    btn_zoom_in = Button(ax_zoom_in, "+")
    ax_zoom_out = plt.axes([0.105, 0.38, 0.07, 0.04])
    btn_zoom_out = Button(ax_zoom_out, "−")

    # === Reset tlačítko ===
    ax_reset = plt.axes([0.025, 0.325, 0.15, 0.04])
    btn_reset = Button(ax_reset, "Reset")

    # === Funkce vykreslení ===
    def draw_fractal() -> None:
        x_min = sliders["x_min"].val
        x_max = sliders["x_max"].val
        y_min = sliders["y_min"].val
        y_max = sliders["y_max"].val
        max_iter = int(sliders["iter"].val)
        cmap = radio_cmap.value_selected
        fractal_type = radio_type.value_selected

        if fractal_type == "mandelbrotova":
            data = mandelbrot_set(x_min, x_max, y_min, y_max, width, height, max_iter)
            title = "Mandelbrotova množina"
        else:
            c = complex(sliders["c_re"].val, sliders["c_im"].val)
            data = julia_set(x_min, x_max, y_min, y_max, width, height, c, max_iter)
            title = f"Juliova množina pro c = {c}"

        ax.clear()
        ax.imshow(data, extent=[x_min, x_max, y_min, y_max], cmap=cmap, origin="lower")
        ax.set_title(title)
        ax.set_xlabel("Reálná část")
        ax.set_ylabel("Imaginární část")
        fig.canvas.draw_idle()

    # === Reakce na změnu hodnot ===
    def on_update(event=None) -> None:
        if update_timer[0] is not None:
            update_timer[0].cancel()
        update_timer[0] = threading.Timer(0.1, draw_fractal)
        update_timer[0].start()

    # === Přiblížení / oddálení ===
    def zoom(factor: float) -> None:
        x_min = sliders["x_min"].val
        x_max = sliders["x_max"].val
        y_min = sliders["y_min"].val
        y_max = sliders["y_max"].val
        x_center = (x_min + x_max) / 2
        y_center = (y_min + y_max) / 2
        x_range = (x_max - x_min) * factor / 2
        y_range = (y_max - y_min) * factor / 2

        sliders["x_min"].set_val(x_center - x_range)
        sliders["x_max"].set_val(x_center + x_range)
        sliders["y_min"].set_val(y_center - y_range)
        sliders["y_max"].set_val(y_center + y_range)

    # === Reset ===
    def reset_view(event=None) -> None:
        sliders["x_min"].set_val(default_params["x_min"])
        sliders["x_max"].set_val(default_params["x_max"])
        sliders["y_min"].set_val(default_params["y_min"])
        sliders["y_max"].set_val(default_params["y_max"])
        sliders["iter"].set_val(default_params["max_iter"])
        sliders["c_re"].set_val(default_params["c_re"])
        sliders["c_im"].set_val(default_params["c_im"])
        radio_cmap.set_active(cmap_list.index(default_params["cmap"]))
        radio_type.set_active(0)

    # === Události ===
    for s in sliders.values():
        s.on_changed(on_update)

    radio_cmap.on_clicked(on_update)
    radio_type.on_clicked(on_update)
    btn_zoom_in.on_clicked(lambda event: zoom(0.5))
    btn_zoom_out.on_clicked(lambda event: zoom(2.0))
    btn_reset.on_clicked(reset_view)

    draw_fractal()
    plt.show()