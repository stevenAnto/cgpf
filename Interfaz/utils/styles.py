# utils/styles.py - Configuración de estilos
from tkinter import ttk

def setup_styles():
    """Configurar estilos TTK para toda la aplicación"""
    style = ttk.Style()
    style.theme_use('clam')
    
    # Estilo para notebook
    style.configure('Custom.TNotebook', tabposition='n')
    style.configure('Custom.TNotebook.Tab', padding=[20, 10])
    
    # Estilo para botones principales
    style.configure('Action.TButton', font=('Arial', 10, 'bold'))
    style.configure('Success.TButton', foreground='white', background='#27AE60')
    style.configure('Warning.TButton', foreground='white', background='#F39C12')
    style.configure('Danger.TButton', foreground='white', background='#E74C3C')
    
    # Estilo para frames
    style.configure('Card.TFrame', relief='raised', borderwidth=2)

# Colores constantes
COLORS = {
    'primary': '#3498DB',
    'primary_dark': '#2980B9',
    'secondary': '#2C3E50',
    'secondary_light': '#34495E',
    'success': '#27AE60',
    'success_dark': '#229954',
    'warning': '#F39C12',
    'warning_dark': '#E67E22',
    'danger': '#E74C3C',
    'danger_dark': '#C0392B',
    'light': '#ECF0F1',
    'muted': '#7F8C8D',
    'white': '#FFFFFF'
}

# Configuraciones de botones
BUTTON_STYLES = {
    'primary': {
        'bg': COLORS['primary'],
        'fg': COLORS['white'],
        'activebackground': COLORS['primary_dark'],
        'activeforeground': COLORS['white'],
        'font': ('Arial', 10, 'bold'),
        'bd': 0,
        'cursor': 'hand2'
    },
    'success': {
        'bg': COLORS['success'],
        'fg': COLORS['white'],
        'activebackground': COLORS['success_dark'],
        'activeforeground': COLORS['white'],
        'font': ('Arial', 10, 'bold'),
        'bd': 0,
        'cursor': 'hand2'
    },
    'warning': {
        'bg': COLORS['warning'],
        'fg': COLORS['white'],
        'activebackground': COLORS['warning_dark'],
        'activeforeground': COLORS['white'],
        'font': ('Arial', 10, 'bold'),
        'bd': 0,
        'cursor': 'hand2'
    },
    'danger': {
        'bg': COLORS['danger'],
        'fg': COLORS['white'],
        'activebackground': COLORS['danger_dark'],
        'activeforeground': COLORS['white'],
        'font': ('Arial', 10, 'bold'),
        'bd': 0,
        'cursor': 'hand2'
    }
}