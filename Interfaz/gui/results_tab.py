# gui/results_tab.py
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import csv
import os
from utils.styles import COLORS

class ResultsTab:
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        self.create_tab()

    def create_tab(self):
        self.frame = ttk.Frame(self.parent)
        self.frame.bind("<Visibility>", self.on_tab_visible)


        # Panel de selección de archivo CSV
        file_panel = tk.Frame(self.frame, bg="#ECF0F1")
        file_panel.pack(fill="x", padx=20, pady=10)

        tk.Label(file_panel, text="Proyectos:", bg="#ECF0F1").pack(side="left", padx=5)
        # Frame para Listbox con Scrollbar
        listbox_frame = tk.Frame(file_panel)
        listbox_frame.pack(side="left", fill="both", expand=True, padx=10)

        scrollbar = tk.Scrollbar(listbox_frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        self.csv_selector = tk.Listbox(listbox_frame, height=5, exportselection=False, yscrollcommand=scrollbar.set)
        self.csv_selector.pack(side="left", fill="both", expand=True)

        scrollbar.config(command=self.csv_selector.yview)

        self.csv_selector.bind("<<ListboxSelect>>", self.on_csv_selected)

        tk.Button(file_panel, text="🔄 Recargar", command=self.load_result_files,
                  bg="#2980B9", fg="white", bd=0, pady=5, activebackground="#2471A3", cursor="hand2").pack(side="left", padx=10)

        # Panel de filtros
        filter_panel = tk.Frame(self.frame, bg="#ECF0F1")
        filter_panel.pack(fill="x", padx=20, pady=10)

        tk.Label(filter_panel, text="Categoría:", bg="#ECF0F1").pack(side="left", padx=5)
        self.categoria_filter = ttk.Combobox(filter_panel, values=["Todos"], width=15)
        self.categoria_filter.set("Todos")
        self.categoria_filter.pack(side="left", padx=5)

        tk.Button(filter_panel, text="Aplicar Filtros", command=self.apply_filters,
                  bg="#3498DB", fg="white", bd=0, pady=5, activebackground="#2980B9", cursor="hand2").pack(side="left", padx=10)

        # Tabla de resultados
        table_frame = tk.Frame(self.frame)
        table_frame.pack(expand=True, fill="both", padx=20, pady=20)

        columns = ("Posición", "Dorsal", "Tiempo", "Nombre", "Categoria")
        self.results_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)

        for col in columns:
            self.results_tree.heading(col, text=col)
            self.results_tree.column(col, width=100)

        v_scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.results_tree.yview)
        
        self.results_tree.configure(yscrollcommand=v_scrollbar.set)

        self.results_tree.pack(side="left", expand=True, fill="both")
        v_scrollbar.pack(side="right", fill="y")
        

        # Panel de acciones
        action_panel = tk.Frame(self.frame)
        action_panel.pack(fill="x", padx=20, pady=20)

        tk.Button(action_panel, text="💾 Exportar CSV", command=self.export_csv,
                  bg="#27AE60", fg="white", font=("Arial", 10, "bold"),
                  bd=0, pady=10, activebackground="#229954", cursor="hand2").pack(side="left", padx=10)


        self.resultados_data = []
        self.resultados_archivos = []
        self.load_result_files()

    def on_tab_visible(self, event):
        # Solo recarga si el tab se vuelve visible
        if event.widget == self.frame:
            self.load_result_files()

    def load_result_files(self):
        resultados_folder = "./resultados"
        self.csv_selector.delete(0, "end")
        self.resultados_archivos.clear()

        if not os.path.exists(resultados_folder):
            os.makedirs(resultados_folder)

        archivos = [f for f in os.listdir(resultados_folder) if f.endswith(".csv")]
        archivos.sort(key=lambda f: os.path.getmtime(os.path.join(resultados_folder, f)), reverse=True)

        for archivo in archivos:
            nombre = os.path.splitext(archivo)[0]
            self.csv_selector.insert("end", nombre)
            self.resultados_archivos.append(os.path.join(resultados_folder, archivo))

        # Mostrar el más reciente automáticamente
        if self.resultados_archivos:
            self.csv_selector.select_set(0)
            self.on_csv_selected(None)


    def on_csv_selected(self, event):
        selected_idx = self.csv_selector.curselection()
        if not selected_idx:
            return

        selected_path = self.resultados_archivos[selected_idx[0]]
        self.resultados_data.clear()

        try:
            with open(selected_path, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.resultados_data.append(row)

            categorias = set(r.get("Categoria", "") for r in self.resultados_data if r.get("Categoria"))
            self.categoria_filter["values"] = ["Todos"] + sorted(categorias)
            self.categoria_filter.set("Todos")

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo leer el archivo:\n{str(e)}")
            return

        self.update_results_table()

    def update_results_table(self):
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)

        for idx, resultado in enumerate(self.resultados_data, start=1):
            values = (
                idx,
                resultado.get("Dorsal", ""),
                resultado.get("Tiempo", ""),
                resultado.get("Nombre", ""),
                resultado.get("Categoria", "")
            )
            self.results_tree.insert("", "end", values=values)

    def apply_filters(self):
        categoria = self.categoria_filter.get()

        for item in self.results_tree.get_children():
            self.results_tree.delete(item)

        for idx, resultado in enumerate(self.resultados_data, start=1):
            if categoria != "Todos" and resultado.get("Categoria") != categoria:
                continue
            values = (
                idx,
                resultado.get("Dorsal", ""),
                resultado.get("Tiempo", ""),
                resultado.get("Nombre", ""),
                resultado.get("Categoria", "")
            )
            self.results_tree.insert("", "end", values=values)

    def export_csv(self):
        if not self.resultados_data:
            messagebox.showwarning("Advertencia", "No hay datos para exportar")
            return

        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("Todos los archivos", "*.*")],
            title="Guardar resultados como CSV"
        )

        if filename:
            try:
                with open(filename, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.DictWriter(file, fieldnames=self.resultados_data[0].keys())
                    writer.writeheader()
                    writer.writerows(self.resultados_data)
                messagebox.showinfo("Éxito", f"Resultados exportados a:\n{filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Error al exportar: {str(e)}")

    def on_data_changed(self, data):
        self.resultados_data = data
        self.update_results_table()
