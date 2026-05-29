# ============================================================
# plot_service.py
# ------------------------------------------------------------
# Contiene todas las funciones de generación de gráficas.
# Usa matplotlib para crear las visualizaciones y las muestra
# en ventanas independientes (plt.show()).
#
# Separar las gráficas de la UI permite reutilizarlas o
# modificarlas sin tocar la ventana principal.
# ============================================================

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


# ============================================================
# CONFIGURACIÓN GLOBAL DE MATPLOTLIB
# ------------------------------------------------------------
# Se aplica a todas las gráficas de la aplicación.
# ============================================================
rcParams.update({
    "figure.facecolor": "#F8FAFC",   # Fondo de la figura
    "axes.facecolor":   "#FFFFFF",   # Fondo del área de graficado
    "axes.spines.top":    False,     # Ocultar borde superior
    "axes.spines.right":  False,     # Ocultar borde derecho
    "axes.spines.left":   True,
    "axes.spines.bottom": True,
    "font.family":      "Segoe UI",
    "font.size":        10,
    "axes.titlesize":   11,
    "axes.labelsize":   10,
})


# ============================================================
# FUNCIÓN: graficar_demograficas
# ------------------------------------------------------------
# Muestra en una sola figura las distribuciones de Edad
# (histograma) y Género (barras), una al lado de la otra.
#
# Parámetros:
#   data → DataFrame con los datos del Excel
#
# Lanza:
#   ValueError → si no hay columnas de Edad o Género
# ============================================================
def graficar_demograficas(data):
    # Seleccionar solo las columnas que existan en el DataFrame
    cols = [(c, t) for c, t in [("Edad", "hist"), ("Genero", "barras")]
            if c in data.columns]

    if not cols:
        raise ValueError("No se encontraron columnas de Edad o Género")

    # Crear subgráficas lado a lado
    fig, axes = plt.subplots(1, len(cols), figsize=(4.5 * len(cols), 3.4))

    # Si solo hay una columna, axes no es lista → convertir
    if len(cols) == 1:
        axes = [axes]

    for ax, (col, tipo) in zip(axes, cols):
        if tipo == "hist":
            # Histograma para variables numéricas (Edad)
            ax.hist(
                data[col].dropna(),
                bins=10,
                color=COLOR_PRIMARY,
                edgecolor="white",
                alpha=0.8
            )
            ax.set_ylabel("Frecuencia", fontsize=8)

        else:
            # Gráfica de barras para variables categóricas (Género)
            conteo = data[col].value_counts()

            bars = ax.bar(
                conteo.index.astype(str),
                conteo.values,
                color=COLORES_BARRAS[:len(conteo)],
                edgecolor="white"
            )

            # Mostrar el conteo encima de cada barra
            for bar in bars:
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + 0.3,
                    str(int(bar.get_height())),
                    ha="center", va="bottom",
                    fontsize=8, fontweight="bold"
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


# ============================================================
# FUNCIÓN: graficar_preguntas
# ------------------------------------------------------------
# Muestra en una cuadrícula todas las preguntas binomiales
# de la encuesta (máx. 6 preguntas, en 2 columnas).
#
# Parámetros:
#   data → DataFrame con los datos del Excel
#
# Lanza:
#   ValueError → si no hay columnas de preguntas reconocidas
# ============================================================
def graficar_preguntas(data):
    # Filtrar solo las preguntas que existan en el DataFrame
    preguntas = [(c, t) for c, t in PREGUNTAS_GRAFICAS if c in data.columns]

    if not preguntas:
        raise ValueError("No se encontraron columnas de encuesta")

    n = len(preguntas)

    # Organizar en 2 columnas (ceil division para filas)
    cols_fig  = 2
    filas_fig = (n + cols_fig - 1) // cols_fig

    fig, axes = plt.subplots(
        filas_fig, cols_fig,
        figsize=(4.6 * cols_fig, 3.1 * filas_fig)
    )

    # Normalizar axes a lista plana para iterar fácilmente
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

        # Mostrar conteo encima de cada barra
        for bar in bars:
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.3,
                str(int(bar.get_height())),
                ha="center", va="bottom",
                fontsize=8, fontweight="bold"
            )

        ax.set_title(titulo, fontsize=9, fontweight="bold")
        ax.set_ylabel("Cantidad", fontsize=8)
        ax.tick_params(axis="x", labelsize=8)
        ax.tick_params(axis="y", labelsize=8)
        ax.grid(True, alpha=0.2, linestyle="--", axis="y")

    # Ocultar subgráficas vacías si el número de preguntas es impar
    for j in range(i + 1, len(axes)):
        axes[j].set_visible(False)

    fig.suptitle("Resultados de Encuesta", fontsize=10, fontweight="bold", y=1.02)
    plt.tight_layout()
    plt.show()


# ============================================================
# FUNCIÓN: graficar_area
# ------------------------------------------------------------
# Dibuja la curva de distribución normal y sombrea la región
# correspondiente al tipo de probabilidad calculada.
#
# Se usa tanto para el módulo normal (variable numérica)
# como para el módulo binomial (aproximación).
#
# Parámetros:
#   a         → valor límite (izquierdo para "entre", único para los demás)
#   b         → valor límite derecho (solo para tipo "entre")
#   tipo      → "exacta" | "menor" | "mayor" | "entre"
#   mu_       → media μ de la distribución a graficar
#   sigma_    → desviación estándar σ
#   subtitulo → texto adicional en el título (ej. nombre de la pregunta)
#
# Lanza:
#   ValueError → si μ o σ no están calculados, o σ = 0
# ============================================================
def graficar_area(a=None, b=None, tipo="menor", mu_=None, sigma_=None, subtitulo=""):
    m = mu_
    s = sigma_

    if m is None or s is None or s == 0:
        raise ValueError("Primero calcule μ y σ")

    # Rango de x: 4 desviaciones estándar a cada lado de la media
    x = np.linspace(m - 4 * s, m + 4 * s, 500)
    y = norm.pdf(x, m, s)   # Densidad de probabilidad en cada punto

    # Color del área sombreada según el tipo de cálculo
    color = COLORES_PROB.get(tipo, ACCENT4)

    fig, ax = plt.subplots(figsize=(8, 4.5))

    # Curva de la distribución normal
    ax.plot(x, y, color=TEXT, linewidth=2)

    # Línea vertical punteada en la media
    ax.axvline(
        m, color=ACCENT1, linestyle="--",
        linewidth=1.5, alpha=0.7,
        label=f"μ = {m:.3f}"
    )

    # Determinar la máscara (región a sombrear) y la etiqueta
    if tipo == "menor":
        # Área a la izquierda de a → P(X < a)
        mascara  = x <= a
        etiqueta = f"P(X < {a:.3f})"

    elif tipo == "mayor":
        # Área a la derecha de a → P(X > a)
        mascara  = x >= a
        etiqueta = f"P(X > {a:.3f})"

    elif tipo == "entre":
        # Área entre a y b → P(a < X < b)
        mascara  = (x >= a) & (x <= b)
        etiqueta = f"P({a:.3f} < X < {b:.3f})"

    elif tipo == "exacta":
        # Intervalo ±0.5 alrededor de a → corrección de continuidad
        mascara  = (x >= a - 0.5) & (x <= a + 0.5)
        etiqueta = f"P(X ≈ {a:.3f}) [±0.5]"

    else:
        return

    # Rellenar la región correspondiente bajo la curva
    ax.fill_between(
        x[y > 0], y[y > 0],
        where=mascara[y > 0],
        color=color, alpha=0.4,
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