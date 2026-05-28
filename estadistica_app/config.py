# ================================
# CONFIGURACIÓN VISUAL
# ================================

BG         = "#EEF2F7"
CARD       = "#FFFFFF"
HEADER_BG  = "#0F172A"
HEADER_TXT = "#F8FAFC"

ACCENT1    = "#2563EB"
ACCENT2    = "#1D4ED8"
ACCENT3    = "#3B82F6"
ACCENT4    = "#0EA5E9"
ACCENT5    = "#1E293B"

COLOR_PRIMARY   = "#2563EB"
COLOR_SECONDARY = "#60A5FA"
COLOR_SUCCESS   = "#059669"
COLOR_WARNING   = "#D97706"
COLOR_DANGER    = "#DC2626"

TEXT       = "#111827"
TEXT_LIGHT = "#64748B"
BORDER     = "#CBD5E1"

BTN_EXACTA = "#7C3AED"
BTN_MENOR  = "#2563EB"
BTN_MAYOR  = "#059669"
BTN_RANGO  = "#0EA5E9"

# ================================
# MODOS DEL PROGRAMA
# ================================

MODO_NORMAL = "normal"
MODO_BINOMIAL = "binomial"
OPCION_BINOMIAL = "Encuesta binomial"

# ================================
# COLORES PARA GRÁFICAS
# ================================

COLORES_BARRAS = [
    "#2563EB",
    "#3B82F6",
    "#0EA5E9",
    "#0284C7",
    "#1D4ED8",
    "#059669",
    "#7C3AED",
    "#F59E0B"
]

COLORES_PROB = {
    "menor": BTN_MENOR,
    "mayor": BTN_MAYOR,
    "entre": BTN_RANGO,
    "exacta": BTN_EXACTA
}

# ================================
# COLUMNAS DEL EXCEL
# ================================

RENOMBRAR = {
    "Edad": "Edad",

    "Genero": "Genero",
    "Género": "Genero",

    "¿Prefiere laptop o computadora de escritorio?": "Laptop_vs_Escritorio",

    "¿Utiliza redes sociales diariamente?": "Redes_Sociales",

    "¿Utilizas mas el teléfono o la televisión?": "Telefono_vs_TV",
    "¿Utilizas más el teléfono o la televisión?": "Telefono_vs_TV",

    "¿Está a favor del uso de inteligencia artificial?": "Favor_IA",

    "¿Está a favor del uso de inteligencia artificial en la educación?": "Favor_IA_Educacion",
    "¿Esta a favor del uso de inteligencia artificial en la educacion?": "Favor_IA_Educacion",
    "¿Está a favor del uso de inteligencia artificial en la educacion?": "Favor_IA_Educacion",
    "¿Esta a favor del uso de inteligencia artificial en la educación?": "Favor_IA_Educacion",

    "¿Prefiere clases virtuales o presenciales?": "Clases_Virtuales",
}

COLUMNAS_BARRAS_COLS = [
    "Genero",
    "Laptop_vs_Escritorio",
    "Redes_Sociales",
    "Telefono_vs_TV",
    "Favor_IA",
    "Favor_IA_Educacion",
    "Clases_Virtuales"
]

PREGUNTAS_GRAFICAS = [
    ("Laptop_vs_Escritorio", "Laptop vs Escritorio"),
    ("Redes_Sociales", "Redes Sociales"),
    ("Telefono_vs_TV", "Teléfono vs TV"),
    ("Favor_IA", "Opinión sobre IA"),
    ("Favor_IA_Educacion", "IA en Educación"),
    ("Clases_Virtuales", "Modalidad de Clases"),
]