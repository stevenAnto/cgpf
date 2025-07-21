from tkinter import ttk, filedialog, messagebox
import tkinter as tk
import os
from utils.styles import BUTTON_STYLES
from gui.report.generate_report import ReportGenerator
from gui.results.results_utils import (
    obtener_csvs_ordenados,
    leer_datos_csv,
    filtrar_por_categoria
)


class ResultsTab:
    def __init__(self, parent, controller):
        self.controller = controller
        self.resultados_data = []
        self.resultados_paths = []

        self.frame = ttk.Frame(parent)
        self.frame.bind("<Visibility>", self.on_tab_visible)

        self.setup_layout()
        self.load_csv_files()

    def setup_layout(self):
        self.setup_file_panel()
        self.setup_filter_panel()
        self.setup_table()
        self.setup_action_panel()

    def setup_file_panel(self):
        panel = ttk.Frame(self.frame)
        panel.pack(fill="x", padx=20, pady=10)

        ttk.Label(panel, text="Proyectos:").pack(side="left", padx=5)

        self.listbox = tk.Listbox(panel, height=5, exportselection=False)
        self.listbox.pack(side="left", fill="x", expand=True, padx=(10, 0))
        self.listbox.bind("<<ListboxSelect>>", self.on_csv_selected)

        scrollbar = ttk.Scrollbar(panel, orient="vertical", command=self.listbox.yview)
        scrollbar.pack(side="left", fill="y")
        self.listbox.config(yscrollcommand=scrollbar.set)

        ttk.Button(panel, text="🔄 Recargar", command=self.load_csv_files).pack(side="left", padx=10)

    def setup_filter_panel(self):
        panel = ttk.Frame(self.frame)
        panel.pack(fill="x", padx=20, pady=10)

        ttk.Label(panel, text="Categoría:").pack(side="left", padx=5)
        self.categoria_filter = ttk.Combobox(panel, values=["Todos"], width=15, state="readonly")
        self.categoria_filter.set("Todos")
        self.categoria_filter.pack(side="left", padx=5)

        ttk.Button(panel, text="Aplicar Filtros", command=self.apply_filters).pack(side="left", padx=10)

    def setup_table(self):
        frame = ttk.Frame(self.frame)
        frame.pack(expand=True, fill="both", padx=20, pady=10)

        columns = ("Posición", "Dorsal", "Tiempo", "Nombre", "Categoria")
        self.tree = ttk.Treeview(frame, columns=columns, show="headings", height=15)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")

        self.tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

    def setup_action_panel(self):
        panel = ttk.Frame(self.frame)
        panel.pack(fill="x", padx=20, pady=20)
        tk.Button(
            panel,
            text="📝 Generar Informe",
            command=self.on_generate_report,
            **BUTTON_STYLES['success']
        ).pack(anchor="center")

    def on_tab_visible(self, event):
        if event.widget == self.frame:
            self.load_csv_files()

    def load_csv_files(self):
        self.listbox.delete(0, "end")
        self.resultados_paths.clear()

        archivos = obtener_csvs_ordenados()
        for nombre, path in archivos:
            self.listbox.insert("end", nombre)
            self.resultados_paths.append(path)

        if archivos:
            self.listbox.select_set(0)
            self.on_csv_selected(None)

    def on_csv_selected(self, event):
        idx = self.listbox.curselection()
        if not idx:
            return
        path = self.resultados_paths[idx[0]]
        try:
            self.resultados_data, categorias = leer_datos_csv(path)
            self.categoria_filter["values"] = ["Todos"] + categorias
            self.categoria_filter.set("Todos")
            self.update_table(self.resultados_data)
        except Exception as e:
            messagebox.showerror("Error al leer CSV", str(e))

    def apply_filters(self):
        cat = self.categoria_filter.get()
        filtrados = filtrar_por_categoria(self.resultados_data, cat)
        self.update_table(filtrados)

    def update_table(self, data):
        self.tree.delete(*self.tree.get_children())
        for i, r in enumerate(data, start=1):
            self.tree.insert("", "end", values=(
                i,
                r.get("Dorsal", ""),
                r.get("Tiempo", ""),
                r.get("Nombre", ""),
                r.get("Categoria", "")
            ))

    def on_generate_report(self):
        idx = self.listbox.curselection()
        if not idx:
            messagebox.showwarning("Sin proyecto seleccionado", "Selecciona un proyecto primero.")
            return

        csv_path = self.resultados_paths[idx[0]]
        carpeta = filedialog.askdirectory(title="Selecciona la carpeta de destino")
        if not carpeta:
            return

        nombre = os.path.splitext(os.path.basename(csv_path))[0]
        output = os.path.join(carpeta, f"{nombre}_informe.pdf")

        try:
            ReportGenerator().generate_report(csv_path, output)
            messagebox.showinfo("Informe generado", f"Guardado en:\n{output}")
        except Exception as e:
            messagebox.showerror("Error al generar informe", str(e))
