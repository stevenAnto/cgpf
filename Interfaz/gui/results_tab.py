# gui/results_tab.py - Basado en funcionalidad existente
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import csv
from utils.styles import COLORS

class ResultsTab:
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        self.create_tab()
    
    def create_tab(self):
        """Crear pestaña de resultados"""
        self.frame = ttk.Frame(self.parent)
        
        # Panel de filtros
        filter_panel = tk.Frame(self.frame, bg="#ECF0F1")
        filter_panel.pack(fill="x", padx=20, pady=20)
        
        tk.Label(filter_panel, text="Género:", bg="#ECF0F1").pack(side="left", padx=5)
        self.gender_filter = ttk.Combobox(filter_panel, 
                                         values=["Todos", "M", "F"], width=10)
        self.gender_filter.set("Todos")
        self.gender_filter.pack(side="left", padx=5)
        
        tk.Button(filter_panel, text="Aplicar Filtros", command=self.apply_filters,
                 bg="#3498DB", fg="white", bd=0, pady=5,
                 activebackground="#2980B9", cursor="hand2").pack(side="left", padx=10)
        
        # Tabla de resultados
        table_frame = tk.Frame(self.frame)
        table_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        columns = ("Posición", "TimeStamp", "Dorsal", "Género")
        self.results_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.results_tree.heading(col, text=col)
            self.results_tree.column(col, width=100)
        
        # Scrollbars para la tabla
        v_scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.results_tree.yview)
        h_scrollbar = ttk.Scrollbar(table_frame, orient="horizontal", command=self.results_tree.xview)
        self.results_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        self.results_tree.pack(side="left", expand=True, fill="both")
        v_scrollbar.pack(side="right", fill="y")
        h_scrollbar.pack(side="bottom", fill="x")
        
        # Panel de acciones
        action_panel = tk.Frame(self.frame)
        action_panel.pack(fill="x", padx=20, pady=20)
        
        tk.Button(action_panel, text="💾 Exportar CSV", command=self.export_csv,
                 bg="#27AE60", fg="white", font=("Arial", 10, "bold"),
                 bd=0, pady=10, activebackground="#229954", cursor="hand2").pack(side="left", padx=10)
        
        tk.Button(action_panel, text="🖨️ Imprimir", command=self.print_results,
                 bg="#9B59B6", fg="white", font=("Arial", 10, "bold"),
                 bd=0, pady=10, activebackground="#8E44AD", cursor="hand2").pack(side="left", padx=10)
        
        # Cargar datos iniciales si existen
        self.update_results_table()
    
    def update_results_table(self):
        """Actualizar tabla de resultados"""
        # Limpiar tabla
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        
        # Obtener datos del estado compartido
        resultados_data = self.controller.get_shared_state('resultados_data') or []
        
        # Agregar datos
        for resultado in resultados_data:
            values = (
                resultado.get("Posición", ""),
                resultado.get("TimeStamp", ""),
                resultado.get("Dorsal", ""),
                resultado.get("Género", "")
            )
            self.results_tree.insert("", "end", values=values)
    
    def apply_filters(self):
        """Aplicar filtros a los resultados"""
        gender = self.gender_filter.get()
        
        # Limpiar tabla
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        
        # Obtener datos del estado compartido
        resultados_data = self.controller.get_shared_state('resultados_data') or []
        
        # Filtrar y mostrar datos
        for resultado in resultados_data:
            show_item = True
            
            if gender != "Todos" and resultado.get("Género") != gender:
                show_item = False
            
            if show_item:
                values = (
                    resultado.get("Posición", ""),
                    resultado.get("TimeStamp", ""),
                    resultado.get("Dorsal", ""),
                    resultado.get("Género", "")
                )
                self.results_tree.insert("", "end", values=values)
    
    def export_csv(self):
        """Exportar resultados a CSV"""
        resultados_data = self.controller.get_shared_state('resultados_data') or []
        
        if not resultados_data:
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
                    if resultados_data:
                        fieldnames = resultados_data[0].keys()
                        writer = csv.DictWriter(file, fieldnames=fieldnames)
                        writer.writeheader()
                        writer.writerows(resultados_data)
                
                messagebox.showinfo("Éxito", f"Resultados exportados a:\n{filename}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Error al exportar: {str(e)}")
    
    def print_results(self):
        """Imprimir resultados (placeholder)"""
        messagebox.showinfo("Función en desarrollo", 
                           "La función de impresión estará disponible en la próxima versión")
    
    def on_data_changed(self, data):
        """Callback cuando cambian los datos"""
        self.update_results_table()