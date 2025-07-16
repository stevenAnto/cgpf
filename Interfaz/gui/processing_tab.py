# gui/processing_tab.py - Con scripts externos multiplataforma
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
import os
import shutil
import threading
import platform
from datetime import datetime
from utils.styles import COLORS

class ProcessingTab:
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        self.create_tab()
    
    def create_tab(self):
        """Crear pestaña de procesamiento"""
        self.frame = ttk.Frame(self.parent)
        
        # Panel superior - Carga de archivo
        upload_panel = tk.Frame(self.frame, bg="#ECF0F1", height=150)
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
        process_panel = tk.Frame(self.frame)
        process_panel.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Información del sistema
        system_frame = tk.Frame(process_panel, bg="#F8F9FA", relief="solid", bd=1)
        system_frame.pack(fill="x", pady=(0, 20))
        
        system_info = f"Sistema: {platform.system()} {platform.release()}"
        script_name = "run_docker.bat" if platform.system() == "Windows" else "run_docker.sh"
        
        tk.Label(system_frame, text=f"🖥️ {system_info}", 
                bg="#F8F9FA", font=("Arial", 9)).pack(anchor="w", padx=10, pady=5)
        tk.Label(system_frame, text=f"📝 Script: {script_name}", 
                bg="#F8F9FA", font=("Arial", 9)).pack(anchor="w", padx=10, pady=(0, 5))
        
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
    
    def get_script_name(self):
        """Obtener nombre del script según el sistema operativo"""
        if platform.system() == "Windows":
            return "run_docker.bat"
        else:
            return "run_docker.sh"
    
    def verify_script_exists(self):
        """Verificar que el script existe y es ejecutable"""
        script_name = self.get_script_name()
        script_path = os.path.join(os.getcwd(), script_name)
        
        if not os.path.exists(script_path):
            self.log_message(f"ERROR: Script {script_name} no encontrado en {os.getcwd()}")
            return False
        
        # En Linux/Mac, verificar permisos de ejecución
        if platform.system() != "Windows":
            import stat
            st = os.stat(script_path)
            if not (st.st_mode & stat.S_IEXEC):
                self.log_message(f"Intentando hacer ejecutable: {script_name}")
                try:
                    os.chmod(script_path, st.st_mode | stat.S_IEXEC)
                    self.log_message(f"Permisos de ejecución otorgados a {script_name}")
                except Exception as e:
                    self.log_message(f"ERROR: No se pudo hacer ejecutable {script_name}: {e}")
                    return False
        
        return True
    
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
            # Actualizar estado compartido
            self.controller.set_shared_state('video_path', path)
            filename = os.path.basename(path)
            self.file_label.config(text=f"📹 {filename}")
            self.log_message(f"Video seleccionado: {filename}")
            return True
        return False
    
    def start_processing(self):
        """Iniciar procesamiento en hilo separado"""
        video_path = self.controller.get_shared_state('video_path')
        if not video_path:
            messagebox.showerror("Error", "Primero selecciona un video")
            return
        
        if self.controller.get_shared_state('processing'):
            messagebox.showwarning("Advertencia", "Ya hay un procesamiento en curso")
            return
        
        # Verificar que el script existe
        if not self.verify_script_exists():
            messagebox.showerror("Error", f"Script {self.get_script_name()} no encontrado o no ejecutable")
            return
        
        # Cambiar estado de botones
        self.process_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        self.controller.set_shared_state('processing', True)
        
        # Iniciar procesamiento en hilo separado
        thread = threading.Thread(target=self.process_video_thread)
        thread.daemon = True
        thread.start()
    
    def process_video_thread(self):
        """Procesamiento en hilo separado usando script externo"""
        try:
            self.update_status("Preparando procesamiento...")
            self.update_progress(10)
            
            # Crear directorios
            os.makedirs("input", exist_ok=True)
            os.makedirs("output", exist_ok=True)
            
            # Copiar video
            video_path = self.controller.get_shared_state('video_path')
            video_name = os.path.basename(video_path)
            input_path = f"input/{video_name}"
            shutil.copy2(video_path, input_path)
            
            self.log_message(f"Video copiado a: {input_path}")
            self.update_progress(30)
            
            # Preparar comando del script
            script_name = self.get_script_name()
            script_path = os.path.join(os.getcwd(), script_name)
            
            if platform.system() == "Windows":
                cmd = [script_path]
            else:
                cmd = ["bash", script_path]
            
            self.log_message(f"Ejecutando script: {script_name}")
            self.update_status("Ejecutando procesamiento YOLO...")
            self.update_progress(50)
            
            # Ejecutar script
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, 
                                     stderr=subprocess.PIPE, text=True,
                                     cwd=os.getcwd())
            
            # Leer salida en tiempo real
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    self.log_message(output.strip())
                    # Actualizar progreso basado en keywords
                    self.parse_progress_from_output(output)
            
            # Obtener código de salida
            return_code = process.poll()
            
            if return_code == 0:
                self.update_progress(90)
                self.update_status("Cargando resultados...")
                self.load_results()
                self.update_progress(100)
                self.update_status("Procesamiento completado exitosamente")
                self.controller.root.after(0, 
                    lambda: messagebox.showinfo("Éxito", "Video procesado correctamente"))
            else:
                error_output = process.stderr.read()
                self.log_message(f"Error: {error_output}")
                self.update_status("Error en procesamiento")
                self.controller.root.after(0, 
                    lambda: messagebox.showerror("Error", f"Error en procesamiento: {error_output}"))
                
        except Exception as e:
            self.log_message(f"Excepción: {str(e)}")
            self.update_status("Error inesperado")
            self.controller.root.after(0, 
                lambda: messagebox.showerror("Error", f"Error inesperado: {str(e)}"))
        
        finally:
            # Restaurar estado de botones
            self.controller.set_shared_state('processing', False)
            self.controller.root.after(0, self.reset_processing_buttons)
    
    def parse_progress_from_output(self, output):
        """Parsear progreso desde la salida del script"""
        output_lower = output.lower()
        
        if "iniciando" in output_lower:
            self.update_progress(50)
        elif "procesamiento" in output_lower and "yolo" in output_lower:
            self.update_progress(60)
        elif "progreso:" in output_lower:
            try:
                # Buscar porcentaje en la línea
                import re
                match = re.search(r'(\d+\.?\d*)%', output)
                if match:
                    progress = float(match.group(1))
                    # Mapear de 0-100% del video a 60-85% del progreso total
                    mapped_progress = 60 + (progress * 0.25)
                    self.update_progress(mapped_progress)
            except:
                pass
        elif "completado" in output_lower:
            self.update_progress(85)
    
    def stop_processing(self):
        """Detener procesamiento"""
        if messagebox.askyesno("Confirmar", "¿Estás seguro de detener el procesamiento?"):
            self.controller.set_shared_state('processing', False)
            self.update_status("Procesamiento detenido por el usuario")
            self.reset_processing_buttons()
    
    def reset_processing_buttons(self):
        """Restaurar estado de botones de procesamiento"""
        self.process_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        self.update_progress(0)
    
    def update_status(self, message):
        """Actualizar mensaje de estado"""
        self.controller.root.after(0, lambda: self.status_label.config(text=message))
    
    def update_progress(self, value):
        """Actualizar barra de progreso"""
        self.controller.root.after(0, lambda: self.progress_var.set(value))
    
    def log_message(self, message):
        """Agregar mensaje al log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"
        
        def update_log():
            self.log_text.insert(tk.END, formatted_message)
            self.log_text.see(tk.END)
        
        self.controller.root.after(0, update_log)
    
    def load_results(self):
        """Cargar resultados desde archivos de salida"""
        try:
            import csv
            # Buscar archivos CSV en la carpeta output
            if not os.path.exists("output"):
                self.log_message("Carpeta output no existe")
                return
                
            csv_files = [f for f in os.listdir("output") if f.endswith('.csv')]
            
            if csv_files:
                csv_path = os.path.join("output", csv_files[0])
                with open(csv_path, 'r', encoding='utf-8') as file:
                    reader = csv.DictReader(file)
                    resultados_data = list(reader)
                
                # Actualizar estado compartido
                self.controller.set_shared_state('resultados_data', resultados_data)
                self.log_message(f"Resultados cargados: {len(resultados_data)} registros")
            else:
                # Datos de ejemplo si no hay archivo
                resultados_data = [
                    {"Posición": "1", "TimeStamp": "00:10:25", "Dorsal": "001", "Género": "M"},
                    {"Posición": "2", "TimeStamp": "00:10:47", "Dorsal": "034", "Género": "F"},
                    {"Posición": "3", "TimeStamp": "00:11:12", "Dorsal": "102", "Género": "M"}
                ]
                self.controller.set_shared_state('resultados_data', resultados_data)
                self.log_message("Usando datos de ejemplo (no se encontró CSV)")
                
        except Exception as e:
            self.log_message(f"Error cargando resultados: {str(e)}")
    
    def on_video_changed(self, video_path):
        """Callback cuando cambia el video seleccionado"""
        if video_path:
            filename = os.path.basename(video_path)
            self.file_label.config(text=f"📹 {filename}")
        else:
            self.file_label.config(text="No hay archivo seleccionado")