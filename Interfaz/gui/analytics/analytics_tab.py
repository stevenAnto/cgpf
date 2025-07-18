# tabs/statistics/statistics_tab.py
import os
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import MaxNLocator

from gui.analytics.analytics_utils import (
    listar_proyectos_csv, cargar_estadisticas_csv, generar_cdf
)

class StatisticsTab:
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        self.create_tab()

    def create_tab(self):
        self.frame = tk.Frame(self.parent)
        self.frame.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(self.frame, borderwidth=0)
        v_scroll = tk.Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=v_scroll.set)
        v_scroll.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.scrollable_frame = ttk.Frame(self.canvas)
        self.canvas_frame_id = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig(self.canvas_frame_id, width=e.width))

        header = tk.Frame(self.scrollable_frame, bg="#2C3E50", height=45)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="📈 Estadísticas Generales", bg="#2C3E50", fg="white",
                 font=("Arial", 14, "bold")).pack(pady=4)

        selector_frame = tk.Frame(self.scrollable_frame)
        selector_frame.pack(fill="x", padx=8, pady=6)
        tk.Label(selector_frame, text="Proyecto:", font=("Arial", 11, "bold")).pack(side="left")
        self.project_dropdown = ttk.Combobox(selector_frame, state="readonly", width=30)
        self.project_dropdown.pack(side="left", padx=8)
        self.project_dropdown.bind("<<ComboboxSelected>>", lambda e: self.update_stats())

        self.stats_frame = tk.Frame(self.scrollable_frame)
        self.stats_frame.pack(fill="both", expand=True, padx=8, pady=6)

        self.refresh_projects()

    def refresh_projects(self):
        names = listar_proyectos_csv()
        self.project_dropdown["values"] = names
        if names:
            self.project_dropdown.current(0)
            self.update_stats()

    def update_stats(self):
        for w in self.stats_frame.winfo_children():
            w.destroy()

        fname = self.project_dropdown.get()
        path = os.path.join("resultados", fname)

        try:
            df, total, prom, mins, maxs, cats = cargar_estadisticas_csv(path)

            # Panel superior
            top = tk.Frame(self.stats_frame)
            top.pack(fill="x", pady=6)

            gf = tk.LabelFrame(top, text="Totales", font=("Arial",11,"bold"), padx=4, pady=4)
            gf.pack(side="left", expand=True, fill="both", padx=2)
            tk.Label(gf, text=f"Total: {total}").pack(anchor="w", pady=1)
            tk.Label(gf, text=f"Promedio: {prom:.2f}s").pack(anchor="w", pady=1)
            tk.Label(gf, text=f"Mínimo: {mins:.2f}s").pack(anchor="w", pady=1)
            tk.Label(gf, text=f"Máximo: {maxs:.2f}s").pack(anchor="w", pady=1)

            cf = tk.LabelFrame(top, text="Por Categoría", font=("Arial",11,"bold"), padx=4, pady=4)
            cf.pack(side="left", expand=True, fill="both", padx=2)
            for cat, c in cats.items():
                tk.Label(cf, text=f"{cat}: {c}").pack(anchor="w", pady=1)

            # Gráficos
            graphs = tk.Frame(self.stats_frame)
            graphs.pack(fill="both", expand=True, pady=6)

            fig1, ax1 = plt.subplots(figsize=(4,4))
            ax1.pie(cats.values, labels=cats.index, autopct='%1.1f%%', startangle=90)
            ax1.set_title("Participantes por Categoría")
            ax1.axis('equal')
            fig1.tight_layout(pad=0.5)
            canvas1 = FigureCanvasTkAgg(fig1, master=graphs)
            canvas1.get_tk_widget().pack(side="left", expand=True, fill="both", padx=4)
            canvas1.draw()

            times, cdf, xs, ys = generar_cdf(df)
            fig2, ax2 = plt.subplots(figsize=(4,4))
            ax2.step(times, cdf, where='post', label='CDF escalonada', color='#1f77b4')
            ax2.plot(xs, ys, '-', label='CDF curva', color='#ff7f0e')
            ax2.set_title("CDF de Tiempos")
            ax2.set_xlabel("Tiempo (s)")
            ax2.set_ylabel("Proporción Acumulada")
            ax2.legend(fontsize=8)
            ax2.yaxis.set_major_locator(MaxNLocator(integer=True))
            fig2.tight_layout(pad=0.5)

            canvas2 = FigureCanvasTkAgg(fig2, master=graphs)
            canvas2.get_tk_widget().pack(side="left", expand=True, fill="both", padx=4)
            canvas2.draw()

        except Exception as e:
            tk.Label(self.stats_frame, text=f"Error: {e}", fg="red").pack(pady=6)
