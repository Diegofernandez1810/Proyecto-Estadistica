import tkinter as tk
from tkinter import ttk

from .config import BG, CARD, HEADER_BG, ACCENT1, BORDER


def make_card(parent, title, icon="📊"):
    outer = tk.Frame(parent, bg=BG)
    outer.pack(fill="x", padx=20, pady=8)

    inner = tk.Frame(
        outer,
        bg=CARD,
        padx=18,
        pady=14,
        relief="flat",
        bd=1
    )
    inner.pack(fill="x")

    header = tk.Frame(inner, bg=CARD)
    header.pack(fill="x", pady=(0, 10))

    line = tk.Frame(header, bg=ACCENT1, width=5, height=28)
    line.pack(side="left", padx=(0, 12))

    tk.Label(
        header,
        text=f"{icon} {title}",
        font=("Segoe UI Variable", 12, "bold"),
        bg=CARD,
        fg=HEADER_BG
    ).pack(side="left")

    content = tk.Frame(inner, bg=CARD)
    content.pack(fill="x")

    return content


def btn(parent, text, color, command, width=16):
    btn_widget = tk.Button(
        parent,
        text=text,
        bg=color,
        fg="white",
        activebackground=color,
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

    def on_enter(e):
        if btn_widget["state"] != "disabled":
            btn_widget.config(bg=color)

    def on_leave(e):
        if btn_widget["state"] != "disabled":
            btn_widget.config(bg=color)

    btn_widget.bind("<Enter>", on_enter)
    btn_widget.bind("<Leave>", on_leave)

    return btn_widget


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


def cambiar_estado_widget(widget, estado):
    """
    Activa o desactiva todos los widgets dentro de una sección.
    estado puede ser: normal o disabled.
    """
    for child in widget.winfo_children():
        try:
            if isinstance(child, ttk.Combobox):
                child.config(state="readonly" if estado == "normal" else "disabled")
            else:
                child.config(state=estado)
        except:
            pass

        cambiar_estado_widget(child, estado)