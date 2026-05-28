import pandas as pd

from .config import RENOMBRAR


def cargar_datos_excel(ruta_archivo):
    data = pd.read_excel(ruta_archivo)

    data.rename(
        columns={k: v for k, v in RENOMBRAR.items() if k in data.columns},
        inplace=True
    )

    data.drop(
        columns=["Marca temporal", "Dirección de correo electrónico"],
        errors="ignore",
        inplace=True
    )

    return data