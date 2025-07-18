import tkinter as tk
from tkinter import ttk
from gui.about.about_utils import get_about_description, get_system_info

class AboutTab:
    def __init__(self, notebook, controller=None):
        self.controller = controller
        self.notebook = notebook
        self.frame = ttk.Frame(self.notebook)
        self.create_about_tab()
    
    def create_about_tab(self):
        header = tk.Frame(self.frame, bg="#2C3E50", height=120)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        tk.Label(header, text="🏁 Sistema de Cronometraje AI",
                 bg="#2C3E50", fg="white", font=("Arial", 20, "bold")).pack(pady=20)
        tk.Label(header, text="Versión 2.0 - YOLO + OpenCV",
                 bg="#2C3E50", fg="#BDC3C7", font=("Arial", 12)).pack()
        
        content = tk.Frame(self.frame)
        content.pack(expand=True, fill="both", padx=40, pady=40)
        
        tk.Label(content, text=get_about_description(), justify="left",
                 font=("Arial", 11), wraplength=800).pack(pady=20)
        
        sys_info = get_system_info()
        sys_text = f"""
Sistema:
• SO: {sys_info["os"]}
• Arquitectura: {sys_info["arch"]}
• Python: {sys_info["python_version"]}
        """
        tk.Label(content, text=sys_text, justify="left",
                 font=("Arial", 10), fg="#555").pack(pady=10)
