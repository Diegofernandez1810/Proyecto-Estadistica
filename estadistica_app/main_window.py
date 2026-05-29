import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from ctypes import windll

import numpy as np

from .state import AppState
from .config import (
    BG,
    CARD,
    HEADER_BG,
    HEADER_TXT,
    ACCENT1,
    ACCENT2,
    ACCENT3,
    ACCENT5,
    COLOR_SUCCESS,
    TEXT,
    TEXT_LIGHT,
    BORDER,
    BTN_EXACTA,
    BTN_MENOR,
    BTN_MAYOR,
    BTN_RANGO,
    MODO_NORMAL,
    MODO_BINOMIAL,
    OPCION_BINOMIAL,
    COLUMNAS_BARRAS_COLS,
)

from .data_service import cargar_datos_excel

from .stats_service import (
    calcular_media_desviacion,
    calcular_prob_exacta,
    calcular_prob_menor,
    calcular_prob_mayor,
    calcular_prob_entre,
    calcular_parametros_binomiales,
)

from .plot_service import (
    graficar_demograficas,
    graficar_preguntas,
    graficar_area,
)

from .ui_helpers import (
    make_card,
    btn,
    entry,
    cambiar_estado_widget,
)


def iniciar_app():
    # ================================
    # DPI WINDOWS
    # ================================
    try:
        windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass

    # ================================
    # ESTADO GENERAL
    # ================================
    state = AppState()

    # ================================
    # VENTANA PRINCIPAL
    # ================================
    ventana = tk.Tk()
    ventana.title("Estadística II — Distribución Normal")
    ventana.configure(bg=BG)

    ancho_pantalla = ventana.winfo_screenwidth()
    alto_pantalla = ventana.winfo_screenheight()

    ancho_ventana = min(720, ancho_pantalla - 40)
    alto_ventana = min(920, alto_pantalla - 60)

    ventana.geometry(f"{ancho_ventana}x{alto_ventana}")
    ventana.resizable(True, True)

    # ================================
    # CANVAS SCROLLABLE
    # ================================
    canvas_scroll = tk.Canvas(ventana, bg=BG, highlightthickness=0)
    scrollbar = ttk.Scrollbar(
        ventana,
        orient="vertical",
        command=canvas_scroll.yview
    )

    canvas_scroll.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    canvas_scroll.pack(side="left", fill="both", expand=True)

    frame_contenido = tk.Frame(canvas_scroll, bg=BG)
    canvas_window = canvas_scroll.create_window(
        (0, 0),
        window=frame_contenido,
        anchor="nw"
    )

    def on_frame_configure(event):
        canvas_scroll.configure(scrollregion=canvas_scroll.bbox("all"))

    def on_canvas_configure(event):
        canvas_scroll.itemconfig(canvas_window, width=event.width)

    frame_contenido.bind("<Configure>", on_frame_configure)
    canvas_scroll.bind("<Configure>", on_canvas_configure)

    def on_mousewheel(event):
        canvas_scroll.yview_scroll(int(-1 * (event.delta / 120)), "units")

    ventana.bind_all("<MouseWheel>", on_mousewheel)

    # ================================
    # ESTILOS TTK
    # ================================
    style = ttk.Style()
    style.theme_use("clam")

    style.configure(
        "TCombobox",
        fieldbackground=CARD,
        background=CARD,
        foreground=TEXT,
        bordercolor=BORDER,
        relief="flat",
        borderwidth=1,
        arrowcolor=ACCENT1
    )

    style.map("TCombobox", fieldbackground=[("readonly", CARD)])

    # ================================
    # FUNCIONES AUXILIARES INTERNAS
    # ================================
    def leer_valor(caja):
        try:
            return float(caja.get())
        except:
            messagebox.showerror("Error", "Ingresa un número válido")
            return None

    def bloquear_modulos():
        cambiar_estado_widget(card_graf, "disabled")
        cambiar_estado_widget(card_stats, "disabled")
        cambiar_estado_widget(card_prob, "disabled")
        cambiar_estado_widget(card_bin, "disabled")

    def aplicar_modo_interfaz(modo):
        state.modo_activo = modo

        if modo == MODO_NORMAL:
            cambiar_estado_widget(card_graf, "normal")
            cambiar_estado_widget(card_stats, "normal")
            cambiar_estado_widget(card_prob, "normal")

            cambiar_estado_widget(card_bin, "disabled")

            messagebox.showinfo(
                "Modo activado",
                "Modo Edad / Variable numérica activado.\n\n"
                "Puedes usar:\n"
                "• Visualización de datos\n"
                "• Estadísticas descriptivas\n"
                "• Cálculo de probabilidades\n\n"
                "La aproximación binomial quedó bloqueada."
            )

        elif modo == MODO_BINOMIAL:
            cambiar_estado_widget(card_graf, "disabled")
            cambiar_estado_widget(card_stats, "disabled")
            cambiar_estado_widget(card_prob, "disabled")

            cambiar_estado_widget(card_bin, "normal")

            messagebox.showinfo(
                "Modo activado",
                "Modo Encuesta binomial activado.\n\n"
                "Puedes usar solamente:\n"
                "• Aproximación Binomial → Normal\n\n"
                "Las secciones de variable numérica quedaron bloqueadas."
            )

    # ================================
    # HEADER
    # ================================
    header = tk.Frame(frame_contenido, bg=HEADER_BG)
    header.pack(fill="x")

    tk.Label(
        header,
        text="📈",
        font=("Segoe UI", 24),
        bg=HEADER_BG,
        fg=HEADER_TXT
    ).pack(pady=(16, 0))

    tk.Label(
        header,
        text="Distribución Normal",
        font=("Segoe UI", 18, "bold"),
        bg=HEADER_BG,
        fg=HEADER_TXT
    ).pack()

    tk.Label(
        header,
        text="Análisis Estadístico Avanzado",
        font=("Segoe UI Variable", 9),
        bg=HEADER_BG,
        fg="#A8CBE5"
    ).pack(pady=(2, 12))

    tk.Frame(
        header,
        bg="#FFFFFF",
        height=2
    ).pack(fill="x", padx=40)

    label_info = tk.Label(
        frame_contenido,
        text="⚡ Cargue su archivo Excel para comenzar",
        font=("Segoe UI Variable", 9),
        bg=BG,
        fg=TEXT_LIGHT
    )
    label_info.pack(pady=12)

    # ================================
    # GESTIÓN DE DATOS
    # ================================
    card_excel = make_card(frame_contenido, "Gestión de Datos", icon="📁")

    def cargar_excel():
        archivo = filedialog.askopenfilename(
            title="Seleccionar archivo Excel",
            filetypes=[("Archivos Excel", "*.xlsx *.xls")]
        )

        if not archivo:
            return

        try:
            state.data = cargar_datos_excel(archivo)

            state.reiniciar_normal()
            state.reiniciar_binomial()
            state.modo_activo = None

            label_info.config(
                text=f"✅ {len(state.data)} registros cargados correctamente",
                fg=COLOR_SUCCESS
            )

            actualizar_selector_columnas()
            actualizar_combo_bin()

            label_mu_sigma.config(text="μ = —    σ = —")
            label_bin_stats.config(text="n = —    p = —    μ = —    σ = —")

            bloquear_modulos()

            messagebox.showinfo(
                "Éxito",
                f"Archivo cargado exitosamente\n{len(state.data)} registros encontrados"
            )

        except Exception as e:
            messagebox.showerror("Error", str(e))

    btn(
        card_excel,
        "📂 Cargar Excel",
        ACCENT1,
        cargar_excel,
        width=22
    ).pack(pady=4)

    # ================================
    # SELECCIÓN DE VARIABLE
    # ================================
    card_col = make_card(frame_contenido, "Selección de Variable", icon="🎯")

    row_col = tk.Frame(card_col, bg=CARD)
    row_col.pack(fill="x", pady=5)

    tk.Label(
        row_col,
        text="Variable:",
        font=("Segoe UI", 9),
        bg=CARD,
        fg=TEXT
    ).pack(side="left")

    combo_columnas = ttk.Combobox(
        row_col,
        state="readonly",
        width=28,
        font=("Segoe UI", 9)
    )
    combo_columnas.pack(side="left", padx=10)

    def actualizar_selector_columnas():
        if state.data is not None:
            nums = state.data.select_dtypes(include=[np.number]).columns.tolist()

            opciones = nums.copy()

            if any(c in state.data.columns for c in COLUMNAS_BARRAS_COLS):
                opciones.append(OPCION_BINOMIAL)

            combo_columnas["values"] = opciones

            if opciones:
                combo_columnas.current(0)

    def seleccionar_columna():
        if state.data is None:
            messagebox.showerror("Error", "Primero cargue un archivo Excel")
            return

        col = combo_columnas.get()

        if not col:
            messagebox.showwarning("Aviso", "Seleccione una variable primero")
            return

        if col == OPCION_BINOMIAL:
            state.columna_activa = None
            state.mu = None
            state.sigma = None

            label_mu_sigma.config(text="μ = —    σ = —")

            aplicar_modo_interfaz(MODO_BINOMIAL)

        else:
            state.columna_activa = col
            state.reiniciar_binomial()

            label_bin_stats.config(text="n = —    p = —    μ = —    σ = —")

            aplicar_modo_interfaz(MODO_NORMAL)

    btn(
        row_col,
        "Activar variable",
        ACCENT5,
        seleccionar_columna,
        width=16
    ).pack(side="left", padx=5)

    # ================================
    # VISUALIZACIÓN DE DATOS
    # ================================
    card_graf = make_card(frame_contenido, "Visualización de Datos", icon="📊")

    def ejecutar_grafica_demografica():
        if state.data is None:
            messagebox.showerror("Error", "Primero cargue un archivo")
            return

        try:
            graficar_demograficas(state.data)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def ejecutar_grafica_preguntas():
        if state.data is None:
            messagebox.showerror("Error", "Primero cargue un archivo")
            return

        try:
            graficar_preguntas(state.data)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    row_graf = tk.Frame(card_graf, bg=CARD)
    row_graf.pack(pady=8)

    btn(
        row_graf,
        "👥 Datos Demográficos",
        ACCENT2,
        ejecutar_grafica_demografica,
        width=22
    ).pack(side="left", padx=8)

    btn(
        row_graf,
        "📋 Preguntas Encuesta",
        ACCENT3,
        ejecutar_grafica_preguntas,
        width=22
    ).pack(side="left", padx=8)

    # ================================
    # ESTADÍSTICAS DESCRIPTIVAS
    # ================================
    card_stats = make_card(frame_contenido, "Estadísticas Descriptivas", icon="📐")

    row_stats = tk.Frame(card_stats, bg=CARD)
    row_stats.pack(fill="x", pady=5)

    label_mu_sigma = tk.Label(
        row_stats,
        text="μ = —    σ = —",
        font=("Segoe UI", 11, "bold"),
        bg=BG,
        fg=ACCENT1,
        padx=12,
        pady=6,
        relief="solid",
        bd=1
    )
    label_mu_sigma.pack(side="left", padx=(0, 12))

    def calcular_estadisticas():
        if state.data is None:
            messagebox.showerror("Error", "Primero cargue un archivo")
            return

        if state.columna_activa is None:
            messagebox.showerror("Error", "Seleccione una columna primero")
            return

        try:
            serie = state.data[state.columna_activa].dropna()

            state.mu, state.sigma, n = calcular_media_desviacion(serie)

            label_mu_sigma.config(
                text=f"μ = {state.mu:.4f}    σ = {state.sigma:.4f}"
            )

            messagebox.showinfo(
                "Estadísticas Calculadas",
                f"Variable: {state.columna_activa}\n\n"
                f"📊 Media (μ):              {state.mu:.4f}\n"
                f"📈 Desviación estándar (σ): {state.sigma:.4f}\n"
                f"📉 Varianza (σ²):          {state.sigma ** 2:.4f}\n"
                f"🔢 n (muestras):           {n}"
            )

        except Exception as e:
            messagebox.showerror("Error", str(e))

    btn(
        row_stats,
        "📐 Calcular μ y σ",
        ACCENT3,
        calcular_estadisticas,
        width=18
    ).pack(side="left")

    # ================================
    # CÁLCULO DE PROBABILIDADES NORMAL
    # ================================
    card_prob = make_card(frame_contenido, "Cálculo de Probabilidades", icon="🎲")

    row_vals = tk.Frame(card_prob, bg=CARD)
    row_vals.pack(fill="x", pady=(0, 10))

    tk.Label(
        row_vals,
        text="Valor 1:",
        font=("Segoe UI", 9, "bold"),
        bg=CARD,
        fg=TEXT
    ).pack(side="left")

    entry_valor = entry(row_vals, width=10)
    entry_valor.pack(side="left", padx=6)

    tk.Label(
        row_vals,
        text="Valor 2 (solo rango):",
        font=("Segoe UI", 9),
        bg=CARD,
        fg=TEXT
    ).pack(side="left", padx=(15, 0))

    entry_valor2 = entry(row_vals, width=10)
    entry_valor2.pack(side="left", padx=6)

    def validar_mu_sigma():
        if state.mu is None or state.sigma is None:
            messagebox.showerror(
                "Error",
                "Primero calcule μ y σ en la sección de estadísticas"
            )
            return False

        if state.sigma == 0:
            messagebox.showerror(
                "Error",
                "La desviación estándar es 0.\nNo se puede graficar la distribución normal."
            )
            return False

        return True

    def prob_exacta():
        if not validar_mu_sigma():
            return

        entry_valor2.delete(0, tk.END)

        x = leer_valor(entry_valor)

        if x is None:
            return

        prob = calcular_prob_exacta(x, state.mu, state.sigma)

        messagebox.showinfo(
            "Resultado",
            f"📊 P(X ≈ {x}) = {prob:.5f}\n\n"
            f"Intervalo utilizado: ±0.5\n"
            f"Nota: en Exacta solo se usa Valor 1.\n"
            f"Variable: {state.columna_activa}"
        )

        graficar_area(
            a=x,
            tipo="exacta",
            mu_=state.mu,
            sigma_=state.sigma
        )

    def prob_menor():
        if not validar_mu_sigma():
            return

        x = leer_valor(entry_valor)

        if x is None:
            return

        prob = calcular_prob_menor(x, state.mu, state.sigma)

        messagebox.showinfo(
            "Resultado",
            f"📊 P(X < {x}) = {prob:.5f}\n\n"
            f"Porcentaje: {prob * 100:.2f}%\n"
            f"Variable: {state.columna_activa}"
        )

        graficar_area(
            a=x,
            tipo="menor",
            mu_=state.mu,
            sigma_=state.sigma
        )

    def prob_mayor():
        if not validar_mu_sigma():
            return

        x = leer_valor(entry_valor)

        if x is None:
            return

        prob = calcular_prob_mayor(x, state.mu, state.sigma)

        messagebox.showinfo(
            "Resultado",
            f"📊 P(X > {x}) = {prob:.5f}\n\n"
            f"Porcentaje: {prob * 100:.2f}%\n"
            f"Variable: {state.columna_activa}"
        )

        graficar_area(
            a=x,
            tipo="mayor",
            mu_=state.mu,
            sigma_=state.sigma
        )

    def prob_entre():
        if not validar_mu_sigma():
            return

        a = leer_valor(entry_valor)
        b = leer_valor(entry_valor2)

        if a is None or b is None:
            return

        if a >= b:
            messagebox.showerror(
                "Error",
                "Valor 1 debe ser menor que Valor 2"
            )
            return

        prob = calcular_prob_entre(a, b, state.mu, state.sigma)

        messagebox.showinfo(
            "Resultado",
            f"📊 P({a} < X < {b}) = {prob:.5f}\n\n"
            f"Porcentaje: {prob * 100:.2f}%\n"
            f"Variable: {state.columna_activa}"
        )

        graficar_area(
            a=a,
            b=b,
            tipo="entre",
            mu_=state.mu,
            sigma_=state.sigma
        )

    row_btns = tk.Frame(card_prob, bg=CARD)
    row_btns.pack(pady=8)

    btn(row_btns, "🎯 Exacta (≈)", BTN_EXACTA, prob_exacta, width=14).grid(row=0, column=0, padx=5, pady=3)
    btn(row_btns, "⬅️ Menor (<)", BTN_MENOR, prob_menor, width=14).grid(row=0, column=1, padx=5, pady=3)
    btn(row_btns, "➡️ Mayor (>)", BTN_MAYOR, prob_mayor, width=14).grid(row=0, column=2, padx=5, pady=3)
    btn(row_btns, "🔄 Rango (entre)", BTN_RANGO, prob_entre, width=14).grid(row=0, column=3, padx=5, pady=3)

    # ================================
    # APROXIMACIÓN BINOMIAL → NORMAL
    # ================================
    card_bin = make_card(frame_contenido, "Aproximación Binomial → Normal", icon="📈")

    row_bin_sel = tk.Frame(card_bin, bg=CARD)
    row_bin_sel.pack(fill="x", pady=(0, 8))

    tk.Label(
        row_bin_sel,
        text="Pregunta:",
        font=("Segoe UI", 9, "bold"),
        bg=CARD,
        fg=TEXT
    ).pack(side="left")

    combo_bin = ttk.Combobox(
        row_bin_sel,
        state="readonly",
        width=22,
        font=("Segoe UI", 9)
    )
    combo_bin.pack(side="left", padx=8)

    tk.Label(
        row_bin_sel,
        text="Éxito =",
        font=("Segoe UI", 9, "bold"),
        bg=CARD,
        fg=TEXT
    ).pack(side="left", padx=(12, 0))

    combo_exito = ttk.Combobox(
        row_bin_sel,
        state="readonly",
        width=14,
        font=("Segoe UI", 9)
    )
    combo_exito.pack(side="left", padx=8)

    def actualizar_combo_bin():
        if state.data is not None:
            cols_bin = [
                c for c in COLUMNAS_BARRAS_COLS
                if c in state.data.columns
            ]

            combo_bin["values"] = cols_bin

            if cols_bin:
                combo_bin.current(0)
                actualizar_opciones_exito()

    def actualizar_opciones_exito(event=None):
        col = combo_bin.get()

        if col and state.data is not None and col in state.data.columns:
            opciones = state.data[col].dropna().unique().tolist()

            combo_exito["values"] = [str(o) for o in opciones]

            if opciones:
                combo_exito.current(0)

    combo_bin.bind("<<ComboboxSelected>>", actualizar_opciones_exito)

    label_bin_stats = tk.Label(
        card_bin,
        text="n = —    p = —    μ = —    σ = —",
        font=("Segoe UI", 9),
        bg=BG,
        fg=TEXT,
        padx=10,
        pady=6,
        relief="solid",
        bd=1
    )
    label_bin_stats.pack(fill="x", pady=6)

    def calcular_binomial():
        if state.data is None:
            messagebox.showerror("Error", "Primero cargue un archivo")
            return

        col = combo_bin.get()
        exito = combo_exito.get()

        if not col or not exito:
            messagebox.showwarning(
                "Aviso",
                "Seleccione pregunta y valor de éxito"
            )
            return

        try:
            n, k, p, q, state.mu_bin, state.sigma_bin = calcular_parametros_binomiales(
                state.data,
                col,
                exito
            )

            label_bin_stats.config(
                text=f"n = {n}    p = {p:.4f}    q = {q:.4f}    μ = {state.mu_bin:.2f}    σ = {state.sigma_bin:.2f}"
            )

            messagebox.showinfo(
                "Parámetros Binomiales",
                f"Análisis Binomial\n{'=' * 35}\n\n"
                f"Pregunta: {col}\n"
                f"Éxito: '{exito}'\n"
                f"Frecuencia: {k} de {n} ({k / n * 100:.1f}%)\n\n"
                f"n (ensayos) = {n}\n"
                f"p (éxito)   = {p:.5f}\n"
                f"q (fracaso) = {q:.5f}\n\n"
                f"μ (media)   = {state.mu_bin:.3f}\n"
                f"σ (desv.)   = {state.sigma_bin:.3f}"
            )

        except Exception as e:
            messagebox.showerror("Error", str(e))

    btn(
        row_bin_sel,
        "📐 Calcular parámetros",
        ACCENT2,
        calcular_binomial,
        width=18
    ).pack(side="left", padx=8)

    def validar_bin():
        if state.mu_bin is None or state.sigma_bin is None:
            messagebox.showerror(
                "Error",
                "Primero calcule los parámetros binomiales"
            )
            return False

        if state.sigma_bin == 0:
            messagebox.showerror(
                "Error",
                "La desviación estándar es 0.\nNo se puede graficar la aproximación normal."
            )
            return False

        return True

    row_bin_vals = tk.Frame(card_bin, bg=CARD)
    row_bin_vals.pack(fill="x", pady=(8, 8))

    tk.Label(
        row_bin_vals,
        text="Valor 1:",
        font=("Segoe UI", 9, "bold"),
        bg=CARD,
        fg=TEXT
    ).pack(side="left")

    entry_bin1 = entry(row_bin_vals, width=8)
    entry_bin1.pack(side="left", padx=6)

    tk.Label(
        row_bin_vals,
        text="Valor 2 (rango):",
        font=("Segoe UI", 9),
        bg=CARD,
        fg=TEXT
    ).pack(side="left", padx=(12, 0))

    entry_bin2 = entry(row_bin_vals, width=8)
    entry_bin2.pack(side="left", padx=6)

    def bin_exacta():
        if not validar_bin():
            return

        entry_bin2.delete(0, tk.END)

        x = leer_valor(entry_bin1)

        if x is None:
            return

        prob = calcular_prob_exacta(x, state.mu_bin, state.sigma_bin)

        messagebox.showinfo(
            "Resultado",
            f"📊 Probabilidad Binomial aproximada con Normal\n{'=' * 35}\n\n"
            f"P(X ≈ {x:.0f}) = {prob:.5f}\n\n"
            f"Nota: en Exacta solo se usa Valor 1.\n\n"
            f"Interpretación:\n"
            f"Probabilidad de que exactamente {x:.0f} personas respondan "
            f"'{combo_exito.get()}'."
        )

        graficar_area(
            a=x,
            tipo="exacta",
            mu_=state.mu_bin,
            sigma_=state.sigma_bin,
            subtitulo=combo_bin.get()
        )

    def bin_menor():
        if not validar_bin():
            return

        x = leer_valor(entry_bin1)

        if x is None:
            return

        prob = calcular_prob_menor(x, state.mu_bin, state.sigma_bin)

        messagebox.showinfo(
            "Resultado",
            f"📊 Probabilidad Binomial aproximada con Normal\n{'=' * 35}\n\n"
            f"P(X < {x:.0f}) = {prob:.5f}\n\n"
            f"Porcentaje: {prob * 100:.2f}%\n\n"
            f"Interpretación:\n"
            f"Probabilidad de que menos de {x:.0f} personas respondan "
            f"'{combo_exito.get()}'."
        )

        graficar_area(
            a=x,
            tipo="menor",
            mu_=state.mu_bin,
            sigma_=state.sigma_bin,
            subtitulo=combo_bin.get()
        )

    def bin_mayor():
        if not validar_bin():
            return

        x = leer_valor(entry_bin1)

        if x is None:
            return

        prob = calcular_prob_mayor(x, state.mu_bin, state.sigma_bin)

        messagebox.showinfo(
            "Resultado",
            f"📊 Probabilidad Binomial aproximada con Normal\n{'=' * 35}\n\n"
            f"P(X > {x:.0f}) = {prob:.5f}\n\n"
            f"Porcentaje: {prob * 100:.2f}%\n\n"
            f"Interpretación:\n"
            f"Probabilidad de que más de {x:.0f} personas respondan "
            f"'{combo_exito.get()}'."
        )

        graficar_area(
            a=x,
            tipo="mayor",
            mu_=state.mu_bin,
            sigma_=state.sigma_bin,
            subtitulo=combo_bin.get()
        )

    def bin_entre():
        if not validar_bin():
            return

        a = leer_valor(entry_bin1)
        b = leer_valor(entry_bin2)

        if a is None or b is None:
            return

        if a >= b:
            messagebox.showerror(
                "Error",
                "Valor 1 debe ser menor que Valor 2"
            )
            return

        prob = calcular_prob_entre(a, b, state.mu_bin, state.sigma_bin)

        messagebox.showinfo(
            "Resultado",
            f"📊 Probabilidad Binomial aproximada con Normal\n{'=' * 35}\n\n"
            f"P({a:.0f} < X < {b:.0f}) = {prob:.5f}\n\n"
            f"Porcentaje: {prob * 100:.2f}%\n\n"
            f"Interpretación:\n"
            f"Probabilidad de que entre {a:.0f} y {b:.0f} personas respondan "
            f"'{combo_exito.get()}'."
        )

        graficar_area(
            a=a,
            b=b,
            tipo="entre",
            mu_=state.mu_bin,
            sigma_=state.sigma_bin,
            subtitulo=combo_bin.get()
        )

    row_bin_btns = tk.Frame(card_bin, bg=CARD)
    row_bin_btns.pack(pady=8)

    btn(row_bin_btns, "🎯 Exacta (≈)", BTN_EXACTA, bin_exacta, width=14).grid(row=0, column=0, padx=5, pady=3)
    btn(row_bin_btns, "⬅️ Menor (<)", BTN_MENOR, bin_menor, width=14).grid(row=0, column=1, padx=5, pady=3)
    btn(row_bin_btns, "➡️ Mayor (>)", BTN_MAYOR, bin_mayor, width=14).grid(row=0, column=2, padx=5, pady=3)
    btn(row_bin_btns, "🔄 Rango (entre)", BTN_RANGO, bin_entre, width=14).grid(row=0, column=3, padx=5, pady=3)

    # ================================
    # FOOTER
    # ================================
    footer = tk.Frame(frame_contenido, bg=BG)
    footer.pack(fill="x", pady=(20, 10))

    tk.Frame(
        footer,
        bg=BORDER,
        height=1
    ).pack(fill="x", padx=40, pady=(0, 12))

    tk.Label(
        footer,
        text="Estadística II • Distribución Normal • Análisis de Datos",
        font=("Segoe UI", 8),
        bg=BG,
        fg=TEXT_LIGHT
    ).pack()

    tk.Label(
        footer,
        text="© 2024 - Aplicación desarrollada con fines académicos",
        font=("Segoe UI", 7),
        bg=BG,
        fg=TEXT_LIGHT
    ).pack(pady=(2, 0))

    # ================================
    # BLOQUEO INICIAL
    # ================================
    bloquear_modulos()

    ventana.mainloop()