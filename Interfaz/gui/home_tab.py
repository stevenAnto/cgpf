# gui/home_tab.py - Basado en funcionalidad existente
import tkinter as tk
from tkinter import ttk
from utils.styles import COLORS

class HomeTab:
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        self.create_tab()
    
    def create_tab(self):
        """Crear pestaña de inicio"""
        self.frame = ttk.Frame(self.parent)
        
        # Header
        header = tk.Frame(self.frame, bg="#3498DB", height=100)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        tk.Label(header, text="Bienvenido al Sistema de Cronometraje", 
                bg="#3498DB", fg="white", font=("Arial", 18, "bold")).pack(pady=30)
        
        # Panel principal
        main_content = tk.Frame(self.frame)
        main_content.pack(expand=True, fill="both", padx=40, pady=40)
        
        # Cards de acciones rápidas
        cards_frame = tk.Frame(main_content)
        cards_frame.pack(expand=True, fill="both")
        
        # Grid de cards
        cards_frame.grid_rowconfigure(0, weight=1)
        cards_frame.grid_rowconfigure(1, weight=1)
        cards_frame.grid_columnconfigure(0, weight=1)
        cards_frame.grid_columnconfigure(1, weight=1)
        
        # Card 1: Nuevo Proyecto
        card1 = self.create_card(cards_frame, "🎬 Cargar Nuevo Video", 
                                "Cargar video y comenzar procesamiento",
                                self.quick_start)
        card1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # Card 2: Ver Resultados
        card2 = self.create_card(cards_frame, "📊 Ver Resultados", 
                                "Revisar rankings anteriores",
                                lambda: self.controller.navigate_to_tab(3))
        card2.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        # Card 3: Configuración
        card3 = self.create_card(cards_frame, "⚙️ Configuración", 
                                "Ajustar parámetros del sistema",
                                lambda: self.controller.navigate_to_tab(1))
        card3.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        # Card 4: Acerca de
        card4 = self.create_card(cards_frame, "ℹ️ Acerca de", 
                                "Información del sistema",
                                lambda: self.controller.navigate_to_tab(4))
        card4.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
    
    def create_card(self, parent, title, description, command):
        """Crear card de acción"""
        card = tk.Frame(parent, bg="white", relief="raised", bd=2)
        
        tk.Label(card, text=title, bg="white", 
                font=("Arial", 14, "bold")).pack(pady=(20, 5))
        
        tk.Label(card, text=description, bg="white", 
                font=("Arial", 10), fg="#7F8C8D", 
                wraplength=200).pack(pady=5)
        
        tk.Button(card, text="Abrir", command=command,
                 bg="#3498DB", fg="white", font=("Arial", 10, "bold"),
                 bd=0, pady=10, width=15,
                 activebackground="#2980B9", cursor="hand2").pack(pady=20)
        
        return card
    
    def quick_start(self):
        """Inicio rápido - seleccionar video y ir a procesamiento"""
        # Navegar a la pestaña de procesamiento
        self.controller.navigate_to_tab(2)