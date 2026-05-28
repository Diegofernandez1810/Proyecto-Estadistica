# ============================================================
# data_service.py
# ------------------------------------------------------------
# Responsable exclusivamente de la carga y limpieza de datos.
# Separa la lógica de lectura del archivo de la interfaz
# gráfica, siguiendo el principio de separación de
# responsabilidades.
# ============================================================

import pandas as pd
from .config import RENOMBRAR


def cargar_datos_excel(ruta_archivo):
    """
    Lee un archivo Excel de Google Forms y prepara el DataFrame
    para su uso en la aplicación.

    Pasos que realiza:
      1. Lee el archivo .xlsx con pandas
      2. Renombra las columnas de Google Forms (preguntas largas)
         a nombres cortos definidos en config.RENOMBRAR
      3. Elimina columnas innecesarias que genera Google Forms
         automáticamente ("Marca temporal" y correo electrónico)

    Parámetros:
        ruta_archivo → string con la ruta al archivo .xlsx

    Retorna:
        data → DataFrame limpio y listo para análisis

    Lanza:
        Exception → si el archivo no existe o tiene formato inválido
    """

    # Paso 1: Leer el Excel
    data = pd.read_excel(ruta_archivo)

    # Paso 2: Renombrar columnas reconocidas (solo las que existan)
    data.rename(
        columns={k: v for k, v in RENOMBRAR.items() if k in data.columns},
        inplace=True
    )

    # Paso 3: Eliminar columnas generadas por Google Forms
    # que no aportan al análisis estadístico
    data.drop(
        columns=["Marca temporal", "Dirección de correo electrónico"],
        errors="ignore",   # No lanza error si la columna no existe
        inplace=True
    )

    return data