# ================================
# IMPORTACIONES
# ================================
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
from scipy.stats import norm

# ================================
# PALETA — COLORES FRÍOS + VERDE
# ================================
BG         = "#EBF4F8"       # Fondo general — azul muy claro
CARD       = "#FFFFFF"       # Tarjetas blancas
HEADER_BG  = "#0077B6"       # Azul profundo
HEADER_TXT = "#FFFFFF"

ACCENT1    = "#0096C7"       # Azul medio    — Archivo
ACCENT2    = "#1B9E6E"       # Verde         — Gráficas
ACCENT3    = "#00B4D8"       # Cian/Teal     — Estadísticas
ACCENT4    = "#5B6BD5"       # Índigo        — Probabilidad
ACCENT5    = "#2D86AB"       # Teal oscuro   — Columna

TEXT       = "#1A2E35"
TEXT_LIGHT = "#5F7F8E"

BTN_EXACTA = "#5B6BD5"       # Índigo
BTN_MENOR  = "#0096C7"       # Azul
BTN_MAYOR  = "#1B9E6E"       # Verde
BTN_RANGO  = "#00B4D8"       # Cian

COLORES_BARRAS = [ACCENT1, ACCENT2, ACCENT3, ACCENT4, ACCENT5,
                  "#48CAE4", "#52B788"]
COLORES_PROB   = {"menor": BTN_MENOR, "mayor": BTN_MAYOR,
                  "entre": BTN_RANGO,  "exacta": BTN_EXACTA}

rcParams.update({
    "figure.facecolor": "#F0F8FF",
    "axes.facecolor":   "#F0F8FF",
    "axes.spines.top":  False,
    "axes.spines.right":False,
    "font.family":      "sans-serif",
})

# ================================
# VARIABLES GLOBALES
# ================================
data           = None
mu             = None
sigma          = None
columna_activa = None
mu_bin         = None
sigma_bin      = None

RENOMBRAR = {
    "Edad"                                              : "Edad",
    "Genero"                                            : "Genero",
    "¿Prefiere laptop o computadora de escritorio?"     : "Laptop_vs_Escritorio",
    "¿Utiliza redes sociales diariamente?"              : "Redes_Sociales",
    "¿Utilizas mas el teléfono o la televisión?"        : "Telefono_vs_TV",
    "¿Está a favor del uso de inteligencia artificial?" : "Favor_IA",
    "¿Prefiere clases virtuales o presenciales?"        : "Clases_Virtuales",
}
COLUMNAS_BARRAS_COLS = ["Genero","Laptop_vs_Escritorio","Redes_Sociales",
                        "Telefono_vs_TV","Favor_IA","Clases_Virtuales"]

# ================================
# VENTANA PRINCIPAL + SCROLL
# ================================
ventana = tk.Tk()
ventana.title("Estadística II — Distribución Normal")
ventana.configure(bg=BG)

# Adaptarse al tamaño de la pantalla
ancho_pantalla  = ventana.winfo_screenwidth()
alto_pantalla   = ventana.winfo_screenheight()
ancho_ventana   = min(700, ancho_pantalla - 40)
alto_ventana    = min(900, alto_pantalla  - 60)
ventana.geometry(f"{ancho_ventana}x{alto_ventana}")
ventana.resizable(True, True)

# Canvas scrollable
canvas_scroll = tk.Canvas(ventana, bg=BG, highlightthickness=0)
scrollbar     = ttk.Scrollbar(ventana, orient="vertical", command=canvas_scroll.yview)
canvas_scroll.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")
canvas_scroll.pack(side="left", fill="both", expand=True)

# Frame interior que contiene todo el contenido
frame_contenido = tk.Frame(canvas_scroll, bg=BG)
canvas_window   = canvas_scroll.create_window((0, 0), window=frame_contenido, anchor="nw")

def on_frame_configure(event):
    canvas_scroll.configure(scrollregion=canvas_scroll.bbox("all"))

def on_canvas_configure(event):
    canvas_scroll.itemconfig(canvas_window, width=event.width)

frame_contenido.bind("<Configure>", on_frame_configure)
canvas_scroll.bind("<Configure>", on_canvas_configure)

# Scroll con rueda del mouse
def on_mousewheel(event):
    canvas_scroll.yview_scroll(int(-1*(event.delta/120)), "units")
ventana.bind_all("<MouseWheel>", on_mousewheel)

# ================================
# ESTILOS TTK
# ================================
style = ttk.Style()
style.theme_use("clam")
style.configure("TCombobox", fieldbackground=CARD, background=CARD,
                foreground=TEXT, bordercolor="#B2D8E8", relief="flat")

# ================================
# HELPERS
# ================================
def make_card(parent, title, color=ACCENT1):
    """Tarjeta blanca con franja de color arriba."""
    outer = tk.Frame(parent, bg=color)
    outer.pack(fill="x", padx=16, pady=5)
    tk.Frame(outer, bg=color, height=4).pack(fill="x")
    inner = tk.Frame(outer, bg=CARD, padx=14, pady=10)
    inner.pack(fill="x")
    if title:
        tk.Label(inner, text=title, font=("Segoe UI", 10, "bold"),
                 bg=CARD, fg=color).pack(anchor="w", pady=(0, 6))
    return inner

def btn(parent, text, color, command, width=16, height=1):
    return tk.Button(parent, text=text, bg=color, fg="white",
                     activebackground=color, activeforeground="white",
                     font=("Segoe UI", 9, "bold"), relief="flat",
                     cursor="hand2", width=width, height=height,
                     command=command, bd=0, padx=6, pady=4)

def _leer_valor(entry):
    try:    return float(entry.get())
    except: messagebox.showerror("Error", "Ingresa un número válido"); return None

# ================================
# HEADER
# ================================
header = tk.Frame(frame_contenido, bg=HEADER_BG)
header.pack(fill="x")
tk.Label(header, text="  Distribución Normal",
         font=("Segoe UI", 17, "bold"), bg=HEADER_BG, fg=HEADER_TXT).pack(pady=(14, 2))
tk.Label(header, text="Proyecto Estadística II",
         font=("Segoe UI", 9), bg=HEADER_BG, fg="#90CAE4").pack()
tk.Frame(header, bg="#005F94", height=3).pack(fill="x", pady=(10, 0))

label_info = tk.Label(frame_contenido,
    text="⬆  Carga tu archivo Excel para comenzar",
    font=("Segoe UI", 9), bg=BG, fg=TEXT_LIGHT)
label_info.pack(pady=5)

# ================================
# CARGAR EXCEL
# ================================
def cargar_excel():
    global data
    archivo = filedialog.askopenfilename(
        title="Seleccionar archivo Excel",
        filetypes=[("Archivos Excel", "*.xlsx *.xls")])
    if not archivo: return
    try:
        data = pd.read_excel(archivo)
        data.rename(columns={k: v for k, v in RENOMBRAR.items()
                              if k in data.columns}, inplace=True)
        data.drop(columns=["Marca temporal", "Dirección de correo electrónico"],
                  errors="ignore", inplace=True)
        label_info.config(
            text=f"✔  {len(data)} registros cargados correctamente", fg="#1B9E6E")
        actualizar_selector_columnas()
        actualizar_combo_bin()
        messagebox.showinfo("Éxito", f"✔ Archivo cargado\n{len(data)} registros encontrados")
    except Exception as e:
        messagebox.showerror("Error", str(e))

card_excel = make_card(frame_contenido, "📂  Archivo de Datos", color=ACCENT1)
btn(card_excel, "  Cargar Excel  ", ACCENT1, cargar_excel, width=20).pack(pady=2)

# ================================
# SELECTOR COLUMNA
# ================================
card_col = make_card(frame_contenido, "  Columna para Análisis Probabilístico", color=ACCENT5)
row_col  = tk.Frame(card_col, bg=CARD)
row_col.pack(fill="x")
tk.Label(row_col, text="Variable:", font=("Segoe UI", 9),
         bg=CARD, fg=TEXT_LIGHT).pack(side="left")
combo_columnas = ttk.Combobox(row_col, state="readonly", width=26, font=("Segoe UI", 9))
combo_columnas.pack(side="left", padx=5)

def actualizar_selector_columnas():
    if data is not None:
        nums = data.select_dtypes(include=[np.number]).columns.tolist()
        combo_columnas["values"] = nums
        if nums: combo_columnas.current(0)

def seleccionar_columna():
    global columna_activa
    col = combo_columnas.get()
    if col:
        columna_activa = col
        messagebox.showinfo("Columna seleccionada", f"Se usará la variable: {col}")
    else:
        messagebox.showwarning("Aviso", "Selecciona una columna primero")

btn(row_col, "Usar esta columna", ACCENT5, seleccionar_columna, width=16).pack(side="left", padx=8)

# ================================
# GRÁFICAS
# ================================
card_graf = make_card(frame_contenido, "  Gráficas Demográficas y de Encuesta", color=ACCENT2)

def graficar_demograficas():
    if data is None:
        messagebox.showerror("Error", "Primero carga un archivo"); return
    cols = [(c, t) for c, t in [("Edad","hist"),("Genero","barras")] if c in data.columns]
    if not cols:
        messagebox.showerror("Error", "No se encontraron Edad o Género"); return
    fig, axes = plt.subplots(1, len(cols), figsize=(6*len(cols), 4))
    if len(cols) == 1: axes = [axes]
    for ax, (col, tipo) in zip(axes, cols):
        if tipo == "hist":
            ax.hist(data[col].dropna(), bins=10, color=ACCENT1, edgecolor="white")
            ax.set_ylabel("Frecuencia")
        else:
            conteo = data[col].value_counts()
            bars = ax.bar(conteo.index.astype(str), conteo.values,
                          color=COLORES_BARRAS[:len(conteo)], edgecolor="white")
            for bar in bars:
                ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.1,
                        str(int(bar.get_height())), ha="center", va="bottom",
                        fontsize=10, fontweight="bold")
            ax.set_ylabel("Cantidad")
        ax.set_title(f"Distribución: {col}", fontweight="bold")
        ax.set_xlabel(col)
    fig.suptitle(" Datos Demográficos", fontsize=14, fontweight="bold")
    plt.tight_layout(); plt.show()

def graficar_preguntas():
    if data is None:
        messagebox.showerror("Error", "Primero carga un archivo"); return
    preguntas = [(c, t) for c, t in [
        ("Laptop_vs_Escritorio", "¿Laptop o Escritorio?"),
        ("Redes_Sociales",       "¿Usa Redes Sociales?"),
        ("Telefono_vs_TV",       "¿Teléfono o TV?"),
        ("Favor_IA",             "¿A favor de la IA?"),
        ("Clases_Virtuales",     "¿Clases Virtuales?"),
    ] if c in data.columns]
    if not preguntas:
        messagebox.showerror("Error", "No se encontraron columnas de preguntas"); return
    n = len(preguntas); cols_fig = 3
    filas_fig = -(-n // cols_fig)
    fig, axes = plt.subplots(filas_fig, cols_fig, figsize=(6*cols_fig, 4*filas_fig))
    axes = axes.flatten()
    for i, (col, titulo) in enumerate(preguntas):
        ax = axes[i]
        conteo = data[col].value_counts()
        bars = ax.bar(conteo.index.astype(str), conteo.values,
                      color=COLORES_BARRAS[:len(conteo)], edgecolor="white")
        for bar in bars:
            ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.1,
                    str(int(bar.get_height())), ha="center", va="bottom",
                    fontsize=10, fontweight="bold")
        ax.set_title(titulo, fontsize=10, fontweight="bold")
        ax.set_ylabel("Cantidad")
    for j in range(i+1, len(axes)): axes[j].set_visible(False)
    fig.suptitle("  Preguntas de la Encuesta", fontsize=14, fontweight="bold")
    plt.tight_layout(); plt.show()

row_graf = tk.Frame(card_graf, bg=CARD)
row_graf.pack(pady=2)
btn(row_graf, "  Datos Demográficos", ACCENT2,  graficar_demograficas, width=22).pack(side="left", padx=8)
btn(row_graf, "  Preguntas Encuesta",  ACCENT4,  graficar_preguntas,    width=22).pack(side="left", padx=8)

# ================================
# ESTADÍSTICAS
# ================================
card_stats = make_card(frame_contenido, "  Estadísticas Descriptivas", color=ACCENT3)
row_stats  = tk.Frame(card_stats, bg=CARD)
row_stats.pack(fill="x")

label_mu_sigma = tk.Label(row_stats,
    text="  μ = —        σ = —  ",
    font=("Segoe UI", 11, "bold"), bg="#E8F8F5", fg=ACCENT2,
    padx=10, pady=6)
label_mu_sigma.pack(side="left", padx=(0, 12))

def calcular_estadisticas():
    global mu, sigma
    if data is None:
        messagebox.showerror("Error", "Primero carga un archivo"); return
    if columna_activa is None:
        messagebox.showerror("Error", "Selecciona una columna primero"); return
    try:
        serie = data[columna_activa].dropna()
        mu    = float(np.mean(serie))
        sigma = float(np.std(serie))
        label_mu_sigma.config(text=f"  μ = {mu:.4f}        σ = {sigma:.4f}  ")
        messagebox.showinfo("Estadísticas",
            f"Columna: {columna_activa}\n"
            f"Media (μ):          {mu:.4f}\n"
            f"Desv. estándar (σ): {sigma:.4f}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

btn(row_stats, "Calcular  μ  y  σ", ACCENT3, calcular_estadisticas, width=18).pack(side="left")

# ================================
# GRÁFICA NORMAL (compartida)
# ================================
def graficar_area(a=None, b=None, tipo="menor", mu_=None, sigma_=None, subtitulo=""):
    m = mu_    if mu_    is not None else mu
    s = sigma_ if sigma_ is not None else sigma
    if m is None or s is None: return
    x = np.linspace(m - 4*s, m + 4*s, 500)
    y = norm.pdf(x, m, s)
    color = COLORES_PROB.get(tipo, ACCENT4)
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(x, y, color=TEXT, linewidth=2.5)
    ax.axvline(m, color=ACCENT5, linestyle="--", linewidth=1.5, label=f"μ = {m:.2f}")
    if   tipo == "menor":  mascara = x <= a;                etiqueta = f"P(X < {a:.2f})"
    elif tipo == "mayor":  mascara = x >= a;                etiqueta = f"P(X > {a:.2f})"
    elif tipo == "entre":  mascara = (x >= a) & (x <= b);  etiqueta = f"P({a:.2f} < X < {b:.2f})"
    elif tipo == "exacta": mascara = (x>=a-0.5)&(x<=a+0.5); etiqueta = f"P(X ≈ {a:.2f}) [±0.5]"
    ax.fill_between(x, y, where=mascara, color=color, alpha=0.55, label=etiqueta)
    ax.set_title(f"Distribución Normal{' — '+subtitulo if subtitulo else ''}",
                 fontsize=13, fontweight="bold", pad=12)
    ax.set_xlabel("Valor"); ax.set_ylabel("Densidad")
    ax.legend(framealpha=0.9)
    plt.tight_layout(); plt.show()

# ================================
# MÓDULO PROBABILIDAD NORMAL
# ================================
card_prob = make_card(frame_contenido, "  Módulo de Probabilidad — Distribución Normal", color=ACCENT4)
row_vals  = tk.Frame(card_prob, bg=CARD)
row_vals.pack(fill="x", pady=(0, 6))

tk.Label(row_vals, text="Valor 1:", font=("Segoe UI",9),
         bg=CARD, fg=TEXT_LIGHT).pack(side="left")
entry_valor = tk.Entry(row_vals, width=10, font=("Segoe UI",10), relief="solid", bd=1)
entry_valor.pack(side="left", padx=6)
tk.Label(row_vals, text="Valor 2 (solo rango):", font=("Segoe UI",9),
         bg=CARD, fg=TEXT_LIGHT).pack(side="left", padx=(14,0))
entry_valor2 = tk.Entry(row_vals, width=10, font=("Segoe UI",10), relief="solid", bd=1)
entry_valor2.pack(side="left", padx=6)

def _validar_mu_sigma():
    if mu is None or sigma is None:
        messagebox.showerror("Error", "Primero calcula μ y σ"); return False
    return True

def prob_exacta():
    if not _validar_mu_sigma(): return
    x = _leer_valor(entry_valor)
    if x is None: return
    prob = norm.cdf(x+0.5,mu,sigma) - norm.cdf(x-0.5,mu,sigma)
    messagebox.showinfo("Resultado", f"P(X ≈ {x}) ≈ {prob:.4f}\n(intervalo ±0.5)")
    graficar_area(a=x, tipo="exacta")

def prob_menor():
    if not _validar_mu_sigma(): return
    x = _leer_valor(entry_valor)
    if x is None: return
    messagebox.showinfo("Resultado", f"P(X < {x}) = {norm.cdf(x,mu,sigma):.4f}")
    graficar_area(a=x, tipo="menor")

def prob_mayor():
    if not _validar_mu_sigma(): return
    x = _leer_valor(entry_valor)
    if x is None: return
    messagebox.showinfo("Resultado", f"P(X > {x}) = {1-norm.cdf(x,mu,sigma):.4f}")
    graficar_area(a=x, tipo="mayor")

def prob_entre():
    if not _validar_mu_sigma(): return
    a = _leer_valor(entry_valor); b = _leer_valor(entry_valor2)
    if a is None or b is None: return
    if a >= b:
        messagebox.showerror("Error", "Valor 1 debe ser menor que Valor 2"); return
    prob = norm.cdf(b,mu,sigma) - norm.cdf(a,mu,sigma)
    messagebox.showinfo("Resultado", f"P({a} < X < {b}) = {prob:.4f}")
    graficar_area(a=a, b=b, tipo="entre")

row_btns = tk.Frame(card_prob, bg=CARD)
row_btns.pack()
btn(row_btns,"P(X ≈ x)  Exacta",  BTN_EXACTA, prob_exacta, width=17).grid(row=0,column=0,padx=5,pady=2)
btn(row_btns,"P(X < x)  Menor",   BTN_MENOR,  prob_menor,  width=17).grid(row=0,column=1,padx=5,pady=2)
btn(row_btns,"P(X > x)  Mayor",   BTN_MAYOR,  prob_mayor,  width=17).grid(row=0,column=2,padx=5,pady=2)
btn(row_btns,"P(a < X < b) Rango",BTN_RANGO,  prob_entre,  width=17).grid(row=0,column=3,padx=5,pady=2)

# ================================
# MÓDULO BINOMIAL → NORMAL
# ================================
card_bin = make_card(frame_contenido, "  Módulo Binomial → Aproximación Normal", color=ACCENT2)

row_bin_sel = tk.Frame(card_bin, bg=CARD)
row_bin_sel.pack(fill="x", pady=(0, 4))
tk.Label(row_bin_sel, text="Pregunta:", font=("Segoe UI",9),
         bg=CARD, fg=TEXT_LIGHT).pack(side="left")
combo_bin = ttk.Combobox(row_bin_sel, state="readonly", width=20, font=("Segoe UI",9))
combo_bin.pack(side="left", padx=6)
tk.Label(row_bin_sel, text="Éxito =", font=("Segoe UI",9),
         bg=CARD, fg=TEXT_LIGHT).pack(side="left", padx=(10,0))
combo_exito = ttk.Combobox(row_bin_sel, state="readonly", width=12, font=("Segoe UI",9))
combo_exito.pack(side="left", padx=6)

def actualizar_combo_bin():
    if data is not None:
        cols_bin = [c for c in COLUMNAS_BARRAS_COLS if c in data.columns]
        combo_bin["values"] = cols_bin
        if cols_bin:
            combo_bin.current(0); actualizar_opciones_exito()

def actualizar_opciones_exito(event=None):
    col = combo_bin.get()
    if col and data is not None and col in data.columns:
        opciones = data[col].dropna().unique().tolist()
        combo_exito["values"] = [str(o) for o in opciones]
        combo_exito.current(0)

combo_bin.bind("<<ComboboxSelected>>", actualizar_opciones_exito)

label_bin_stats = tk.Label(card_bin,
    text="  n = —   p = —   q = —   μ = n·p = —   σ = √(n·p·q) = —  ",
    font=("Segoe UI", 9, "bold"), bg="#E8F8F5", fg=ACCENT2, padx=8, pady=5)
label_bin_stats.pack(fill="x", pady=4)

def calcular_binomial():
    global mu_bin, sigma_bin
    if data is None:
        messagebox.showerror("Error", "Primero carga un archivo"); return
    col = combo_bin.get(); exito = combo_exito.get()
    if not col or not exito:
        messagebox.showwarning("Aviso", "Selecciona pregunta y valor de éxito"); return
    serie = data[col].dropna().astype(str)
    n = len(serie); k = (serie == exito).sum()
    p = k/n; q = 1-p
    mu_bin = n*p; sigma_bin = np.sqrt(n*p*q)
    label_bin_stats.config(
        text=f"  n={n}   p={p:.4f}   q={q:.4f}   "
             f"μ = n·p = {mu_bin:.2f}   σ = √(n·p·q) = {sigma_bin:.2f}  ")
    messagebox.showinfo("Parámetros Binomial",
        f"Columna: {col}   |   Éxito: '{exito}' ({k} de {n})\n\n"
        f"n  = {n}\np  = {p:.4f}\nq  = {q:.4f}\n"
        f"μ  = n·p        = {mu_bin:.2f}\n"
        f"σ  = √(n·p·q)  = {sigma_bin:.2f}")

btn(row_bin_sel, "Calcular n,p,q,μ,σ", ACCENT2, calcular_binomial, width=18).pack(side="left", padx=8)

def _validar_bin():
    if mu_bin is None or sigma_bin is None:
        messagebox.showerror("Error", "Primero calcula n, p, q, μ y σ"); return False
    return True

row_bin_vals = tk.Frame(card_bin, bg=CARD)
row_bin_vals.pack(fill="x", pady=(4, 6))
tk.Label(row_bin_vals, text="Valor 1:", font=("Segoe UI",9),
         bg=CARD, fg=TEXT_LIGHT).pack(side="left")
entry_bin1 = tk.Entry(row_bin_vals, width=10, font=("Segoe UI",10), relief="solid", bd=1)
entry_bin1.pack(side="left", padx=6)
tk.Label(row_bin_vals, text="Valor 2 (rango):", font=("Segoe UI",9),
         bg=CARD, fg=TEXT_LIGHT).pack(side="left", padx=(14,0))
entry_bin2 = tk.Entry(row_bin_vals, width=10, font=("Segoe UI",10), relief="solid", bd=1)
entry_bin2.pack(side="left", padx=6)

def bin_exacta():
    if not _validar_bin(): return
    x = _leer_valor(entry_bin1)
    if x is None: return
    prob = norm.cdf(x+0.5,mu_bin,sigma_bin) - norm.cdf(x-0.5,mu_bin,sigma_bin)
    messagebox.showinfo("Resultado",
        f"P(X ≈ {x:.0f}) ≈ {prob:.4f}  (corrección ±0.5)\n\n"
        f"Probabilidad de que exactamente {x:.0f} personas\n"
        f"respondan '{combo_exito.get()}'")
    graficar_area(a=x, tipo="exacta", mu_=mu_bin, sigma_=sigma_bin, subtitulo=combo_bin.get())

def bin_menor():
    if not _validar_bin(): return
    x = _leer_valor(entry_bin1)
    if x is None: return
    prob = norm.cdf(x, mu_bin, sigma_bin)
    messagebox.showinfo("Resultado",
        f"P(X < {x:.0f}) = {prob:.4f}\n\n"
        f"Probabilidad de que menos de {x:.0f} personas\n"
        f"respondan '{combo_exito.get()}'")
    graficar_area(a=x, tipo="menor", mu_=mu_bin, sigma_=sigma_bin, subtitulo=combo_bin.get())

def bin_mayor():
    if not _validar_bin(): return
    x = _leer_valor(entry_bin1)
    if x is None: return
    prob = 1 - norm.cdf(x, mu_bin, sigma_bin)
    messagebox.showinfo("Resultado",
        f"P(X > {x:.0f}) = {prob:.4f}\n\n"
        f"Probabilidad de que más de {x:.0f} personas\n"
        f"respondan '{combo_exito.get()}'")
    graficar_area(a=x, tipo="mayor", mu_=mu_bin, sigma_=sigma_bin, subtitulo=combo_bin.get())

def bin_entre():
    if not _validar_bin(): return
    a = _leer_valor(entry_bin1); b = _leer_valor(entry_bin2)
    if a is None or b is None: return
    if a >= b:
        messagebox.showerror("Error", "Valor 1 debe ser menor que Valor 2"); return
    prob = norm.cdf(b,mu_bin,sigma_bin) - norm.cdf(a,mu_bin,sigma_bin)
    messagebox.showinfo("Resultado",
        f"P({a:.0f} < X < {b:.0f}) = {prob:.4f}\n\n"
        f"Probabilidad de que entre {a:.0f} y {b:.0f} personas\n"
        f"respondan '{combo_exito.get()}'")
    graficar_area(a=a, b=b, tipo="entre", mu_=mu_bin, sigma_=sigma_bin, subtitulo=combo_bin.get())

row_bin_btns = tk.Frame(card_bin, bg=CARD)
row_bin_btns.pack()
btn(row_bin_btns,"P(X ≈ x)  Exacta",  BTN_EXACTA, bin_exacta, width=17).grid(row=0,column=0,padx=5,pady=2)
btn(row_bin_btns,"P(X < x)  Menor",   BTN_MENOR,  bin_menor,  width=17).grid(row=0,column=1,padx=5,pady=2)
btn(row_bin_btns,"P(X > x)  Mayor",   BTN_MAYOR,  bin_mayor,  width=17).grid(row=0,column=2,padx=5,pady=2)
btn(row_bin_btns,"P(a < X < b) Rango",BTN_RANGO,  bin_entre,  width=17).grid(row=0,column=3,padx=5,pady=2)

# ================================
# FOOTER
# ================================
tk.Frame(frame_contenido, bg=HEADER_BG, height=3).pack(fill="x", pady=(12,0))
tk.Label(frame_contenido, text="Estadística II  •  Distribución Normal",
         font=("Segoe UI", 8), bg=BG, fg=TEXT_LIGHT).pack(pady=6)

# ================================
# EJECUTAR
# ================================
ventana.mainloop()