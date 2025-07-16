# gui/about_tab.py
import tkinter as tk
from tkinter import ttk
import platform
import sys

class AboutTab:
    def __init__(self, notebook, controller=None):
        self.controller = controller
        self.notebook = notebook
        self.frame = ttk.Frame(self.notebook)
        self.create_about_tab()
    
    def create_about_tab(self):
        """Pestaña Acerca de - diseño simplificado"""

        # Encabezado
        header = tk.Frame(self.frame, bg="#2C3E50", height=120)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        tk.Label(header, text="🏁 Sistema de Cronometraje AI",
                 bg="#2C3E50", fg="white", font=("Arial", 20, "bold")).pack(pady=20)
        tk.Label(header, text="Versión 2.0 - YOLO + OpenCV",
                 bg="#2C3E50", fg="#BDC3C7", font=("Arial", 12)).pack()
        
        # Contenido principal
        content = tk.Frame(self.frame)
        content.pack(expand=True, fill="both", padx=40, pady=40)
        
        info_text = """
Este sistema usa inteligencia artificial para analizar videos de carreras, 
detectando corredores y generando rankings automáticos.

Características:
• Detección con YOLOv8
• Seguimiento en tiempo real
• Reconocimiento de dorsales
• Exportación de resultados

Tecnologías:
• Python 3.8+
• OpenCV, EasyOCR
• Docker, Tkinter
        """
        
        tk.Label(content, text=info_text, justify="left",
                 font=("Arial", 11), wraplength=800).pack(pady=20)
        
        # Información del sistema
        sys_info = f"""
Sistema:
• SO: {platform.system()} {platform.release()}
• Arquitectura: {platform.machine()}
• Python: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}
        """
        tk.Label(content, text=sys_info, justify="left",
                 font=("Arial", 10), fg="#555").pack(pady=10)
