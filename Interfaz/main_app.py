# main_app.py - Aplicación principal con estado compartido
import tkinter as tk
from tkinter import ttk, messagebox
import sys
from gui.home_tab import HomeTab
from gui.config_tab import ConfigTab
from gui.processing_tab import ProcessingTab
from gui.results_tab import ResultsTab
from gui.about_tab import AboutTab
from utils.styles import setup_styles

class CarrerasApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🏁 Sistema de Cronometraje de Carreras - v2.0")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
        # Estado compartido centralizado
        self.shared_state = {
            'video_path': None,
            'processing': False,
            'resultados_data': [],
            'config': {}
        }
        
        # Configurar estilo
        setup_styles()
        
        # Configurar interfaz
        self.setup_main_interface()
        
        # Configurar grid principal
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
    
    def setup_main_interface(self):
        """Configurar interfaz principal"""
        # Panel lateral izquierdo
        self.sidebar = tk.Frame(self.root, bg="#2C3E50", width=250)
        self.sidebar.grid(row=0, column=0, sticky="ns")
        self.sidebar.grid_propagate(False)
        
        # Header del sidebar
        self.create_sidebar_header()
        
        # Botones de navegación
        self.create_nav_buttons()
        
        # Panel principal derecho
        self.main_panel = tk.Frame(self.root, bg="white")
        self.main_panel.grid(row=0, column=1, sticky="nsew")
        self.main_panel.grid_rowconfigure(0, weight=1)
        self.main_panel.grid_columnconfigure(0, weight=1)
        
        # Notebook para las pestañas
        self.notebook = ttk.Notebook(self.main_panel, style='Custom.TNotebook')
        self.notebook.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Crear todas las pestañas
        self.create_tabs()
    
    def create_sidebar_header(self):
        """Crear header del sidebar"""
        header_frame = tk.Frame(self.sidebar, bg="#2C3E50")
        header_frame.pack(fill="x", pady=20)
        
        title_label = tk.Label(header_frame, text="🏁 CARRERAS AI", 
                              bg="#2C3E50", fg="white", 
                              font=("Arial", 16, "bold"))
        title_label.pack()
        
        subtitle_label = tk.Label(header_frame, text="Sistema de Cronometraje", 
                                 bg="#2C3E50", fg="#BDC3C7", 
                                 font=("Arial", 10))
        subtitle_label.pack()
    
    def create_nav_buttons(self):
        """Crear botones de navegación lateral"""
        nav_buttons = [
            ("🏠 Inicio", lambda: self.navigate_to_tab(0)),
            ("⚙️ Configuración", lambda: self.navigate_to_tab(1)),
            ("🎬 Procesamiento", lambda: self.navigate_to_tab(2)),
            ("📊 Resultados", lambda: self.navigate_to_tab(3)),
            ("ℹ️ Acerca de", lambda: self.navigate_to_tab(4))
        ]
        
        for text, command in nav_buttons:
            btn = tk.Button(self.sidebar, text=text, command=command,
                           bg="#34495E", fg="white", font=("Arial", 11),
                           bd=0, pady=15, width=20,
                           activebackground="#3498DB", activeforeground="white",
                           cursor="hand2", anchor="w", padx=20)
            btn.pack(fill="x", padx=20, pady=5)
    
    def create_tabs(self):
        """Crear todas las pestañas"""
        # Instanciar todas las pestañas pasando self como controller
        self.home_tab = HomeTab(self.notebook, self)
        self.config_tab = ConfigTab(self.notebook, self)
        self.processing_tab = ProcessingTab(self.notebook, self)
        self.results_tab = ResultsTab(self.notebook, self)
        self.about_tab = AboutTab(self.notebook, self)
        
        # Agregar pestañas al notebook
        self.notebook.add(self.home_tab.frame, text="🏠 Inicio")
        self.notebook.add(self.config_tab.frame, text="⚙️ Configuración")
        self.notebook.add(self.processing_tab.frame, text="🎬 Procesamiento")
        self.notebook.add(self.results_tab.frame, text="📊 Resultados")
        self.notebook.add(self.about_tab.frame, text="ℹ️ Acerca de")
    
    # Métodos para manejo de estado compartido
    def get_shared_state(self, key=None):
        """Obtener estado compartido"""
        if key:
            return self.shared_state.get(key)
        return self.shared_state
    
    def set_shared_state(self, key, value):
        """Establecer estado compartido y notificar cambios"""
        self.shared_state[key] = value
        self.notify_state_change(key, value)
    
    def notify_state_change(self, key, value):
        """Notificar a pestañas sobre cambios de estado"""
        if key == 'video_path':
            # Notificar a processing_tab que hay nuevo video
            if hasattr(self.processing_tab, 'on_video_changed'):
                self.processing_tab.on_video_changed(value)
        
        if key == 'resultados_data':
            # Notificar a results_tab que hay nuevos datos
            if hasattr(self.results_tab, 'on_data_changed'):
                self.results_tab.on_data_changed(value)
    
    def navigate_to_tab(self, tab_index):
        """Navegar a una pestaña específica"""
        self.notebook.select(tab_index)
    
    def quick_start(self):
        """Inicio rápido - seleccionar video y ir a procesamiento"""
        # Navegar a procesamiento y permitir que maneje la selección
        self.navigate_to_tab(2)
        
        # Intentar seleccionar video si el método existe
        if hasattr(self.processing_tab, 'select_video'):
            return self.processing_tab.select_video()
        return False
    
    def run(self):
        """Ejecutar la aplicación"""
        self.root.mainloop()

def python_version():
    """Obtener versión de Python"""
    return f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"

if __name__ == "__main__":
    try:
        app = CarrerasApp()
        app.run()
    except Exception as e:
        print(f"Error al iniciar la aplicación: {e}")
        messagebox.showerror("Error crítico", f"Error al iniciar la aplicación:\n{e}")