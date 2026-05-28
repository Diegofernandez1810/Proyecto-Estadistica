import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
from scipy.stats import norm

from .config import (
    COLOR_PRIMARY,
    TEXT,
    ACCENT1,
    ACCENT4,
    COLORES_BARRAS,
    COLORES_PROB,
    PREGUNTAS_GRAFICAS
)


rcParams.update({
    "figure.facecolor": "#F8FAFC",
    "axes.facecolor": "#FFFFFF",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.spines.left": True,
    "axes.spines.bottom": True,
    "font.family": "Segoe UI",
    "font.size": 10,
    "axes.titlesize": 11,
    "axes.labelsize": 10,
})


def graficar_demograficas(data):
    cols = [(c, t) for c, t in [("Edad", "hist"), ("Genero", "barras")] if c in data.columns]

    if not cols:
        raise ValueError("No se encontraron columnas de Edad o Género")

    fig, axes = plt.subplots(1, len(cols), figsize=(4.5 * len(cols), 3.4))

    if len(cols) == 1:
        axes = [axes]

    for ax, (col, tipo) in zip(axes, cols):
        if tipo == "hist":
            ax.hist(
                data[col].dropna(),
                bins=10,
                color=COLOR_PRIMARY,
                edgecolor="white",
                alpha=0.8
            )
            ax.set_ylabel("Frecuencia", fontsize=8)

        else:
            conteo = data[col].value_counts()

            bars = ax.bar(
                conteo.index.astype(str),
                conteo.values,
                color=COLORES_BARRAS[:len(conteo)],
                edgecolor="white"
            )

            for bar in bars:
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + 0.3,
                    str(int(bar.get_height())),
                    ha="center",
                    va="bottom",
                    fontsize=8,
                    fontweight="bold"
                )

            ax.set_ylabel("Cantidad", fontsize=8)

        ax.set_title(col, fontweight="bold", fontsize=9)
        ax.set_xlabel(col, fontsize=8)
        ax.tick_params(axis="x", labelsize=8)
        ax.tick_params(axis="y", labelsize=8)
        ax.grid(True, alpha=0.15, linestyle="--", color="#94A3B8")

    fig.suptitle("Análisis Demográfico", fontsize=10, fontweight="bold", y=1.02)
    plt.tight_layout()
    plt.show()


def graficar_preguntas(data):
    preguntas = [(c, t) for c, t in PREGUNTAS_GRAFICAS if c in data.columns]

    if not preguntas:
        raise ValueError("No se encontraron columnas de encuesta")

    n = len(preguntas)

    cols_fig = 2
    filas_fig = (n + cols_fig - 1) // cols_fig

    fig, axes = plt.subplots(
        filas_fig,
        cols_fig,
        figsize=(4.6 * cols_fig, 3.1 * filas_fig)
    )

    if n == 1:
        axes = [axes]
    else:
        axes = axes.flatten()

    for i, (col, titulo) in enumerate(preguntas):
        ax = axes[i]
        conteo = data[col].value_counts()

        bars = ax.bar(
            conteo.index.astype(str),
            conteo.values,
            color=COLORES_BARRAS[:len(conteo)],
            edgecolor="white"
        )

        for bar in bars:
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.3,
                str(int(bar.get_height())),
                ha="center",
                va="bottom",
                fontsize=8,
                fontweight="bold"
            )

        ax.set_title(titulo, fontsize=9, fontweight="bold")
        ax.set_ylabel("Cantidad", fontsize=8)
        ax.tick_params(axis="x", labelsize=8)
        ax.tick_params(axis="y", labelsize=8)
        ax.grid(True, alpha=0.2, linestyle="--", axis="y")

    for j in range(i + 1, len(axes)):
        axes[j].set_visible(False)

    fig.suptitle("Resultados de Encuesta", fontsize=10, fontweight="bold", y=1.02)
    plt.tight_layout()
    plt.show()


def graficar_area(a=None, b=None, tipo="menor", mu_=None, sigma_=None, subtitulo=""):
    m = mu_
    s = sigma_

    if m is None or s is None or s == 0:
        raise ValueError("Primero calcule μ y σ")

    x = np.linspace(m - 4 * s, m + 4 * s, 500)
    y = norm.pdf(x, m, s)

    color = COLORES_PROB.get(tipo, ACCENT4)

    fig, ax = plt.subplots(figsize=(8, 4.5))

    ax.plot(x, y, color=TEXT, linewidth=2)

    ax.axvline(
        m,
        color=ACCENT1,
        linestyle="--",
        linewidth=1.5,
        alpha=0.7,
        label=f"μ = {m:.3f}"
    )

    if tipo == "menor":
        mascara = x <= a
        etiqueta = f"P(X < {a:.3f})"

    elif tipo == "mayor":
        mascara = x >= a
        etiqueta = f"P(X > {a:.3f})"

    elif tipo == "entre":
        mascara = (x >= a) & (x <= b)
        etiqueta = f"P({a:.3f} < X < {b:.3f})"

    elif tipo == "exacta":
        mascara = (x >= a - 0.5) & (x <= a + 0.5)
        etiqueta = f"P(X ≈ {a:.3f}) [±0.5]"

    else:
        return

    ax.fill_between(
        x[y > 0],
        y[y > 0],
        where=mascara[y > 0],
        color=color,
        alpha=0.4,
        label=etiqueta
    )

    titulo = "Distribución Normal"

    if subtitulo:
        titulo += f"\n{subtitulo}"

    ax.set_title(titulo, fontsize=12, fontweight="bold", pad=15)
    ax.set_xlabel("Valor", fontsize=10)
    ax.set_ylabel("Densidad de Probabilidad", fontsize=10)
    ax.legend(loc="upper right", framealpha=0.95, fontsize=9)
    ax.grid(True, alpha=0.2, linestyle="--")

    plt.tight_layout()
    plt.show()