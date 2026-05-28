# ============================================================
# config.py
# ------------------------------------------------------------
# Archivo de configuración central de la aplicación.
# Contiene todos los colores, constantes y mapeos de columnas.
# Al centralizar aquí, cualquier cambio visual o de datos
# se hace en un solo lugar sin tocar el resto del código.
# ============================================================


# ============================================================
# PALETA DE COLORES — TEMA OSCURO/AZUL PROFESIONAL
# ------------------------------------------------------------
# BG       → fondo general de la ventana
# CARD     → fondo de cada tarjeta/sección (blanco)
# HEADER_* → colores del encabezado superior
# ACCENT*  → colores de acento para secciones y botones
# TEXT*    → colores de texto principal y secundario
# BORDER   → color para bordes y separadores
# ============================================================

BG         = "#EEF2F7"       # Fondo general — gris azulado suave
CARD       = "#FFFFFF"       # Fondo de tarjetas — blanco puro
HEADER_BG  = "#0F172A"       # Header — azul marino muy oscuro
HEADER_TXT = "#F8FAFC"       # Texto del header — blanco suave

ACCENT1    = "#2563EB"       # Azul principal (botón cargar, borde tarjetas)
ACCENT2    = "#1D4ED8"       # Azul oscuro (gráfica demográfica)
ACCENT3    = "#3B82F6"       # Azul medio (estadísticas, preguntas)
ACCENT4    = "#0EA5E9"       # Azul cielo (probabilidad)
ACCENT5    = "#1E293B"       # Azul muy oscuro (selector de variable)

COLOR_PRIMARY   = "#2563EB"  # Color principal reutilizable
COLOR_SECONDARY = "#60A5FA"  # Azul claro secundario
COLOR_SUCCESS   = "#059669"  # Verde — mensajes de éxito
COLOR_WARNING   = "#D97706"  # Naranja — advertencias
COLOR_DANGER    = "#DC2626"  # Rojo — errores

TEXT       = "#111827"       # Texto principal — negro suave
TEXT_LIGHT = "#64748B"       # Texto secundario — gris azulado
BORDER     = "#CBD5E1"       # Bordes y separadores

# Colores de los 4 tipos de botones de probabilidad
BTN_EXACTA = "#7C3AED"       # Morado  — P(X ≈ x) exacta
BTN_MENOR  = "#2563EB"       # Azul    — P(X < x) menor
BTN_MAYOR  = "#059669"       # Verde   — P(X > x) mayor
BTN_RANGO  = "#0EA5E9"       # Celeste — P(a < X < b) rango


# ============================================================
# MODOS DE OPERACIÓN
# ------------------------------------------------------------
# La app puede funcionar en dos modos excluyentes:
#   MODO_NORMAL   → se usa una columna numérica (ej. Edad)
#                   para calcular μ, σ y probabilidades
#   MODO_BINOMIAL → se usan las preguntas Sí/No de la encuesta
#                   para aproximar con la distribución normal
#
# OPCION_BINOMIAL es el texto que aparece en el Combobox
# para que el usuario active el modo binomial.
# ============================================================

MODO_NORMAL   = "normal"
MODO_BINOMIAL = "binomial"
OPCION_BINOMIAL = "Encuesta binomial"


# ============================================================
# COLORES PARA GRÁFICAS DE BARRAS
# ------------------------------------------------------------
# Lista de colores aplicados en orden a las barras de cada
# gráfica categórica. Si hay más categorías que colores,
# se recicla desde el inicio.
# ============================================================

COLORES_BARRAS = [
    "#2563EB",   # Azul principal
    "#3B82F6",   # Azul medio
    "#0EA5E9",   # Azul cielo
    "#0284C7",   # Azul oscuro
    "#1D4ED8",   # Azul marino
    "#059669",   # Verde
    "#7C3AED",   # Morado
    "#F59E0B"    # Ámbar (contraste)
]

# Mapa tipo → color para sombrear la curva normal
COLORES_PROB = {
    "menor":  BTN_MENOR,
    "mayor":  BTN_MAYOR,
    "entre":  BTN_RANGO,
    "exacta": BTN_EXACTA
}


# ============================================================
# MAPEO DE COLUMNAS: Google Forms → nombres internos
# ------------------------------------------------------------
# Google Forms genera columnas con el texto exacto de cada
# pregunta, lo que hace difícil referenciarlas en el código.
# Este diccionario traduce esos nombres largos a nombres
# cortos usados en toda la aplicación.
#
# Se incluyen variantes con/sin tildes para mayor robustez.
# ============================================================

RENOMBRAR = {
    "Edad"    : "Edad",
    "Genero"  : "Genero",
    "Género"  : "Genero",

    "¿Prefiere laptop o computadora de escritorio?"  : "Laptop_vs_Escritorio",
    "¿Utiliza redes sociales diariamente?"           : "Redes_Sociales",

    "¿Utilizas mas el teléfono o la televisión?"     : "Telefono_vs_TV",
    "¿Utilizas más el teléfono o la televisión?"     : "Telefono_vs_TV",

    "¿Está a favor del uso de inteligencia artificial?"                    : "Favor_IA",
    "¿Está a favor del uso de inteligencia artificial en la educación?"    : "Favor_IA_Educacion",
    "¿Esta a favor del uso de inteligencia artificial en la educacion?"    : "Favor_IA_Educacion",
    "¿Está a favor del uso de inteligencia artificial en la educacion?"    : "Favor_IA_Educacion",
    "¿Esta a favor del uso de inteligencia artificial en la educación?"    : "Favor_IA_Educacion",

    "¿Prefiere clases virtuales o presenciales?"     : "Clases_Virtuales",
}

# Columnas categóricas (Sí/No o A/B) usadas en el módulo binomial
COLUMNAS_BARRAS_COLS = [
    "Genero",
    "Laptop_vs_Escritorio",
    "Redes_Sociales",
    "Telefono_vs_TV",
    "Favor_IA",
    "Favor_IA_Educacion",
    "Clases_Virtuales"
]

# Pares (columna, título legible) para las gráficas de preguntas
PREGUNTAS_GRAFICAS = [
    ("Laptop_vs_Escritorio", "Laptop vs Escritorio"),
    ("Redes_Sociales",       "Redes Sociales"),
    ("Telefono_vs_TV",       "Teléfono vs TV"),
    ("Favor_IA",             "Opinión sobre IA"),
    ("Favor_IA_Educacion",   "IA en Educación"),
    ("Clases_Virtuales",     "Modalidad de Clases"),
]