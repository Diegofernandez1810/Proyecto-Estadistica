import tkinter as tk
from tkinter import ttk

from .config import BG, CARD, HEADER_BG, ACCENT1, BORDER


# ============================================================
# FUNCIÓN: make_card
# ------------------------------------------------------------
# Crea una "tarjeta" visual que agrupa una sección de la UI.
# Cada tarjeta tiene:
#   - Un borde izquierdo de color (línea vertical de acento)
#   - Un título con ícono
#   - Un frame interior (content) donde se agregan los widgets
#
# Parámetros:
#   parent  → widget padre donde se coloca la tarjeta
#   title   → texto del encabezado de la tarjeta
#   icon    → emoji que aparece antes del título
#
# Retorna:
#   content → frame interior listo para agregar widgets
# ============================================================
def make_card(parent, title, icon="📊"):
    # Frame exterior con padding de fondo
    outer = tk.Frame(parent, bg=BG)
    outer.pack(fill="x", padx=20, pady=8)

    # Frame blanco que actúa como "cuerpo" de la tarjeta
    inner = tk.Frame(
        outer,
        bg=CARD,
        padx=18,
        pady=14,
        relief="flat",
        bd=1
    )
    inner.pack(fill="x")

    # Encabezado de la tarjeta
    header = tk.Frame(inner, bg=CARD)
    header.pack(fill="x", pady=(0, 10))

    # Línea vertical de color a la izquierda del título
    line = tk.Frame(header, bg=ACCENT1, width=5, height=28)
    line.pack(side="left", padx=(0, 12))

    # Etiqueta con ícono y texto del título
    tk.Label(
        header,
        text=f"{icon} {title}",
        font=("Segoe UI Variable", 12, "bold"),
        bg=CARD,
        fg=HEADER_BG
    ).pack(side="left")

    # Frame vacío donde se colocarán los controles de la sección
    content = tk.Frame(inner, bg=CARD)
    content.pack(fill="x")

    return content


# ============================================================
# FUNCIÓN: _oscurecer_color
# ------------------------------------------------------------
# Toma un color hexadecimal y lo oscurece un porcentaje dado.
# Se usa para el efecto hover de los botones.
#
# Parámetros:
#   hex_color → color en formato "#RRGGBB"
#   factor    → valor entre 0 y 1 (0.85 = 15% más oscuro)
#
# Retorna:
#   string con el color oscurecido en formato "#RRGGBB"
# ============================================================
def _oscurecer_color(hex_color, factor=0.82):
    hex_color = hex_color.lstrip("#")
    r = int(int(hex_color[0:2], 16) * factor)
    g = int(int(hex_color[2:4], 16) * factor)
    b = int(int(hex_color[4:6], 16) * factor)
    # Clamp a rango 0-255
    r = max(0, min(255, r))
    g = max(0, min(255, g))
    b = max(0, min(255, b))
    return f"#{r:02x}{g:02x}{b:02x}"


# ============================================================
# FUNCIÓN: btn
# ------------------------------------------------------------
# Crea un botón con estilo moderno (sin relieve, color sólido)
# e incluye efecto hover: se oscurece al pasar el mouse encima
# y vuelve al color original al salir.
#
# Parámetros:
#   parent  → widget padre
#   text    → texto que muestra el botón
#   color   → color de fondo en hex (ej. "#2563EB")
#   command → función que ejecuta al hacer clic
#   width   → ancho del botón en caracteres
#
# Retorna:
#   btn_widget → el widget Button configurado
# ============================================================
def btn(parent, text, color, command, width=16):
    # Color más oscuro para el estado hover
    color_hover = _oscurecer_color(color)

    btn_widget = tk.Button(
        parent,
        text=text,
        bg=color,
        fg="white",
        activebackground=color_hover,
        activeforeground="white",
        font=("Segoe UI", 9, "bold"),
        relief="flat",
        cursor="hand2",
        width=width,
        height=1,
        command=command,
        bd=0,
        padx=8,
        pady=6
    )

    # Oscurece el botón cuando el mouse entra
    def on_enter(e):
        if btn_widget["state"] != "disabled":
            btn_widget.config(bg=color_hover)

    # Restaura el color original cuando el mouse sale
    def on_leave(e):
        if btn_widget["state"] != "disabled":
            btn_widget.config(bg=color)

    btn_widget.bind("<Enter>", on_enter)
    btn_widget.bind("<Leave>", on_leave)

    return btn_widget


# ============================================================
# FUNCIÓN: entry
# ------------------------------------------------------------
# Crea un campo de texto estilizado, consistente con el
# diseño de la aplicación.
#
# Parámetros:
#   parent → widget padre
#   width  → ancho en caracteres
#
# Retorna:
#   Entry widget configurado
# ============================================================
def entry(parent, width=12):
    return tk.Entry(
        parent,
        width=width,
        font=("Segoe UI", 10),
        relief="solid",
        bd=1,
        highlightthickness=0,
        highlightcolor=ACCENT1,
        highlightbackground=BORDER
    )


# ============================================================
# FUNCIÓN: cambiar_estado_widget
# ------------------------------------------------------------
# Recorre todos los widgets dentro de un contenedor y cambia
# su estado a "normal" o "disabled".
#
# Se usa para bloquear/desbloquear secciones completas de la
# interfaz según el modo activo (Normal vs Binomial).
#
# Parámetros:
#   widget → frame contenedor cuyos hijos serán modificados
#   estado → "normal" para activar, "disabled" para bloquear
# ============================================================
def cambiar_estado_widget(widget, estado):
    for child in widget.winfo_children():
        try:
            # Los Combobox tienen estado especial "readonly"
            if isinstance(child, ttk.Combobox):
                child.config(state="readonly" if estado == "normal" else "disabled")
            else:
                child.config(state=estado)
        except:
            # Algunos widgets no soportan cambio de estado; se ignoran
            pass

        # Llamada recursiva para widgets anidados
        cambiar_estado_widget(child, estado)