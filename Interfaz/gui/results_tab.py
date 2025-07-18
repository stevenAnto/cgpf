# gui/results_tab.py
import os
import csv
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from gui.report.generate_report import ReportGenerator
from tkinter import filedialog

class ResultsTab:
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        self.create_tab()

    def create_tab(self):
        self.frame = ttk.Frame(self.parent)
        self.frame.bind("<Visibility>", self.on_tab_visible)

        # Panel de selección de proyecto (.csv)
        file_panel = tk.Frame(self.frame, bg="#ECF0F1")
        file_panel.pack(fill="x", padx=20, pady=10)

        tk.Label(file_panel, text="Proyectos:", bg="#ECF0F1").pack(side="left", padx=5)
        listbox_frame = tk.Frame(file_panel)
        listbox_frame.pack(side="left", fill="both", expand=True, padx=10)

        scrollbar = tk.Scrollbar(listbox_frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")
        self.csv_selector = tk.Listbox(
            listbox_frame, height=5, exportselection=False,
            yscrollcommand=scrollbar.set
        )
        self.csv_selector.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.csv_selector.yview)
        self.csv_selector.bind("<<ListboxSelect>>", self.on_csv_selected)

        tk.Button(
            file_panel, text="🔄 Recargar", command=self.load_result_files,
            bg="#2980B9", fg="white", bd=0, pady=5,
            activebackground="#2471A3", cursor="hand2"
        ).pack(side="left", padx=10)

        # Panel de filtros
        filter_panel = tk.Frame(self.frame, bg="#ECF0F1")
        filter_panel.pack(fill="x", padx=20, pady=10)

        tk.Label(filter_panel, text="Categoría:", bg="#ECF0F1").pack(side="left", padx=5)
        self.categoria_filter = ttk.Combobox(filter_panel, values=["Todos"], width=15)
        self.categoria_filter.set("Todos")
        self.categoria_filter.pack(side="left", padx=5)

        tk.Button(
            filter_panel, text="Aplicar Filtros", command=self.apply_filters,
            bg="#3498DB", fg="white", bd=0, pady=5,
            activebackground="#2980B9", cursor="hand2"
        ).pack(side="left", padx=10)

        # Tabla de resultados
        table_frame = tk.Frame(self.frame)
        table_frame.pack(expand=True, fill="both", padx=20, pady=20)

        columns = ("Posición", "Dorsal", "Tiempo", "Nombre", "Categoria")
        self.results_tree = ttk.Treeview(
            table_frame, columns=columns, show="headings", height=15
        )
        for col in columns:
            self.results_tree.heading(col, text=col)
            self.results_tree.column(col, width=100)
        v_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.results_tree.yview)
        self.results_tree.configure(yscrollcommand=v_scroll.set)
        self.results_tree.pack(side="left", expand=True, fill="both")
        v_scroll.pack(side="right", fill="y")

        # Panel de acciones con botón centrado
        action_panel = tk.Frame(self.frame)
        action_panel.pack(fill="x", padx=20, pady=20)
        self.report_button = tk.Button(
            action_panel,
            text="📝 Generar Informe",
            command=self.on_generate_report,
            bg="#27AE60", fg="white", font=("Arial", 10, "bold"),
            bd=0, pady=10, activebackground="#229954", cursor="hand2"
        )
        self.report_button.pack(anchor="center")

        # Estado interno
        self.resultados_data = []
        self.resultados_archivos = []
        self.load_result_files()

    def on_tab_visible(self, event):
        if event.widget == self.frame:
            self.load_result_files()

    def load_result_files(self):
        folder = "./resultados"
        self.csv_selector.delete(0, "end")
        self.resultados_archivos.clear()
        if not os.path.exists(folder):
            os.makedirs(folder)
        archivos = [
            f for f in os.listdir(folder)
            if f.lower().endswith(".csv")
        ]
        archivos.sort(
            key=lambda f: os.path.getmtime(os.path.join(folder, f)),
            reverse=True
        )
        for f in archivos:
            nombre = os.path.splitext(f)[0]
            self.csv_selector.insert("end", nombre)
            self.resultados_archivos.append(os.path.join(folder, f))
        if self.resultados_archivos:
            self.csv_selector.select_set(0)
            self.on_csv_selected(None)

    def on_csv_selected(self, event):
        idx = self.csv_selector.curselection()
        if not idx:
            return
        path = self.resultados_archivos[idx[0]]
        self.resultados_data.clear()
        try:
            with open(path, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.resultados_data.append(row)
            cats = sorted({
                r.get("Categoria", "")
                for r in self.resultados_data
                if r.get("Categoria")
            })
            self.categoria_filter["values"] = ["Todos"] + cats
            self.categoria_filter.set("Todos")
            self.update_results_table()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo leer:\n{e}")

    def update_results_table(self):
        for i in self.results_tree.get_children():
            self.results_tree.delete(i)
        for i, r in enumerate(self.resultados_data, start=1):
            self.results_tree.insert(
                "", "end",
                values=(
                    i,
                    r.get("Dorsal",""),
                    r.get("Tiempo",""),
                    r.get("Nombre",""),
                    r.get("Categoria","")
                )
            )

    def apply_filters(self):
        cat = self.categoria_filter.get()
        for i in self.results_tree.get_children():
            self.results_tree.delete(i)
        for idx, r in enumerate(self.resultados_data, start=1):
            if cat != "Todos" and r.get("Categoria") != cat:
                continue
            self.results_tree.insert(
                "", "end",
                values=(
                    idx,
                    r.get("Dorsal",""),
                    r.get("Tiempo",""),
                    r.get("Nombre",""),
                    r.get("Categoria","")
                )
            )

    def on_generate_report(self):
        idx = self.csv_selector.curselection()
        if not idx:
            messagebox.showwarning("Selecciona un proyecto", "Primero elige un proyecto")
            return
        csv_path = self.resultados_archivos[idx[0]]
        # Solicitar carpeta de destino
        dest_folder = filedialog.askdirectory(
            title="Selecciona carpeta de destino"
        )
        if not dest_folder:
            return
        nombre_proyecto = os.path.splitext(os.path.basename(csv_path))[0]
        output_pdf = os.path.join(dest_folder, f"{nombre_proyecto}_informe.pdf")

        try:
            rg = ReportGenerator()
            rg.generate_report(csv_path, output_pdf)
            messagebox.showinfo(
                "Informe generado",
                f"PDF guardado en:\n{output_pdf}"
            )
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el informe:\n{e}")

    def on_data_changed(self, data):
        self.resultados_data = data
        self.update_results_table()
