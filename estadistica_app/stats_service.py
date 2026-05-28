# ============================================================
# stats_service.py
# ------------------------------------------------------------
# Contiene todas las funciones de cálculo estadístico.
# Están separadas de la UI para que puedan probarse o
# reutilizarse independientemente.
#
# Usa:
#   numpy  → para media, desviación estándar y raíz cuadrada
#   scipy  → para la función de distribución acumulada (CDF)
#             de la distribución normal
# ============================================================

import numpy as np
from scipy.stats import norm


# ============================================================
# MÓDULO NORMAL — Variable numérica (ej. Edad)
# ============================================================

def calcular_media_desviacion(serie):
    """
    Calcula los parámetros estadísticos básicos de una serie numérica.

    Parámetros:
        serie → pandas Series con valores numéricos

    Retorna:
        mu    → media aritmética (μ)
        sigma → desviación estándar poblacional (σ)
        n     → número de datos válidos (sin NaN)
    """
    serie = serie.dropna()       # Eliminar valores vacíos
    mu    = float(np.mean(serie))
    sigma = float(np.std(serie)) # std() por defecto usa denominador n (poblacional)
    n     = len(serie)
    return mu, sigma, n


def calcular_prob_exacta(x, mu, sigma):
    """
    Calcula P(X ≈ x) usando la corrección de continuidad.

    En distribuciones continuas P(X = x) = 0 exactamente.
    Para aproximar una probabilidad "exacta" se usa un
    intervalo de ±0.5 alrededor de x:
        P(x - 0.5 ≤ X ≤ x + 0.5)

    Parámetros:
        x     → valor exacto a evaluar
        mu    → media de la distribución
        sigma → desviación estándar

    Retorna:
        float → probabilidad aproximada (entre 0 y 1)
    """
    return norm.cdf(x + 0.5, mu, sigma) - norm.cdf(x - 0.5, mu, sigma)


def calcular_prob_menor(x, mu, sigma):
    """
    Calcula P(X < x): probabilidad acumulada hasta x.

    Usa la CDF (Cumulative Distribution Function) de la normal,
    que devuelve el área bajo la curva a la izquierda de x.

    Parámetros:
        x     → límite superior
        mu    → media
        sigma → desviación estándar

    Retorna:
        float → probabilidad (entre 0 y 1)
    """
    return norm.cdf(x, mu, sigma)


def calcular_prob_mayor(x, mu, sigma):
    """
    Calcula P(X > x): probabilidad de superar el valor x.

    Equivale al complemento de la CDF:
        P(X > x) = 1 - P(X ≤ x)

    Parámetros:
        x     → límite inferior
        mu    → media
        sigma → desviación estándar

    Retorna:
        float → probabilidad (entre 0 y 1)
    """
    return 1 - norm.cdf(x, mu, sigma)


def calcular_prob_entre(a, b, mu, sigma):
    """
    Calcula P(a < X < b): probabilidad de estar entre dos valores.

    Se obtiene restando las CDF:
        P(a < X < b) = CDF(b) - CDF(a)

    Parámetros:
        a     → límite inferior del intervalo
        b     → límite superior del intervalo (debe ser > a)
        mu    → media
        sigma → desviación estándar

    Retorna:
        float → probabilidad (entre 0 y 1)
    """
    return norm.cdf(b, mu, sigma) - norm.cdf(a, mu, sigma)


# ============================================================
# MÓDULO BINOMIAL → NORMAL
# ============================================================

def calcular_parametros_binomiales(data, columna, exito):
    """
    Calcula los parámetros de la aproximación normal a la binomial
    a partir de una columna de respuestas Sí/No de la encuesta.

    Fundamento teórico:
        Si X ~ Binomial(n, p), cuando n es grande se puede
        aproximar con una Normal donde:
            μ = n · p
            σ = √(n · p · q),   q = 1 - p

    Parámetros:
        data    → DataFrame con los datos del Excel
        columna → nombre de la columna binomial (ej. "Favor_IA")
        exito   → valor que se considera "éxito" (ej. "Si")

    Retorna:
        n        → total de encuestados
        k        → número de respuestas "éxito"
        p        → proporción de éxito  (k / n)
        q        → proporción de fracaso (1 - p)
        mu_bin   → media de la aproximación normal (n · p)
        sigma_bin→ desviación estándar (√(n · p · q))
    """
    # Convertir a string para comparación robusta (evita errores de tipo)
    serie = data[columna].dropna().astype(str)

    n = len(serie)
    k = (serie == exito).sum()   # Conteo de respuestas que coinciden con "éxito"

    # Protección contra división por cero si no hay datos
    p = k / n if n > 0 else 0
    q = 1 - p

    mu_bin    = n * p
    sigma_bin = np.sqrt(n * p * q)

    return n, k, p, q, mu_bin, sigma_bin