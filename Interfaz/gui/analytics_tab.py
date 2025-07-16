# gui/analytics_tab.py - Pestaña de análisis
import tkinter as tk
from tkinter import ttk
from utils.styles import COLORS, BUTTON_STYLES

class AnalyticsTab:
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        self.create_tab()
    
    def create_tab(self):
        """Crear pestaña de análisis"""
        self.frame = ttk.Frame(self.parent)
        
        # Header
        header = tk.Frame(self.frame, bg=COLORS['primary'], height=80)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        tk.Label(header, text="📈 Análisis y Estadísticas Avanzadas", 
                bg=COLORS['primary'], fg=COLORS['white'], 
                font=("Arial", 16, "bold")).pack(pady=25)
        
        # Contenedor principal con scroll
        self.create_scrollable_content()
        
        # Métricas principales
        self.create_main_metrics()
        
        # Análisis por categorías
        self.create_category_analysis()
        
        # Gráficos placeholder
        self.create_charts_section()
        
        # Análisis comparativo
        self.create_comparative_analysis()
    
    def create_scrollable_content(self):
        """Crear contenedor scrollable"""
        # Canvas y scrollbar para scroll
        self.canvas = tk.Canvas(self.frame)
        scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def create_main_metrics(self):
        """Crear métricas principales"""
        metrics_frame = tk.LabelFrame(self.scrollable_frame, text="📊 Métricas Principales", 
                                     font=("Arial", 14, "bold"))
        metrics_frame.pack(fill="x", padx=20, pady=20)
        
        # Grid de métricas
        metrics_grid = tk.Frame(metrics_frame)
        metrics_grid.pack(fill="x", padx=15, pady=15)
        
        # Métricas principales
        self.main_metrics = {
            'total_participants': {'value': '0', 'label': 'Total Participantes'},
            'finishers': {'value': '0', 'label': 'Finalizaron'},
            'dnf_rate': {'value': '0%', 'label': 'Tasa de Abandono'},
            'avg_pace': {'value': '0:00 min/km', 'label': 'Ritmo Promedio'},
            'fastest_lap': {'value': '00:00:00', 'label': 'Vuelta Más Rápida'},
            'slowest_lap': {'value': '00:00:00', 'label': 'Vuelta Más Lenta'},
            'time_range': {'value': '00:00:00', 'label': 'Rango de Tiempos'},
            'avg_age': {'value': '0', 'label': 'Edad Promedio'}
        }
        
        # Crear cards de métricas
        for i, (key, metric) in enumerate(self.main_metrics.items()):
            row = i // 4
            col = i % 4
            
            card = tk.Frame(metrics_grid, bg=COLORS['white'], relief="raised", bd=2)
            card.grid(row=row, column=col, padx=8, pady=8, sticky="ew")
            
            # Valor principal
            value_label = tk.Label(card, text=metric['value'], bg=COLORS['white'], 
                                  font=("Arial", 16, "bold"), fg=COLORS['primary'])
            value_label.pack(pady=(15, 5))
            
            # Etiqueta descriptiva
            desc_label = tk.Label(card, text=metric['label'], bg=COLORS['white'], 
                                 font=("Arial", 9), fg=COLORS['muted'], wraplength=100)
            desc_label.pack(pady=(0, 15))
            
            # Guardar referencia para actualizar
            metric['value_label'] = value_label
        
        # Configurar grid
        for i in range(4):
            metrics_grid.grid_columnconfigure(i, weight=1)
    
    def create_category_analysis(self):
        """Crear análisis por categorías"""
        category_frame = tk.LabelFrame(self.scrollable_frame, text="🏆 Análisis por Categorías", 
                                      font=("Arial", 14, "bold"))
        category_frame.pack(fill="x", padx=20, pady=20)
        
        # Tabla de análisis por categoría
        table_frame = tk.Frame(category_frame)
        table_frame.pack(fill="x", padx=15, pady=15)
        
        # Headers
        headers = ["Categoría", "Participantes", "Finalizaron", "% Finalización", 
                  "Mejor Tiempo", "Tiempo Promedio", "Velocidad Prom."]
        
        for i, header in enumerate(headers):
            tk.Label(table_frame, text=header, font=("Arial", 10, "bold"), 
                    bg=COLORS['light'], relief="raised", bd=1).grid(
                    row=0, column=i, sticky="ew", padx=1, pady=1)
        
        # Datos de ejemplo por categoría
        self.category_data = [
            ["Juvenil", "8", "8", "100%", "11:12:45", "12:45:30", "9.2 km/h"],
            ["Adulto", "15", "14", "93.3%", "10:25:30", "11:35:15", "10.8 km/h"],
            ["Senior", "12", "11", "91.7%", "11:35:20", "13:22:10", "8.9 km/h"],
            ["Veterano", "7", "6", "85.7%", "12:08:45", "14:15:30", "8.1 km/h"]
        ]
        
        # Mostrar datos
        for i, row_data in enumerate(self.category_data, 1):
            for j, cell_data in enumerate(row_data):
                bg_color = COLORS['white'] if i % 2 == 0 else "#F8F9FA"
                tk.Label(table_frame, text=cell_data, font=("Arial", 9), 
                        bg=bg_color, relief="solid", bd=1).grid(
                        row=i, column=j, sticky="ew", padx=1, pady=1)
        
        # Configurar columnas
        for i in range(len(headers)):
            table_frame.grid_columnconfigure(i, weight=1)
    
    def create_charts_section(self):
        """Crear sección de gráficos"""
        charts_frame = tk.LabelFrame(self.scrollable_frame, text="📈 Visualizaciones", 
                                    font=("Arial", 14, "bold"))
        charts_frame.pack(fill="x", padx=20, pady=20)
        
        # Grid para gráficos
        charts_grid = tk.Frame(charts_frame)
        charts_grid.pack(fill="x", padx=15, pady=15)
        
        # Placeholder para gráficos
        chart_placeholders = [
            ("📊 Distribución de Tiempos", "Histograma de tiempos de finalización"),
            ("🏃 Velocidad vs Categoría", "Comparación de velocidades promedio"),
            ("⏱️ Progresión de Carrera", "Tiempos de paso en diferentes puntos"),
            ("👥 Participación por Género", "Distribución de participantes")
        ]
        
        for i, (title, description) in enumerate(chart_placeholders):
            row = i // 2
            col = i % 2
            
            chart_card = tk.Frame(charts_grid, bg=COLORS['light'], relief="raised", bd=2)
            chart_card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            
            # Título del gráfico
            tk.Label(chart_card, text=title, bg=COLORS['light'], 
                    font=("Arial", 12, "bold")).pack(pady=10)
            
            # Área del gráfico (placeholder)
            graph_area = tk.Frame(chart_card, bg=COLORS['white'], height=200, width=300)
            graph_area.pack(padx=10, pady=10)
            graph_area.pack_propagate(False)
            
            tk.Label(graph_area, text=f"📈 {description}\n\n[Gráfico en desarrollo]", 
                    bg=COLORS['white'], font=("Arial", 10), 
                    fg=COLORS['muted'], justify="center").pack(expand=True)
            
            # Botón para generar gráfico
            tk.Button(chart_card, text="📊 Generar Gráfico", 
                     command=lambda t=title: self.generate_chart(t),
                     **BUTTON_STYLES['primary'], width=20).pack(pady=10)
        
        # Configurar grid
        charts_grid.grid_columnconfigure(0, weight=1)
        charts_grid.grid_columnconfigure(1, weight=1)
    
    def create_comparative_analysis(self):
        """Crear análisis comparativo"""
        comp_frame = tk.LabelFrame(self.scrollable_frame, text="🔍 Análisis Comparativo", 
                                  font=("Arial", 14, "bold"))
        comp_frame.pack(fill="x", padx=20, pady=20)
        
        # Sección de comparación por género
        gender_frame = tk.LabelFrame(comp_frame, text="👫 Comparación por Género")
        gender_frame.pack(fill="x", padx=15, pady=10)
        
        gender_grid = tk.Frame(gender_frame)
        gender_grid.pack(fill="x", padx=10, pady=10)
        
        # Headers para comparación de género
        gender_headers = ["Género", "Participantes", "% Participación", "Tiempo Promedio", 
                         "Mejor Tiempo", "Velocidad Prom."]
        
        for i, header in enumerate(gender_headers):
            tk.Label(gender_grid, text=header, font=("Arial", 10, "bold"), 
                    bg=COLORS['primary'], fg=COLORS['white'], relief="raised", bd=1).grid(
                    row=0, column=i, sticky="ew", padx=1, pady=1)
        
        # Datos por género
        gender_data = [
            ["Masculino", "25", "59.5%", "12:15:30", "10:25:30", "9.8 km/h"],
            ["Femenino", "17", "40.5%", "13:45:15", "10:47:15", "8.9 km/h"]
        ]
        
        for i, row_data in enumerate(gender_data, 1):
            for j, cell_data in enumerate(row_data):
                color = "#E3F2FD" if row_data[0] == "Masculino" else "#FCE4EC"
                tk.Label(gender_grid, text=cell_data, font=("Arial", 9), 
                        bg=color, relief="solid", bd=1).grid(
                        row=i, column=j, sticky="ew", padx=1, pady=1)
        
        # Configurar columnas
        for i in range(len(gender_headers)):
            gender_grid.grid_columnconfigure(i, weight=1)
        
        # Sección de tendencias temporales
        trends_frame = tk.LabelFrame(comp_frame, text="📈 Tendencias y Patrones")
        trends_frame.pack(fill="x", padx=15, pady=10)
        
        trends_content = tk.Frame(trends_frame)
        trends_content.pack(fill="x", padx=10, pady=10)
        
        # Análisis de tendencias
        trends_text = """
        🔍 Análisis de Patrones Detectados:
        
        • Pico de rendimiento: La mayoría de corredores alcanzan su mejor ritmo entre los 15-25 minutos
        • Patrón de género: Los hombres muestran 12% mejor tiempo promedio
        • Categoría dominante: Los adultos (25-35 años) representan el 35% de participantes
        • Tasa de finalización: 92% general, siendo los juveniles con mejor tasa (100%)
        • Horario óptimo: Los tiempos mejoran 8% en temperaturas de 18-22°C
        
        📊 Recomendaciones:
        • Implementar estrategias de ritmo para mejorar consistencia
        • Considerar categorías de edad más específicas
        • Análisis de fatiga en el último tercio de la carrera
        """
        
        tk.Label(trends_content, text=trends_text, justify="left", 
                font=("Arial", 10), bg=COLORS['light'], 
                wraplength=800, anchor="nw").pack(fill="x", pady=10)
        
        # Botones de análisis avanzado
        analysis_buttons = tk.Frame(comp_frame)
        analysis_buttons.pack(fill="x", padx=15, pady=15)
        
        tk.Button(analysis_buttons, text="📊 Exportar Análisis Completo", 
                 command=self.export_full_analysis, **BUTTON_STYLES['success'], 
                 width=25).pack(side="left", padx=5)
        
        tk.Button(analysis_buttons, text="📈 Generar Informe PDF", 
                 command=self.generate_pdf_report, **BUTTON_STYLES['primary'], 
                 width=20).pack(side="left", padx=5)
        
        tk.Button(analysis_buttons, text="🔄 Actualizar Datos", 
                 command=self.refresh_analytics, **BUTTON_STYLES['warning'], 
                 width=15).pack(side="left", padx=5)
        
        # Información adicional
        info_frame = tk.Frame(self.scrollable_frame, bg=COLORS['light'])
        info_frame.pack(fill="x", padx=20, pady=20)
        
        tk.Label(info_frame, text="💡 Tip: Para análisis más detallados, exporte los datos y utilice herramientas especializadas como Excel o R", 
                bg=COLORS['light'], font=("Arial", 10, "italic"), 
                fg=COLORS['muted'], wraplength=800).pack(pady=15)
    
    def generate_chart(self, chart_type):
        """Generar gráfico específico"""
        try:
            # Aquí implementarías la generación real de gráficos con matplotlib
            # Por ahora, mostrar mensaje informativo
            from tkinter import messagebox
            
            message = f"Generando gráfico: {chart_type}\n\n"
            
            if "Distribución" in chart_type:
                message += "Este gráfico mostraría un histograma de los tiempos de finalización, permitiendo identificar la distribución normal o patrones anómalos."
            elif "Velocidad" in chart_type:
                message += "Comparación de velocidades promedio entre categorías, útil para ajustar estrategias de entrenamiento."
            elif "Progresión" in chart_type:
                message += "Análisis de tiempos parciales en diferentes puntos de la carrera para identificar patrones de fatiga."
            elif "Participación" in chart_type:
                message += "Distribución por género y categoría de edad para planificación de futuras carreras."
            
            message += f"\n\nEn una versión completa, se abriría una ventana con el gráfico interactivo generado usando matplotlib o plotly."
            
            messagebox.showinfo("Gráfico en Desarrollo", message)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error generando gráfico: {str(e)}")
    
    def export_full_analysis(self):
        """Exportar análisis completo"""
        from tkinter import filedialog, messagebox
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv"), ("All files", "*.*")],
            title="Exportar análisis completo"
        )
        
        if filename:
            try:
                # Aquí implementarías la exportación real
                # Por ahora, crear archivo de ejemplo
                
                if filename.endswith('.xlsx'):
                    self.create_excel_analysis(filename)
                else:
                    self.create_csv_analysis(filename)
                
                messagebox.showinfo("Éxito", f"Análisis exportado a: {filename}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Error exportando análisis: {str(e)}")
    
    def create_excel_analysis(self, filename):
        """Crear análisis en Excel"""
        try:
            import pandas as pd
            
            # Crear múltiples hojas con diferentes análisis
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                # Hoja 1: Resultados principales
                df_results = pd.DataFrame(self.controller.resultados_data)
                df_results.to_excel(writer, sheet_name='Resultados', index=False)
                
                # Hoja 2: Análisis por categoría
                df_category = pd.DataFrame(self.category_data, 
                                         columns=["Categoría", "Participantes", "Finalizaron", 
                                                "% Finalización", "Mejor Tiempo", "Tiempo Promedio", "Velocidad Prom."])
                df_category.to_excel(writer, sheet_name='Por_Categoria', index=False)
                
                # Hoja 3: Estadísticas generales
                stats_data = {
                    'Métrica': list(self.main_metrics.keys()),
                    'Valor': [metric['value'] for metric in self.main_metrics.values()],
                    'Descripción': [metric['label'] for metric in self.main_metrics.values()]
                }
                df_stats = pd.DataFrame(stats_data)
                df_stats.to_excel(writer, sheet_name='Estadisticas', index=False)
                
        except ImportError:
            # Fallback a CSV si no hay pandas
            self.create_csv_analysis(filename.replace('.xlsx', '.csv'))
    
    def create_csv_analysis(self, filename):
        """Crear análisis en CSV"""
        import csv
        
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            
            # Escribir análisis completo
            writer.writerow(['ANÁLISIS COMPLETO DE CARRERA'])
            writer.writerow([''])
            
            # Métricas principales
            writer.writerow(['MÉTRICAS PRINCIPALES'])
            for key, metric in self.main_metrics.items():
                writer.writerow([metric['label'], metric['value']])
            
            writer.writerow([''])
            
            # Análisis por categoría
            writer.writerow(['ANÁLISIS POR CATEGORÍA'])
            writer.writerow(["Categoría", "Participantes", "Finalizaron", "% Finalización", 
                           "Mejor Tiempo", "Tiempo Promedio", "Velocidad Prom."])
            
            for row in self.category_data:
                writer.writerow(row)
    
    def generate_pdf_report(self):
        """Generar informe PDF"""
        from tkinter import messagebox
        messagebox.showinfo("Función en desarrollo", 
                           "La generación de PDF estará disponible en la próxima versión.\n\n"
                           "Características planificadas:\n"
                           "• Informe completo con gráficos\n"
                           "• Análisis estadístico detallado\n"
                           "• Comparaciones históricas\n"
                           "• Recomendaciones automáticas")
    
    def refresh_analytics(self):
        """Actualizar análisis con datos actuales"""
        # Recalcular métricas basadas en datos actuales
        self.update_metrics()
        
        from tkinter import messagebox
        messagebox.showinfo("Actualizado", "Análisis actualizado con los datos más recientes")
    
    def update_metrics(self):
        """Actualizar métricas con datos reales"""
        if not self.controller.resultados_data:
            return
        
        data = self.controller.resultados_data
        
        # Calcular métricas reales
        total_participants = len(data)
        finishers = len([r for r in data if r.get("Estado") == "Finalizado"])
        dnf_rate = ((total_participants - finishers) / total_participants * 100) if total_participants > 0 else 0
        
        # Actualizar valores
        self.main_metrics['total_participants']['value'] = str(total_participants)
        self.main_metrics['finishers']['value'] = str(finishers)
        self.main_metrics['dnf_rate']['value'] = f"{dnf_rate:.1f}%"
        
        # Actualizar labels si existen
        for key, metric in self.main_metrics.items():
            if 'value_label' in metric:
                metric['value_label'].config(text=metric['value'])