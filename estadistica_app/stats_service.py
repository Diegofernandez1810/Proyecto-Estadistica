import numpy as np
from scipy.stats import norm


def calcular_media_desviacion(serie):
    serie = serie.dropna()

    mu = float(np.mean(serie))
    sigma = float(np.std(serie))
    n = len(serie)

    return mu, sigma, n


def calcular_prob_exacta(x, mu, sigma):
    return norm.cdf(x + 0.5, mu, sigma) - norm.cdf(x - 0.5, mu, sigma)


def calcular_prob_menor(x, mu, sigma):
    return norm.cdf(x, mu, sigma)


def calcular_prob_mayor(x, mu, sigma):
    return 1 - norm.cdf(x, mu, sigma)


def calcular_prob_entre(a, b, mu, sigma):
    return norm.cdf(b, mu, sigma) - norm.cdf(a, mu, sigma)


def calcular_parametros_binomiales(data, columna, exito):
    serie = data[columna].dropna().astype(str)

    n = len(serie)
    k = (serie == exito).sum()

    p = k / n if n > 0 else 0
    q = 1 - p

    mu_bin = n * p
    sigma_bin = np.sqrt(n * p * q)

    return n, k, p, q, mu_bin, sigma_bin