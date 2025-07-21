import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from gui.processing.loading_spinner import LoadingSpinner
from utils.styles import BUTTON_STYLES

from gui.processing.processing_utils import (
    validar_campos,
    generar_output_path,
    generar_comando,
    ejecutar_script,
    log_with_timestamp,
)

class ProcessingTab:
    def __init__(self, parent, controller):
        self.controller = controller
        self.video_path = None
        self.csv_path = None
        self.processing = False

        self.frame = ttk.Frame(parent)
        self._crear_interfaz()

    def _crear_interfaz(self):
        # Panel de subida
        upload_panel = ttk.Frame(self.frame)
        upload_panel.pack(fill="x", padx=20, pady=10)

        ttk.Label(upload_panel, text="Nuevo Proyecto", font=("Arial", 16, "bold")).pack(pady=10)

        # Nombre del proyecto
        name_frame = ttk.Frame(upload_panel)
        name_frame.pack(pady=5)
        ttk.Label(name_frame, text="Nombre del Proyecto:").pack(side="left")
        self.project_entry = ttk.Entry(name_frame, width=40)
        self.project_entry.pack(side="left", padx=10)

        # Video
        video_frame = ttk.Frame(upload_panel)
        video_frame.pack(pady=5)
        ttk.Button(video_frame, text="📹 Seleccionar Video", command=self._select_video).pack(side="left")
        self.video_label = ttk.Label(video_frame, text="No seleccionado", foreground="gray")
        self.video_label.pack(side="left", padx=10)

        # CSV
        csv_frame = ttk.Frame(upload_panel)
        csv_frame.pack(pady=5)
        ttk.Button(csv_frame, text="📄 Seleccionar CSV Participantes", command=self._select_csv).pack(side="left")
        self.csv_label = ttk.Label(csv_frame, text="No seleccionado", foreground="gray")
        self.csv_label.pack(side="left", padx=10)

        # Botón de procesamiento
        self.process_button = tk.Button(
            self.frame,
            text="▶️ Iniciar Procesamiento",
            command=self._start_processing,
            **BUTTON_STYLES['success']
        )
        self.process_button.pack(pady=10)

        # Spinner
        self.spinner = LoadingSpinner(self.frame)

        # Log
        log_frame = ttk.Frame(self.frame)
        log_frame.pack(expand=True, fill="both", padx=20, pady=10)

        ttk.Label(log_frame, text="Log de Procesamiento:", font=("Arial", 12, "bold")).pack(anchor="w")
        self.log_text = tk.Text(log_frame, height=12, bg="#2C3E50", fg="#ECF0F1", font=("Consolas", 9))
        scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        self.log_text.pack(side="left", expand=True, fill="both")
        scrollbar.pack(side="right", fill="y")

    def _select_video(self):
        path = filedialog.askopenfilename(title="Seleccionar Video", filetypes=[("Videos", "*.mp4 *.avi *.mov *.mkv")])
        if path:
            self.video_path = path
            self.video_label.config(text=path.split("/")[-1], foreground="black")
            log_with_timestamp(self.log_text, f"📹 Video seleccionado: {path}")

    def _select_csv(self):
        path = filedialog.askopenfilename(title="Seleccionar CSV de Participantes", filetypes=[("CSV Files", "*.csv")])
        if path:
            self.csv_path = path
            self.csv_label.config(text=path.split("/")[-1], foreground="black")
            log_with_timestamp(self.log_text, f"📄 CSV seleccionado: {path}")

    def _start_processing(self):
        project_name = self.project_entry.get().strip()

        valido, error_msg = validar_campos(self.video_path, self.csv_path, project_name)
        if not valido:
            messagebox.showerror("Campos incompletos", error_msg)
            return

        self.controller.set_shared_state("project_name", project_name)
        self.log_text.delete("1.0", "end")

        output_path = generar_output_path(project_name)
        cmd = generar_comando(self.video_path, self.csv_path, output_path)

        self.processing = True
        self.process_button.config(state="disabled")
        self.spinner.start()

        def run():
            try:
                success = ejecutar_script(cmd, lambda m: log_with_timestamp(self.log_text, m))
                if success:
                    log_with_timestamp(self.log_text, "✅ Procesamiento completado con éxito.")
                    self.controller.navigate_to_tab(3)
                else:
                    log_with_timestamp(self.log_text, "❌ El proceso terminó con errores.")
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                self.processing = False
                self.spinner.stop()
                self.process_button.config(state="normal")

        threading.Thread(target=run, daemon=True).start()
