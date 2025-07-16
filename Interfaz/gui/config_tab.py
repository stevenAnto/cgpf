# gui/config_tab.py - Pestaña de configuración
# gui/config_tab.py - Basado en funcionalidad existente
import tkinter as tk
from tkinter import ttk
from utils.styles import COLORS

class ConfigTab:
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        self.create_tab()
        self.setup_default_values()
    
    def create_tab(self):
        """Crear pestaña de configuración"""
        self.frame = ttk.Frame(self.parent)
        
        # Crear scrollable frame
        canvas = tk.Canvas(self.frame)
        scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Secciones de configuración
        self.create_video_config()
        self.create_detection_config()
        self.create_output_config()
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def create_video_config(self):
        """Configuración de video"""
        section = ttk.LabelFrame(self.scrollable_frame, text="Configuración de Video", padding=20)
        section.pack(fill="x", padx=20, pady=10)
        
        # Resolución de procesamiento
        tk.Label(section, text="Resolución de procesamiento:").grid(row=0, column=0, sticky="w", pady=5)
        self.resolution_var = tk.StringVar()
        resolution_combo = ttk.Combobox(section, textvariable=self.resolution_var,
                                       values=["320x240", "640x480", "1280x720", "1920x1080"])
        resolution_combo.grid(row=0, column=1, padx=10, pady=5)
        
        # FPS de procesamiento
        tk.Label(section, text="FPS de procesamiento:").grid(row=1, column=0, sticky="w", pady=5)
        self.fps_var = tk.StringVar()
        fps_combo = ttk.Combobox(section, textvariable=self.fps_var,
                                values=["10", "15", "30", "60"])
        fps_combo.grid(row=1, column=1, padx=10, pady=5)
    
    def create_detection_config(self):
        """Configuración de detección"""
        section = ttk.LabelFrame(self.scrollable_frame, text="Configuración de Detección YOLO", padding=20)
        section.pack(fill="x", padx=20, pady=10)
        
        # Confianza mínima
        tk.Label(section, text="Confianza mínima:").grid(row=0, column=0, sticky="w", pady=5)
        self.confidence_var = tk.DoubleVar()
        confidence_scale = tk.Scale(section, from_=0.1, to=1.0, resolution=0.1,
                                   orient="horizontal", variable=self.confidence_var)
        confidence_scale.grid(row=0, column=1, padx=10, pady=5)
    
    def create_output_config(self):
        """Configuración de salida"""
        section = ttk.LabelFrame(self.scrollable_frame, text="Configuración de Salida", padding=20)
        section.pack(fill="x", padx=20, pady=10)
        
        # Generar video de salida
        self.generate_video_var = tk.BooleanVar()
        tk.Checkbutton(section, text="Generar video con detecciones",
                      variable=self.generate_video_var).grid(row=0, column=0, sticky="w", pady=5)
        
        # Formato de salida
        tk.Label(section, text="Formato de datos:").grid(row=1, column=0, sticky="w", pady=5)
        self.format_var = tk.StringVar()
        format_combo = ttk.Combobox(section, textvariable=self.format_var,
                                   values=["CSV", "JSON", "Excel"])
        format_combo.grid(row=1, column=1, padx=10, pady=5)
    
    def setup_default_values(self):
        """Configurar valores por defecto"""
        self.resolution_var.set("640x480")
        self.fps_var.set("30")
        self.confidence_var.set(0.5)
        self.generate_video_var.set(True)
        self.format_var.set("CSV")
    
    def get_config(self):
        """Obtener configuración actual como diccionario"""
        return {
            'video': {
                'resolution': self.resolution_var.get(),
                'fps': int(self.fps_var.get()),
            },
            'detection': {
                'confidence': self.confidence_var.get(),
            },
            'output': {
                'generate_video': self.generate_video_var.get(),
                'format': self.format_var.get(),
            }
        }