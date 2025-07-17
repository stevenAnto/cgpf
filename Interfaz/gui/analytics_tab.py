import os
import tkinter as tk
from tkinter import ttk
import pandas as pd
import numpy as np
from glob import glob
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import MaxNLocator

class StatisticsTab:
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        self.create_tab()

    def create_tab(self):
        # Contenedor principal
        self.frame = tk.Frame(self.parent)
        self.frame.pack(fill="both", expand=True)

        # Canvas con scroll vertical
        self.canvas = tk.Canvas(self.frame, borderwidth=0)
        v_scroll = tk.Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=v_scroll.set)
        v_scroll.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        # Frame interno desplazable y autoajuste de ancho
        self.scrollable_frame = ttk.Frame(self.canvas)
        self.canvas_frame_id = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.itemconfig(self.canvas_frame_id, width=e.width)
        )

        # Encabezado
        header = tk.Frame(self.scrollable_frame, bg="#2C3E50", height=45)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="📈 Estadísticas Generales", bg="#2C3E50", fg="white",
                 font=("Arial", 14, "bold")).pack(pady=4)

        # Selector de proyecto
        selector_frame = tk.Frame(self.scrollable_frame)
        selector_frame.pack(fill="x", padx=8, pady=6)
        tk.Label(selector_frame, text="Proyecto:", font=("Arial", 11, "bold")).pack(side="left")
        self.project_dropdown = ttk.Combobox(selector_frame, state="readonly", width=30)
        self.project_dropdown.pack(side="left", padx=8)
        self.project_dropdown.bind("<<ComboboxSelected>>", lambda e: self.update_stats())

        # Frame para estadísticas y gráficos
        self.stats_frame = tk.Frame(self.scrollable_frame)
        self.stats_frame.pack(fill="both", expand=True, padx=8, pady=6)

        self.refresh_projects()

    def refresh_projects(self):
        files = glob(os.path.join("resultados", "*.csv"))
        files.sort(key=os.path.getmtime, reverse=True)
        names = [os.path.basename(f) for f in files]
        self.project_dropdown["values"] = names
        if names:
            self.project_dropdown.current(0)
            self.update_stats()

    def convertir_a_segundos(self, tiempo_str):
        """Convierte 'horas-min-seg-ms' (omisiones desde la izquierda)."""
        partes = tiempo_str.strip().split("-")
        try:
            nums = [int(p) for p in partes][::-1]  # invertir para ms, s, m, h
            ms = nums[0] if len(nums) > 0 else 0
            s  = nums[1] if len(nums) > 1 else 0
            m  = nums[2] if len(nums) > 2 else 0
            h  = nums[3] if len(nums) > 3 else 0
            return h*3600 + m*60 + s + ms/1000
        except:
            return 0

    def update_stats(self):
        # Limpiar contenido previo
        for w in self.stats_frame.winfo_children():
            w.destroy()

        fname = self.project_dropdown.get()
        path = os.path.join("resultados", fname)
        try:
            df = pd.read_csv(path)
            df.columns = [c.strip() for c in df.columns]
            df['Tiempo_s'] = df['Tiempo'].astype(str).apply(self.convertir_a_segundos)

            total = len(df)
            prom  = df['Tiempo_s'].mean()
            mins  = df['Tiempo_s'].min()
            maxs  = df['Tiempo_s'].max()
            cats  = df['Categoria'].value_counts().sort_index()

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

            # Pastel para categoría
            fig1, ax1 = plt.subplots(figsize=(4,4))
            ax1.pie(cats.values, labels=cats.index, autopct='%1.1f%%', startangle=90)
            ax1.set_title("Participantes por Categoría")
            ax1.axis('equal')
            fig1.tight_layout(pad=0.5)
            canvas1 = FigureCanvasTkAgg(fig1, master=graphs)
            canvas1.get_tk_widget().pack(side="left", expand=True, fill="both", padx=4)
            canvas1.draw()

            # CDF con escalera y curva suavizada
            times = np.sort(df['Tiempo_s'])
            cdf   = np.arange(1, len(times)+1) / len(times)

            fig2, ax2 = plt.subplots(figsize=(4,4))
            # escalera:
            ax2.step(times, cdf, where='post', label='CDF escalonada', color='#1f77b4')
            # Curva suave mediante polinomio
            xs = np.linspace(times.min(), times.max(), 300)
            # Ajuste polinómico de grado 3
            coefs = np.polyfit(times, cdf, deg=3)
            poly  = np.poly1d(coefs)
            ys    = np.clip(poly(xs), 0, 1)  # asegurar que quede en [0,1]
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
