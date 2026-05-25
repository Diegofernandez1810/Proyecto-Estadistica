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
# PALETA — ULTRA PROFESIONAL MODERNA
# ================================
BG         = "#EEF2F7"       # Fondo elegante gris azulado
CARD       = "#FFFFFF"       # Tarjetas limpias
HEADER_BG  = "#0F172A"       # Azul navy premium
HEADER_TXT = "#F8FAFC"

# Colores principales
ACCENT1    = "#2563EB"       # Azul profesional principal
ACCENT2    = "#1D4ED8"       # Azul intenso elegante
ACCENT3    = "#3B82F6"       # Azul moderno
ACCENT4    = "#0EA5E9"       # Cyan premium
ACCENT5    = "#1E293B"       # Azul oscuro sofisticado

# Colores auxiliares
COLOR_PRIMARY   = "#2563EB"
COLOR_SECONDARY = "#60A5FA"
COLOR_SUCCESS   = "#059669"  # Verde elegante
COLOR_WARNING   = "#D97706"  # Ámbar premium
COLOR_DANGER    = "#DC2626"  # Rojo moderno

# Texto
TEXT       = "#111827"
TEXT_LIGHT = "#64748B"
BORDER     = "#CBD5E1"

# Botones
BTN_EXACTA = "#7C3AED"       # Morado premium
BTN_MENOR  = "#2563EB"       # Azul
BTN_MAYOR  = "#059669"       # Verde
BTN_RANGO  = "#0EA5E9"       # Cyan

# Colores para gráficas
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

COLORES_PROB   = {"menor": BTN_MENOR, "mayor": BTN_MAYOR,
                  "entre": BTN_RANGO,  "exacta": BTN_EXACTA}

rcParams.update({
    "figure.facecolor": "#F8FAFC",
    "axes.facecolor":   "#FFFFFF",
    "axes.spines.top":  False,
    "axes.spines.right": False,
    "axes.spines.left": True,
    "axes.spines.bottom": True,
    "font.family":      "Segoe UI",
    "font.size":        10,
    "axes.titlesize":   11,
    "axes.labelsize":   10,
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
from ctypes import windll

try:
    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

ventana = tk.Tk()
ventana.title("Estadística II — Distribución Normal")
ventana.configure(bg=BG)

# Adaptarse al tamaño de la pantalla
ancho_pantalla  = ventana.winfo_screenwidth()
alto_pantalla   = ventana.winfo_screenheight()
ancho_ventana   = min(720, ancho_pantalla - 40)
alto_ventana    = min(920, alto_pantalla  - 60)
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
# ESTILOS TTK PROFESIONALES
# ================================
style = ttk.Style()
style.theme_use("clam")
style.configure("TCombobox", 
                fieldbackground=CARD, 
                background=CARD,
                foreground=TEXT, 
                bordercolor=BORDER, 
                relief="flat",
                borderwidth=1,
                arrowcolor=ACCENT1)
style.map("TCombobox", fieldbackground=[("readonly", CARD)])

# ================================
# HELPERS PROFESIONALES
# ================================
def make_card(parent, title, icon="📊"):
    """Tarjeta profesional limpia."""
    
    # Contenedor externo
    outer = tk.Frame(parent, bg=BG)
    outer.pack(fill="x", padx=20, pady=8)

    # Tarjeta principal
    inner = tk.Frame(
        outer,
        bg=CARD,
        padx=18,
        pady=14,
        relief="flat",
        bd=1
    )
    inner.pack(fill="x")

    # Header del card
    header = tk.Frame(inner, bg=CARD)
    header.pack(fill="x", pady=(0, 10))

    # Línea decorativa izquierda
    line = tk.Frame(header, bg=ACCENT1, width=5, height=28)
    line.pack(side="left", padx=(0, 12))

    # Título
    tk.Label(
        header,
        text=f"{icon} {title}",
        font=("Segoe UI Variable", 12, "bold"),
        bg=CARD,
        fg=HEADER_BG
    ).pack(side="left")

    # Frame de contenido REAL
    content = tk.Frame(inner, bg=CARD)
    content.pack(fill="x")

    return content

def btn(parent, text, color, command, width=16):
    """Botón profesional con hover effect."""
    btn_widget = tk.Button(parent, text=text, bg=color, fg="white",
                           activebackground=color, activeforeground="white",
                           font=("Segoe UI", 9, "bold"), relief="flat",
                           cursor="hand2", width=width, height=1,
                           command=command, bd=0, padx=8, pady=6)
    
    # Efecto hover
    def on_enter(e): btn_widget.config(bg=color, relief="flat")
    def on_leave(e): btn_widget.config(bg=color, relief="flat")
    
    btn_widget.bind("<Enter>", on_enter)
    btn_widget.bind("<Leave>", on_leave)
    return btn_widget

def entry(parent, width=12):
    """Entry profesional."""
    return tk.Entry(parent, width=width, font=("Segoe UI", 10),
                    relief="solid", bd=1, highlightthickness=0,
                    highlightcolor=ACCENT1, highlightbackground=BORDER)

def _leer_valor(entry):
    """Lee valor de entry con validación."""
    try:    
        valor = float(entry.get())
        return valor
    except: 
        messagebox.showerror("Error", "Ingresa un número válido")
        return None

# ================================
# HEADER PROFESIONAL
# ================================
header = tk.Frame(frame_contenido, bg=HEADER_BG)
header.pack(fill="x")

# Logo / título
tk.Label(header, text="📈", font=("Segoe UI", 24),
         bg=HEADER_BG, fg=HEADER_TXT).pack(pady=(16, 0))

tk.Label(header, text="Distribución Normal",
         font=("Segoe UI", 18, "bold"), bg=HEADER_BG, fg=HEADER_TXT).pack()

tk.Label(header, text="Análisis Estadístico Avanzado",
         font=("Segoe UI Variable", 9), bg=HEADER_BG, fg="#A8CBE5").pack(pady=(2, 12))

# Línea decorativa
tk.Frame(header, bg="#FFFFFF", height=2).pack(fill="x", padx=40)

label_info = tk.Label(frame_contenido, text="⚡ Cargue su archivo Excel para comenzar",
                      font=("Segoe UI Variable", 9), bg=BG, fg=TEXT_LIGHT)
label_info.pack(pady=12)

# ================================
# CARGAR EXCEL
# ================================
def cargar_excel():
    global data
    archivo = filedialog.askopenfilename(
        title="Seleccionar archivo Excel",
        filetypes=[("Archivos Excel", "*.xlsx *.xls")])
    if not archivo: 
        return
    try:
        data = pd.read_excel(archivo)
        data.rename(columns={k: v for k, v in RENOMBRAR.items()
                              if k in data.columns}, inplace=True)
        data.drop(columns=["Marca temporal", "Dirección de correo electrónico"],
                  errors="ignore", inplace=True)
        label_info.config(text=f"✅ {len(data)} registros cargados correctamente", fg=COLOR_SUCCESS)
        actualizar_selector_columnas()
        actualizar_combo_bin()
        messagebox.showinfo("Éxito", f"Archivo cargado exitosamente\n{len(data)} registros encontrados")
    except Exception as e:
        messagebox.showerror("Error", str(e))

card_excel = make_card(frame_contenido, "Gestión de Datos", icon="📁")
btn(card_excel, "📂 Cargar Excel", ACCENT1, cargar_excel, width=22).pack(pady=4)

# ================================
# SELECTOR COLUMNA
# ================================
card_col = make_card(frame_contenido, "Selección de Variable", icon="🎯")
row_col  = tk.Frame(card_col, bg=CARD)
row_col.pack(fill="x", pady=5)

tk.Label(row_col, text="Variable numérica:", font=("Segoe UI", 9),
         bg=CARD, fg=TEXT).pack(side="left")
combo_columnas = ttk.Combobox(row_col, state="readonly", width=28, font=("Segoe UI", 9))
combo_columnas.pack(side="left", padx=10)

def actualizar_selector_columnas():
    if data is not None:
        nums = data.select_dtypes(include=[np.number]).columns.tolist()
        combo_columnas["values"] = nums
        if nums: 
            combo_columnas.current(0)

def seleccionar_columna():
    global columna_activa
    col = combo_columnas.get()
    if col:
        columna_activa = col
        messagebox.showinfo("Variable seleccionada", f"Variable activa: {col}")
    else:
        messagebox.showwarning("Aviso", "Seleccione una columna primero")

btn(row_col, "Activar variable", ACCENT5, seleccionar_columna, width=16).pack(side="left", padx=5)

# ================================
# GRÁFICAS
# ================================
card_graf = make_card(frame_contenido, "Visualización de Datos", icon="📊")

def graficar_demograficas():
    if data is None:
        messagebox.showerror("Error", "Primero cargue un archivo")
        return
    cols = [(c, t) for c, t in [("Edad","hist"),("Genero","barras")] if c in data.columns]
    if not cols:
        messagebox.showerror("Error", "No se encontraron columnas de Edad o Género")
        return
    
    fig, axes = plt.subplots(1, len(cols), figsize=(6*len(cols), 4.5))
    if len(cols) == 1: 
        axes = [axes]
    
    for ax, (col, tipo) in zip(axes, cols):
        if tipo == "hist":
            ax.hist(data[col].dropna(), bins=12, color=COLOR_PRIMARY, 
                   edgecolor="white", alpha=0.8)
            ax.set_ylabel("Frecuencia", fontsize=9)
        else:
            conteo = data[col].value_counts()
            bars = ax.bar(conteo.index.astype(str), conteo.values,
                          color=COLORES_BARRAS[:len(conteo)], edgecolor="white")
            for bar in bars:
                ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.5,
                        str(int(bar.get_height())), ha="center", va="bottom",
                        fontsize=9, fontweight="bold")
            ax.set_ylabel("Cantidad", fontsize=9)
        
        ax.set_title(col, fontweight="bold", fontsize=11)
        ax.set_xlabel(col, fontsize=9)
        ax.grid(True, alpha=0.15, linestyle='--', color="#94A3B8")
    
    fig.suptitle("Análisis Demográfico", fontsize=13, fontweight="bold", y=1.02)
    plt.tight_layout()
    plt.show()

def graficar_preguntas():
    if data is None:
        messagebox.showerror("Error", "Primero cargue un archivo")
        return
    
    preguntas = [(c, t) for c, t in [
        ("Laptop_vs_Escritorio", "Preferencia: Laptop vs Escritorio"),
        ("Redes_Sociales",       "Uso de Redes Sociales"),
        ("Telefono_vs_TV",       "Preferencia: Teléfono vs TV"),
        ("Favor_IA",             "Opinión sobre IA"),
        ("Clases_Virtuales",     "Modalidad de Clases"),
    ] if c in data.columns]
    
    if not preguntas:
        messagebox.showerror("Error", "No se encontraron columnas de encuesta")
        return
    
    n = len(preguntas)
    cols_fig = 3
    filas_fig = (n + cols_fig - 1) // cols_fig
    fig, axes = plt.subplots(filas_fig, cols_fig, figsize=(6*cols_fig, 5*filas_fig))
    axes = axes.flatten()
    
    for i, (col, titulo) in enumerate(preguntas):
        ax = axes[i]
        conteo = data[col].value_counts()
        bars = ax.bar(conteo.index.astype(str), conteo.values,
                      color=COLORES_BARRAS[:len(conteo)], edgecolor="white")
        for bar in bars:
            ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.5,
                    str(int(bar.get_height())), ha="center", va="bottom",
                    fontsize=9, fontweight="bold")
        ax.set_title(titulo, fontsize=10, fontweight="bold")
        ax.set_ylabel("Cantidad", fontsize=9)
        ax.grid(True, alpha=0.2, linestyle='--', axis='y')
    
    for j in range(i+1, len(axes)):
        axes[j].set_visible(False)
    
    fig.suptitle("Resultados de Encuesta", fontsize=13, fontweight="bold", y=1.02)
    plt.tight_layout()
    plt.show()

row_graf = tk.Frame(card_graf, bg=CARD)
row_graf.pack(pady=8)

btn(row_graf, "👥 Datos Demográficos", ACCENT2, graficar_demograficas, width=22).pack(side="left", padx=8)
btn(row_graf, "📋 Preguntas Encuesta", ACCENT3, graficar_preguntas, width=22).pack(side="left", padx=8)

# ================================
# ESTADÍSTICAS
# ================================
card_stats = make_card(frame_contenido, "Estadísticas Descriptivas", icon="📐")
row_stats  = tk.Frame(card_stats, bg=CARD)
row_stats.pack(fill="x", pady=5)

label_mu_sigma = tk.Label(row_stats,
    text="μ = —    σ = —",
    font=("Segoe UI", 11, "bold"), 
    bg=BG, 
    fg=ACCENT1,
    padx=12, 
    pady=6,
    relief="solid",
    bd=1)
label_mu_sigma.pack(side="left", padx=(0, 12))

def calcular_estadisticas():
    global mu, sigma
    if data is None:
        messagebox.showerror("Error", "Primero cargue un archivo")
        return
    if columna_activa is None:
        messagebox.showerror("Error", "Seleccione una columna primero")
        return
    
    try:
        serie = data[columna_activa].dropna()
        mu    = float(np.mean(serie))
        sigma = float(np.std(serie))
        label_mu_sigma.config(text=f"μ = {mu:.4f}    σ = {sigma:.4f}")
        
        messagebox.showinfo("Estadísticas Calculadas",
            f"Variable: {columna_activa}\n\n"
            f"📊 Media (μ):              {mu:.4f}\n"
            f"📈 Desviación estándar (σ): {sigma:.4f}\n"
            f"📉 Varianza (σ²):          {sigma**2:.4f}\n"
            f"🔢 n (muestras):           {len(serie)}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

btn(row_stats, "📐 Calcular μ y σ", ACCENT3, calcular_estadisticas, width=18).pack(side="left")

# ================================
# GRÁFICA NORMAL (compartida)
# ================================
def graficar_area(a=None, b=None, tipo="menor", mu_=None, sigma_=None, subtitulo=""):
    m = mu_ if mu_ is not None else mu
    s = sigma_ if sigma_ is not None else sigma
    
    if m is None or s is None or s == 0:
        messagebox.showerror("Error", "Primero calcule μ y σ")
        return
    
    x = np.linspace(m - 4*s, m + 4*s, 500)
    y = norm.pdf(x, m, s)
    color = COLORES_PROB.get(tipo, ACCENT4)
    
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(x, y, color=TEXT, linewidth=2)
    ax.axvline(m, color=ACCENT1, linestyle="--", linewidth=1.5, alpha=0.7, label=f"μ = {m:.3f}")
    
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
        mascara = (x >= a-0.5) & (x <= a+0.5)
        etiqueta = f"P(X ≈ {a:.3f}) [±0.5]"
    else:
        return
    
    ax.fill_between(x[y>0], y[y>0], where=mascara[y>0], color=color, alpha=0.4, label=etiqueta)
    
    ax.set_title(f"Distribución Normal", fontsize=12, fontweight="bold", pad=15)
    ax.set_xlabel("Valor", fontsize=10)
    ax.set_ylabel("Densidad de Probabilidad", fontsize=10)
    ax.legend(loc="upper right", framealpha=0.95, fontsize=9)
    ax.grid(True, alpha=0.2, linestyle='--')
    
    plt.tight_layout()
    plt.show()

# ================================
# MÓDULO PROBABILIDAD NORMAL
# ================================
card_prob = make_card(frame_contenido, "Cálculo de Probabilidades", icon="🎲")

row_vals = tk.Frame(card_prob, bg=CARD)
row_vals.pack(fill="x", pady=(0, 10))

tk.Label(row_vals, text="Valor 1:", font=("Segoe UI", 9, "bold"),
         bg=CARD, fg=TEXT).pack(side="left")
entry_valor = entry(row_vals, width=10)
entry_valor.pack(side="left", padx=6)

tk.Label(row_vals, text="Valor 2 (solo rango):", font=("Segoe UI", 9),
         bg=CARD, fg=TEXT).pack(side="left", padx=(15, 0))
entry_valor2 = entry(row_vals, width=10)
entry_valor2.pack(side="left", padx=6)

def _validar_mu_sigma():
    if mu is None or sigma is None:
        messagebox.showerror("Error", "Primero calcule μ y σ en la sección de estadísticas")
        return False
    return True

def prob_exacta():
    if not _validar_mu_sigma(): 
        return
    x = _leer_valor(entry_valor)
    if x is None: 
        return
    
    prob = norm.cdf(x+0.5, mu, sigma) - norm.cdf(x-0.5, mu, sigma)
    messagebox.showinfo("Resultado", 
        f"📊 P(X ≈ {x}) = {prob:.5f}\n\n"
        f"Intervalo: ±0.5\n"
        f"Variable: {columna_activa}")
    graficar_area(a=x, tipo="exacta")

def prob_menor():
    if not _validar_mu_sigma(): 
        return
    x = _leer_valor(entry_valor)
    if x is None: 
        return
    
    prob = norm.cdf(x, mu, sigma)
    messagebox.showinfo("Resultado", 
        f"📊 P(X < {x}) = {prob:.5f}\n\n"
        f"Porcentaje: {prob*100:.2f}%\n"
        f"Variable: {columna_activa}")
    graficar_area(a=x, tipo="menor")

def prob_mayor():
    if not _validar_mu_sigma(): 
        return
    x = _leer_valor(entry_valor)
    if x is None: 
        return
    
    prob = 1 - norm.cdf(x, mu, sigma)
    messagebox.showinfo("Resultado", 
        f"📊 P(X > {x}) = {prob:.5f}\n\n"
        f"Porcentaje: {prob*100:.2f}%\n"
        f"Variable: {columna_activa}")
    graficar_area(a=x, tipo="mayor")

def prob_entre():
    if not _validar_mu_sigma(): 
        return
    a = _leer_valor(entry_valor)
    b = _leer_valor(entry_valor2)
    if a is None or b is None: 
        return
    if a >= b:
        messagebox.showerror("Error", "Valor 1 debe ser menor que Valor 2")
        return
    
    prob = norm.cdf(b, mu, sigma) - norm.cdf(a, mu, sigma)
    messagebox.showinfo("Resultado", 
        f"📊 P({a} < X < {b}) = {prob:.5f}\n\n"
        f"Porcentaje: {prob*100:.2f}%\n"
        f"Variable: {columna_activa}")
    graficar_area(a=a, b=b, tipo="entre")

row_btns = tk.Frame(card_prob, bg=CARD)
row_btns.pack(pady=8)

btn(row_btns, "🎯 Exacta (≈)", BTN_EXACTA, prob_exacta, width=14).grid(row=0, column=0, padx=5, pady=3)
btn(row_btns, "⬅️ Menor (<)", BTN_MENOR, prob_menor, width=14).grid(row=0, column=1, padx=5, pady=3)
btn(row_btns, "➡️ Mayor (>)", BTN_MAYOR, prob_mayor, width=14).grid(row=0, column=2, padx=5, pady=3)
btn(row_btns, "🔄 Rango (entre)", BTN_RANGO, prob_entre, width=14).grid(row=0, column=3, padx=5, pady=3)

# ================================
# MÓDULO BINOMIAL → NORMAL
# ================================
card_bin = make_card(frame_contenido, "Aproximación Binomial → Normal", icon="📈")

row_bin_sel = tk.Frame(card_bin, bg=CARD)
row_bin_sel.pack(fill="x", pady=(0, 8))

tk.Label(row_bin_sel, text="Pregunta:", font=("Segoe UI", 9, "bold"),
         bg=CARD, fg=TEXT).pack(side="left")
combo_bin = ttk.Combobox(row_bin_sel, state="readonly", width=22, font=("Segoe UI", 9))
combo_bin.pack(side="left", padx=8)

tk.Label(row_bin_sel, text="Éxito =", font=("Segoe UI", 9, "bold"),
         bg=CARD, fg=TEXT).pack(side="left", padx=(12, 0))
combo_exito = ttk.Combobox(row_bin_sel, state="readonly", width=14, font=("Segoe UI", 9))
combo_exito.pack(side="left", padx=8)

def actualizar_combo_bin():
    if data is not None:
        cols_bin = [c for c in COLUMNAS_BARRAS_COLS if c in data.columns]
        combo_bin["values"] = cols_bin
        if cols_bin:
            combo_bin.current(0)
            actualizar_opciones_exito()

def actualizar_opciones_exito(event=None):
    col = combo_bin.get()
    if col and data is not None and col in data.columns:
        opciones = data[col].dropna().unique().tolist()
        combo_exito["values"] = [str(o) for o in opciones]
        if opciones:
            combo_exito.current(0)

combo_bin.bind("<<ComboboxSelected>>", actualizar_opciones_exito)

label_bin_stats = tk.Label(card_bin,
    text="n = —    p = —    μ = —    σ = —",
    font=("Segoe UI", 9), 
    bg=BG, 
    fg=TEXT, 
    padx=10, 
    pady=6,
    relief="solid",
    bd=1)
label_bin_stats.pack(fill="x", pady=6)

def calcular_binomial():
    global mu_bin, sigma_bin
    if data is None:
        messagebox.showerror("Error", "Primero cargue un archivo")
        return
    
    col = combo_bin.get()
    exito = combo_exito.get()
    
    if not col or not exito:
        messagebox.showwarning("Aviso", "Seleccione pregunta y valor de éxito")
        return
    
    serie = data[col].dropna().astype(str)
    n = len(serie)
    k = (serie == exito).sum()
    p = k / n if n > 0 else 0
    q = 1 - p
    
    mu_bin = n * p
    sigma_bin = np.sqrt(n * p * q)
    
    label_bin_stats.config(
        text=f"n = {n}    p = {p:.4f}    q = {q:.4f}    μ = {mu_bin:.2f}    σ = {sigma_bin:.2f}")
    
    messagebox.showinfo("Parámetros Binomiales",
        f"Análisis Binomial\n{'='*35}\n\n"
        f"Pregunta: {col}\n"
        f"Éxito: '{exito}'\n"
        f"Frecuencia: {k} de {n} ({k/n*100:.1f}%)\n\n"
        f"n (ensayos) = {n}\n"
        f"p (éxito)   = {p:.5f}\n"
        f"q (fracaso) = {q:.5f}\n\n"
        f"μ (media)   = {mu_bin:.3f}\n"
        f"σ (desv.)   = {sigma_bin:.3f}")

btn(row_bin_sel, "📐 Calcular parámetros", ACCENT2, calcular_binomial, width=18).pack(side="left", padx=8)

def _validar_bin():
    if mu_bin is None or sigma_bin is None:
        messagebox.showerror("Error", "Primero calcule los parámetros binomiales")
        return False
    return True

row_bin_vals = tk.Frame(card_bin, bg=CARD)
row_bin_vals.pack(fill="x", pady=(8, 8))

tk.Label(row_bin_vals, text="Valor 1:", font=("Segoe UI", 9, "bold"),
         bg=CARD, fg=TEXT).pack(side="left")
entry_bin1 = entry(row_bin_vals, width=8)
entry_bin1.pack(side="left", padx=6)

tk.Label(row_bin_vals, text="Valor 2 (rango):", font=("Segoe UI", 9),
         bg=CARD, fg=TEXT).pack(side="left", padx=(12, 0))
entry_bin2 = entry(row_bin_vals, width=8)
entry_bin2.pack(side="left", padx=6)

def bin_exacta():
    if not _validar_bin(): 
        return
    x = _leer_valor(entry_bin1)
    if x is None: 
        return
    
    prob = norm.cdf(x+0.5, mu_bin, sigma_bin) - norm.cdf(x-0.5, mu_bin, sigma_bin)
    messagebox.showinfo("Resultado", 
        f"📊 Probabilidad Binomial (aprox. Normal)\n{'='*35}\n\n"
        f"P(X ≈ {x:.0f}) = {prob:.5f}\n\n"
        f"Interpretación: Probabilidad de que\n"
        f"exactamente {x:.0f} personas respondan\n"
        f"'{combo_exito.get()}'")
    graficar_area(a=x, tipo="exacta", mu_=mu_bin, sigma_=sigma_bin, subtitulo=combo_bin.get())

def bin_menor():
    if not _validar_bin(): 
        return
    x = _leer_valor(entry_bin1)
    if x is None: 
        return
    
    prob = norm.cdf(x, mu_bin, sigma_bin)
    messagebox.showinfo("Resultado", 
        f"📊 Probabilidad Binomial (aprox. Normal)\n{'='*35}\n\n"
        f"P(X < {x:.0f}) = {prob:.5f}\n\n"
        f"Interpretación: Probabilidad de que\n"
        f"menos de {x:.0f} personas respondan\n"
        f"'{combo_exito.get()}'")
    graficar_area(a=x, tipo="menor", mu_=mu_bin, sigma_=sigma_bin, subtitulo=combo_bin.get())

def bin_mayor():
    if not _validar_bin(): 
        return
    x = _leer_valor(entry_bin1)
    if x is None: 
        return
    
    prob = 1 - norm.cdf(x, mu_bin, sigma_bin)
    messagebox.showinfo("Resultado", 
        f"📊 Probabilidad Binomial (aprox. Normal)\n{'='*35}\n\n"
        f"P(X > {x:.0f}) = {prob:.5f}\n\n"
        f"Interpretación: Probabilidad de que\n"
        f"más de {x:.0f} personas respondan\n"
        f"'{combo_exito.get()}'")
    graficar_area(a=x, tipo="mayor", mu_=mu_bin, sigma_=sigma_bin, subtitulo=combo_bin.get())

def bin_entre():
    if not _validar_bin(): 
        return
    a = _leer_valor(entry_bin1)
    b = _leer_valor(entry_bin2)
    if a is None or b is None: 
        return
    if a >= b:
        messagebox.showerror("Error", "Valor 1 debe ser menor que Valor 2")
        return
    
    prob = norm.cdf(b, mu_bin, sigma_bin) - norm.cdf(a, mu_bin, sigma_bin)
    messagebox.showinfo("Resultado", 
        f"📊 Probabilidad Binomial (aprox. Normal)\n{'='*35}\n\n"
        f"P({a:.0f} < X < {b:.0f}) = {prob:.5f}\n\n"
        f"Interpretación: Probabilidad de que\n"
        f"entre {a:.0f} y {b:.0f} personas respondan\n"
        f"'{combo_exito.get()}'")
    graficar_area(a=a, b=b, tipo="entre", mu_=mu_bin, sigma_=sigma_bin, subtitulo=combo_bin.get())

row_bin_btns = tk.Frame(card_bin, bg=CARD)
row_bin_btns.pack(pady=8)

btn(row_bin_btns, "🎯 Exacta (≈)", BTN_EXACTA, bin_exacta, width=14).grid(row=0, column=0, padx=5, pady=3)
btn(row_bin_btns, "⬅️ Menor (<)", BTN_MENOR, bin_menor, width=14).grid(row=0, column=1, padx=5, pady=3)
btn(row_bin_btns, "➡️ Mayor (>)", BTN_MAYOR, bin_mayor, width=14).grid(row=0, column=2, padx=5, pady=3)
btn(row_bin_btns, "🔄 Rango (entre)", BTN_RANGO, bin_entre, width=14).grid(row=0, column=3, padx=5, pady=3)

# ================================
# FOOTER PROFESIONAL
# ================================
footer = tk.Frame(frame_contenido, bg=BG)
footer.pack(fill="x", pady=(20, 10))

tk.Frame(footer, bg=BORDER, height=1).pack(fill="x", padx=40, pady=(0, 12))

tk.Label(footer, text="Estadística II • Distribución Normal • Análisis de Datos",
         font=("Segoe UI", 8), bg=BG, fg=TEXT_LIGHT).pack()
tk.Label(footer, text="© 2024 - Aplicación desarrollada con fines académicos",
         font=("Segoe UI", 7), bg=BG, fg=TEXT_LIGHT).pack(pady=(2, 0))

# ================================
# EJECUTAR
# ================================
ventana.mainloop()