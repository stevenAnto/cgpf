# main.py - Interfaz Mejorada
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
import os
import shutil
import csv
from datetime import datetime
import threading

class CarrerasApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🏁 Sistema de Cronometraje de Carreras - v2.0")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
        # Variables principales
        self.video_path = None
        self.processing = False
        self.resultados_data = []
        
        # Configurar estilo
        self.setup_styles()
        
        # Configurar interfaz
        self.setup_main_interface()
        
        # Configurar grid principal
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
    
    def setup_styles(self):
        """Configurar estilos TTK"""
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
    
    def setup_main_interface(self):
        """Configurar interfaz principal"""
        # Panel lateral izquierdo
        self.sidebar = tk.Frame(self.root, bg="#2C3E50", width=250)
        self.sidebar.grid(row=0, column=0, sticky="ns")
        self.sidebar.grid_propagate(False)
        
        # Header del sidebar
        header_frame = tk.Frame(self.sidebar, bg="#2C3E50")
        header_frame.pack(fill="x", pady=20)
        
        title_label = tk.Label(header_frame, text="🏁 YOLO ", 
                              bg="#2C3E50", fg="white", 
                              font=("Arial", 16, "bold"))
        title_label.pack()
        
        subtitle_label = tk.Label(header_frame, text="Sistema de Cronometraje", 
                                 bg="#2C3E50", fg="#BDC3C7", 
                                 font=("Arial", 10))
        subtitle_label.pack()
        
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
        self.create_home_tab()
        self.create_config_tab()
        self.create_processing_tab()
        self.create_results_tab()
        self.create_about_tab()
    
    def create_nav_buttons(self):
        """Crear botones de navegación lateral"""
        nav_buttons = [
            ("🏠 Inicio", lambda: self.notebook.select(0)),
            ("⚙️ Configuración", lambda: self.notebook.select(1)),
            ("🎬 Procesamiento", lambda: self.notebook.select(2)),
            ("📊 Resultados", lambda: self.notebook.select(3)),
            ("ℹ️ Acerca de", lambda: self.notebook.select(4))
        ]
        
        for text, command in nav_buttons:
            btn = tk.Button(self.sidebar, text=text, command=command,
                           bg="#34495E", fg="white", font=("Arial", 11),
                           bd=0, pady=15, width=20,
                           activebackground="#3498DB", activeforeground="white",
                           cursor="hand2", anchor="w", padx=20)
            btn.pack(fill="x", padx=20, pady=5)
    
    def create_home_tab(self):
        """Pestaña de inicio"""
        home_frame = ttk.Frame(self.notebook)
        self.notebook.add(home_frame, text="🏠 Inicio")
        
        # Header
        header = tk.Frame(home_frame, bg="#3498DB", height=100)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        tk.Label(header, text="Bienvenido al Sistema de Cronometraje", 
                bg="#3498DB", fg="white", font=("Arial", 18, "bold")).pack(pady=30)
        
        # Panel principal
        main_content = tk.Frame(home_frame)
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
                                lambda: self.quick_start())
        card1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # Card 2: Ver Resultados
        card2 = self.create_card(cards_frame, "📊 Ver Resultados", 
                                "Revisar rankings anteriores",
                                lambda: self.notebook.select(3))
        card2.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        # Card 3: Configuración
        card3 = self.create_card(cards_frame, "⚙️ Configuración", 
                                "Ajustar parámetros del sistema",
                                lambda: self.notebook.select(1))
        card3.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        # Card 4: Análisis
        card4 = self.create_card(cards_frame, "📈 Análisis", 
                                "Estadísticas y gráficos",
                                lambda: self.notebook.select(4))
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
    
    def create_config_tab(self):
        """Pestaña de configuración"""
        config_frame = ttk.Frame(self.notebook)
        self.notebook.add(config_frame, text="⚙️ Configuración")
        
        # Crear scrollable frame
        canvas = tk.Canvas(config_frame)
        scrollbar = ttk.Scrollbar(config_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Secciones de configuración
        self.create_video_config(scrollable_frame)
        self.create_detection_config(scrollable_frame)
        self.create_output_config(scrollable_frame)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def create_video_config(self, parent):
        """Configuración de video"""
        section = ttk.LabelFrame(parent, text="Configuración de Video", padding=20)
        section.pack(fill="x", padx=20, pady=10)
        
        # Resolución de procesamiento
        tk.Label(section, text="Resolución de procesamiento:").grid(row=0, column=0, sticky="w", pady=5)
        self.resolution_var = tk.StringVar(value="640x480")
        resolution_combo = ttk.Combobox(section, textvariable=self.resolution_var,
                                       values=["320x240", "640x480", "1280x720", "1920x1080"])
        resolution_combo.grid(row=0, column=1, padx=10, pady=5)
        
        # FPS de procesamiento
        tk.Label(section, text="FPS de procesamiento:").grid(row=1, column=0, sticky="w", pady=5)
        self.fps_var = tk.StringVar(value="30")
        fps_combo = ttk.Combobox(section, textvariable=self.fps_var,
                                values=["10", "15", "30", "60"])
        fps_combo.grid(row=1, column=1, padx=10, pady=5)
    
    def create_detection_config(self, parent):
        """Configuración de detección"""
        section = ttk.LabelFrame(parent, text="Configuración de Detección YOLO", padding=20)
        section.pack(fill="x", padx=20, pady=10)
        
        # Confianza mínima
        tk.Label(section, text="Confianza mínima:").grid(row=0, column=0, sticky="w", pady=5)
        self.confidence_var = tk.DoubleVar(value=0.5)
        confidence_scale = tk.Scale(section, from_=0.1, to=1.0, resolution=0.1,
                                   orient="horizontal", variable=self.confidence_var)
        confidence_scale.grid(row=0, column=1, padx=10, pady=5)
        
    
    def create_output_config(self, parent):
        """Configuración de salida"""
        section = ttk.LabelFrame(parent, text="Configuración de Salida", padding=20)
        section.pack(fill="x", padx=20, pady=10)
        
        # Generar video de salida
        self.generate_video_var = tk.BooleanVar(value=True)
        tk.Checkbutton(section, text="Generar video con detecciones",
                      variable=self.generate_video_var).grid(row=0, column=0, sticky="w", pady=5)
        
        # Formato de salida
        tk.Label(section, text="Formato de datos:").grid(row=1, column=0, sticky="w", pady=5)
        self.format_var = tk.StringVar(value="CSV")
        format_combo = ttk.Combobox(section, textvariable=self.format_var,
                                   values=["CSV", "JSON", "Excel"])
        format_combo.grid(row=1, column=1, padx=10, pady=5)
    
    def create_processing_tab(self):
        """Pestaña de procesamiento"""
        proc_frame = ttk.Frame(self.notebook)
        self.notebook.add(proc_frame, text="🎬 Procesamiento")
        
        # Panel superior - Carga de archivo
        upload_panel = tk.Frame(proc_frame, bg="#ECF0F1", height=150)
        upload_panel.pack(fill="x", padx=20, pady=20)
        upload_panel.pack_propagate(False)
        
        tk.Label(upload_panel, text="Seleccionar Video para Procesar", 
                bg="#ECF0F1", font=("Arial", 14, "bold")).pack(pady=20)
        
        file_frame = tk.Frame(upload_panel, bg="#ECF0F1")
        file_frame.pack()
        
        self.file_label = tk.Label(file_frame, text="No hay archivo seleccionado", 
                                  bg="#ECF0F1", fg="#7F8C8D")
        self.file_label.pack(side="left", padx=10)
        
        tk.Button(file_frame, text="📁 Seleccionar Video", command=self.select_video,
                 bg="#3498DB", fg="white", font=("Arial", 10, "bold"),
                 bd=0, pady=10, activebackground="#2980B9", cursor="hand2").pack(side="left", padx=10)
        
        # Panel de procesamiento
        process_panel = tk.Frame(proc_frame)
        process_panel.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Barra de progreso
        progress_frame = tk.Frame(process_panel)
        progress_frame.pack(fill="x", pady=20)
        
        tk.Label(progress_frame, text="Progreso de Procesamiento:", 
                font=("Arial", 12, "bold")).pack(anchor="w")
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var,
                                           maximum=100, length=400)
        self.progress_bar.pack(fill="x", pady=10)
        
        self.status_label = tk.Label(progress_frame, text="Listo para procesar", 
                                    fg="#27AE60", font=("Arial", 10))
        self.status_label.pack(anchor="w")
        
        # Botones de control
        button_frame = tk.Frame(process_panel)
        button_frame.pack(pady=20)
        
        self.process_btn = tk.Button(button_frame, text="▶️ Iniciar Procesamiento", 
                                    command=self.start_processing,
                                    bg="#27AE60", fg="white", font=("Arial", 12, "bold"),
                                    bd=0, pady=15, width=20,
                                    activebackground="#229954", cursor="hand2")
        self.process_btn.pack(side="left", padx=10)
        
        self.stop_btn = tk.Button(button_frame, text="⏹️ Detener", 
                                 command=self.stop_processing,
                                 bg="#E74C3C", fg="white", font=("Arial", 12, "bold"),
                                 bd=0, pady=15, width=15, state="disabled",
                                 activebackground="#C0392B", cursor="hand2")
        self.stop_btn.pack(side="left", padx=10)
        
        # Log de procesamiento
        log_frame = tk.Frame(process_panel)
        log_frame.pack(expand=True, fill="both", pady=20)
        
        tk.Label(log_frame, text="Log de Procesamiento:", 
                font=("Arial", 12, "bold")).pack(anchor="w")
        
        self.log_text = tk.Text(log_frame, height=10, bg="#2C3E50", fg="#ECF0F1",
                               font=("Consolas", 9))
        log_scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=log_scrollbar.set)
        
        self.log_text.pack(side="left", expand=True, fill="both")
        log_scrollbar.pack(side="right", fill="y")
    
    def create_results_tab(self):
        """Pestaña de resultados"""
        results_frame = ttk.Frame(self.notebook)
        self.notebook.add(results_frame, text="📊 Resultados")
        
        # Panel de filtros
        filter_panel = tk.Frame(results_frame, bg="#ECF0F1")
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
        table_frame = tk.Frame(results_frame)
        table_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        columns = ("Posición", "TimeStamp", "Dorsal","Género")
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
        action_panel = tk.Frame(results_frame)
        action_panel.pack(fill="x", padx=20, pady=20)
        
        tk.Button(action_panel, text="💾 Exportar CSV", command=self.export_csv,
                 bg="#27AE60", fg="white", font=("Arial", 10, "bold"),
                 bd=0, pady=10, activebackground="#229954", cursor="hand2").pack(side="left", padx=10)
        
        tk.Button(action_panel, text="🖨️ Imprimir", command=self.print_results,
                 bg="#9B59B6", fg="white", font=("Arial", 10, "bold"),
                 bd=0, pady=10, activebackground="#8E44AD", cursor="hand2").pack(side="left", padx=10)
    
    
    def create_about_tab(self):
        """Pestaña acerca de"""
        about_frame = ttk.Frame(self.notebook)
        self.notebook.add(about_frame, text="ℹ️ Acerca de")
        
        # Header
        header = tk.Frame(about_frame, bg="#2C3E50", height=120)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        tk.Label(header, text="🏁 Sistema de Cronometraje AI", 
                bg="#2C3E50", fg="white", font=("Arial", 20, "bold")).pack(pady=20)
        tk.Label(header, text="Versión 2.0 - Tecnología YOLO + OpenCV", 
                bg="#2C3E50", fg="#BDC3C7", font=("Arial", 12)).pack()
        
        # Contenido
        content = tk.Frame(about_frame)
        content.pack(expand=True, fill="both", padx=40, pady=40)
        
        info_text = """
        Este sistema utiliza inteligencia artificial para el análisis automático 
        de videos de carreras, detectando corredores y generando rankings precisos.
        
        Características principales:
        • Detección automática de corredores con YOLO v8
        • Seguimiento de objetos en tiempo real
        • Reconocimiento de dorsales con OCR
        • Generación automática de rankings
        • Análisis de velocidad y métricas
        • Exportación de resultados en múltiples formatos
        
        Tecnologías utilizadas:
        • Python 3.8+
        • OpenCV para procesamiento de video
        • YOLO v8 para detección de objetos
        • EasyOCR para reconocimiento de texto
        • Docker para containerización
        • Tkinter para la interfaz gráfica
        """
        
        tk.Label(content, text=info_text, justify="left", 
                font=("Arial", 11), wraplength=800).pack(pady=20)
        
        # Información del sistema
        system_frame = tk.Frame(content, bg="#ECF0F1")
        system_frame.pack(fill="x", pady=20)
        
        tk.Label(system_frame, text="Información del Sistema", 
                bg="#ECF0F1", font=("Arial", 14, "bold")).pack(pady=10)
        
        tk.Label(system_frame, text=f"Desarrollado en 2025 | Python {python_version()}", 
                bg="#ECF0F1", font=("Arial", 10)).pack(pady=5)
    
    # Métodos de funcionalidad
    def quick_start(self):
        """Inicio rápido - seleccionar video y ir a procesamiento"""
        if self.select_video():
            self.notebook.select(2)  # Ir a pestaña de procesamiento
    
    def select_video(self):
        """Seleccionar archivo de video"""
        filetypes = [
            ("Videos", "*.mp4 *.avi *.mov *.mkv *.wmv"),
            ("MP4", "*.mp4"),
            ("AVI", "*.avi"),
            ("Todos los archivos", "*.*")
        ]
        
        path = filedialog.askopenfilename(
            title="Seleccionar Video de Carrera",
            filetypes=filetypes
        )
        
        if path:
            self.video_path = path
            filename = os.path.basename(path)
            self.file_label.config(text=f"📹 {filename}")
            self.log_message(f"Video seleccionado: {filename}")
            return True
        return False
    
    def start_processing(self):
        """Iniciar procesamiento en hilo separado"""
        if not self.video_path:
            messagebox.showerror("Error", "Primero selecciona un video")
            return
        
        if self.processing:
            messagebox.showwarning("Advertencia", "Ya hay un procesamiento en curso")
            return
        
        # Cambiar estado de botones
        self.process_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        self.processing = True
        
        # Iniciar procesamiento en hilo separado
        thread = threading.Thread(target=self.process_video_thread)
        thread.daemon = True
        thread.start()
    
    def process_video_thread(self):
        """Procesamiento en hilo separado"""
        try:
            self.update_status("Preparando procesamiento...")
            self.update_progress(10)
            
            # Crear directorios
            os.makedirs("input", exist_ok=True)
            os.makedirs("output", exist_ok=True)
            
            # Copiar video
            video_name = os.path.basename(self.video_path)
            input_path = f"input/{video_name}"
            shutil.copy2(self.video_path, input_path)
            
            self.log_message(f"Video copiado a: {input_path}")
            self.update_progress(30)
            
            # Preparar comando Docker
            cmd = [
                "docker", "run", "--rm",
                "-v", f"{os.getcwd()}/input:/app/input",
                "-v", f"{os.getcwd()}/output:/app/output",
                "mi-yolo-app"
            ]
            
            self.update_status("Ejecutando procesamiento YOLO...")
            self.update_progress(50)
            
            # Ejecutar Docker
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, 
                                     stderr=subprocess.PIPE, text=True)
            
            # Leer salida en tiempo real
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    self.log_message(output.strip())
            
            # Obtener código de salida
            return_code = process.poll()
            
            if return_code == 0:
                self.update_progress(90)
                self.update_status("Cargando resultados...")
                self.load_results()
                self.update_progress(100)
                self.update_status("Procesamiento completado exitosamente")
                self.root.after(0, lambda: messagebox.showinfo("Éxito", "Video procesado correctamente"))
            else:
                error_output = process.stderr.read()
                self.log_message(f"Error: {error_output}")
                self.update_status("Error en procesamiento")
                self.root.after(0, lambda: messagebox.showerror("Error", f"Error en procesamiento: {error_output}"))
                
        except Exception as e:
            self.log_message(f"Excepción: {str(e)}")
            self.update_status("Error inesperado")
            self.root.after(0, lambda: messagebox.showerror("Error", f"Error inesperado: {str(e)}"))
        
        finally:
            # Restaurar estado de botones
            self.processing = False
            self.root.after(0, self.reset_processing_buttons)
    
    def stop_processing(self):
        """Detener procesamiento"""
        if messagebox.askyesno("Confirmar", "¿Estás seguro de detener el procesamiento?"):
            self.processing = False
            self.update_status("Procesamiento detenido por el usuario")
            self.reset_processing_buttons()
    
    def reset_processing_buttons(self):
        """Restaurar estado de botones de procesamiento"""
        self.process_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        self.update_progress(0)
    
    def update_status(self, message):
        """Actualizar mensaje de estado"""
        self.root.after(0, lambda: self.status_label.config(text=message))
    
    def update_progress(self, value):
        """Actualizar barra de progreso"""
        self.root.after(0, lambda: self.progress_var.set(value))
    
    def log_message(self, message):
        """Agregar mensaje al log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"
        
        def update_log():
            self.log_text.insert(tk.END, formatted_message)
            self.log_text.see(tk.END)
        
        self.root.after(0, update_log)
    
    def load_results(self):
        """Cargar resultados desde archivos de salida"""
        try:
            # Buscar archivos CSV en la carpeta output
            csv_files = [f for f in os.listdir("output") if f.endswith('.csv')]
            
            if csv_files:
                csv_path = os.path.join("output", csv_files[0])
                with open(csv_path, 'r', encoding='utf-8') as file:
                    reader = csv.DictReader(file)
                    self.resultados_data = list(reader)
                
                self.log_message(f"Resultados cargados: {len(self.resultados_data)} registros")
                self.root.after(0, self.update_results_table)
            else:
                # Datos de ejemplo si no hay archivo
                self.resultados_data = [
                    {"Posición": "1", "Dorsal": "001", "Tiempo": "10:25:30", 
                     "Velocidad": "12.5 km/h", "Categoría": "Adulto", "Género": "M"},
                    {"Posición": "2", "Dorsal": "034", "Tiempo": "10:47:15", 
                     "Velocidad": "11.8 km/h", "Categoría": "Adulto", "Género": "F"},
                    {"Posición": "3", "Dorsal": "102", "Tiempo": "11:12:45", 
                     "Velocidad": "10.9 km/h", "Categoría": "Juvenil", "Género": "M"}
                ]
                self.log_message("Usando datos de ejemplo (no se encontró CSV)")
                
        except Exception as e:
            self.log_message(f"Error cargando resultados: {str(e)}")
    
    def update_results_table(self):
        """Actualizar tabla de resultados"""
        # Limpiar tabla
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        
        # Agregar datos
        for resultado in self.resultados_data:
            values = (
                resultado.get("Posición", ""),
                resultado.get("Dorsal", ""),
                resultado.get("Tiempo", ""),
                resultado.get("Velocidad", ""),
                resultado.get("Categoría", ""),
                resultado.get("Género", "")
            )
            self.results_tree.insert("", "end", values=values)
    
    def apply_filters(self):
        """Aplicar filtros a los resultados"""
        category = self.category_filter.get()
        gender = self.gender_filter.get()
        
        # Limpiar tabla
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        
        # Filtrar y mostrar datos
        for resultado in self.resultados_data:
            show_item = True
            
            if category != "Todas" and resultado.get("Categoría") != category:
                show_item = False
            
            if gender != "Todos" and resultado.get("Género") != gender:
                show_item = False
            
            if show_item:
                values = (
                    resultado.get("Posición", ""),
                    resultado.get("Dorsal", ""),
                    resultado.get("Tiempo", ""),
                    resultado.get("Velocidad", ""),
                    resultado.get("Categoría", ""),
                    resultado.get("Género", "")
                )
                self.results_tree.insert("", "end", values=values)
    
    def export_csv(self):
        """Exportar resultados a CSV"""
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
                    if self.resultados_data:
                        fieldnames = self.resultados_data[0].keys()
                        writer = csv.DictWriter(file, fieldnames=fieldnames)
                        writer.writeheader()
                        writer.writerows(self.resultados_data)
                
                messagebox.showinfo("Éxito", f"Resultados exportados a:\n{filename}")
                self.log_message(f"Resultados exportados: {filename}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Error al exportar: {str(e)}")
    
    def send_results(self):
        """Enviar resultados por email (placeholder)"""
        messagebox.showinfo("Función en desarrollo", 
                           "La función de envío por email estará disponible en la próxima versión")
    
    def print_results(self):
        """Imprimir resultados (placeholder)"""
        messagebox.showinfo("Función en desarrollo", 
                           "La función de impresión estará disponible en la próxima versión")
    
    def run(self):
        """Ejecutar la aplicación"""
        self.root.mainloop()

def python_version():
    """Obtener versión de Python"""
    import sys
    return f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"

if __name__ == "__main__":
    try:
        app = CarrerasApp()
        app.run()
    except Exception as e:
        print(f"Error al iniciar la aplicación: {e}")
        messagebox.showerror("Error crítico", f"Error al iniciar la aplicación:\n{e}")