import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
import threading
import os
from datetime import datetime
from .loading_spinner import LoadingSpinner


class ProcessingTab:
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        self.processing = False
        self.create_tab()

    def create_tab(self):
        self.frame = ttk.Frame(self.parent)

        upload_panel = tk.Frame(self.frame, bg="#ECF0F1", height=200)
        upload_panel.pack(fill="x", padx=20, pady=10)
        upload_panel.pack_propagate(False)

        tk.Label(upload_panel, text="Nuevo Proyecto", bg="#ECF0F1", font=("Arial", 16, "bold")).pack(pady=10)

        name_frame = tk.Frame(upload_panel, bg="#ECF0F1")
        name_frame.pack(pady=5)
        tk.Label(name_frame, text="Nombre del Proyecto:", bg="#ECF0F1").pack(side="left")
        self.project_entry = tk.Entry(name_frame, width=40)
        self.project_entry.pack(side="left", padx=10)

        video_frame = tk.Frame(upload_panel, bg="#ECF0F1")
        video_frame.pack(pady=5)
        tk.Button(video_frame, text="📹 Seleccionar Video", command=self.select_video).pack(side="left")
        self.video_label = tk.Label(video_frame, text="No seleccionado", bg="#ECF0F1", fg="gray")
        self.video_label.pack(side="left", padx=10)

        csv_frame = tk.Frame(upload_panel, bg="#ECF0F1")
        csv_frame.pack(pady=5)
        tk.Button(csv_frame, text="📄 Seleccionar CSV Participantes", command=self.select_csv).pack(side="left")
        self.csv_label = tk.Label(csv_frame, text="No seleccionado", bg="#ECF0F1", fg="gray")
        self.csv_label.pack(side="left", padx=10)

        self.process_button = tk.Button(self.frame, text="▶️ Iniciar Procesamiento",
                                        command=self.start_processing,
                                        bg="#27AE60", fg="white", font=("Arial", 12, "bold"), pady=10)
        self.process_button.pack(pady=10)

        self.spinner = LoadingSpinner(self.frame)

        log_frame = tk.Frame(self.frame)
        log_frame.pack(expand=True, fill="both", padx=20, pady=10)

        tk.Label(log_frame, text="Log de Procesamiento:", font=("Arial", 12, "bold")).pack(anchor="w")

        self.log_text = tk.Text(log_frame, height=12, bg="#2C3E50", fg="#ECF0F1", font=("Consolas", 9))
        log_scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=log_scrollbar.set)

        self.log_text.pack(side="left", expand=True, fill="both")
        log_scrollbar.pack(side="right", fill="y")

    def select_video(self):
        path = filedialog.askopenfilename(title="Seleccionar Video", filetypes=[("Videos", "*.mp4 *.avi *.mov *.mkv")])
        if path:
            self.controller.set_shared_state('video_path', path)
            self.video_label.config(text=os.path.basename(path))
            self.update_log(f"📹 Video seleccionado: {path}")

    def select_csv(self):
        path = filedialog.askopenfilename(title="Seleccionar CSV de Participantes", filetypes=[("CSV Files", "*.csv")])
        if path:
            self.controller.set_shared_state('csv_path', path)
            self.csv_label.config(text=os.path.basename(path))
            self.update_log(f"📄 CSV seleccionado: {path}")

    def start_processing(self):
        video_path = self.controller.get_shared_state('video_path')
        csv_path = self.controller.get_shared_state('csv_path')
        project_name = self.project_entry.get().strip()

        if not all([video_path, csv_path, project_name]):
            messagebox.showerror("Campos incompletos", "Selecciona video, CSV y escribe un nombre de proyecto.")
            return

        self.controller.set_shared_state('project_name', project_name)
        self.log_text.delete("1.0", "end")

        output_dir = "./resultados"
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, f"{project_name}.csv")

        cmd = ["python", "run_all.py", "--video", video_path, "--rutacsv", csv_path, "--output", output_path]

        self.process_button.config(state="disabled")
        self.spinner.start()
        self.processing = True

        def run_command():
            try:
                self.update_log("⏳ Ejecutando script...")

                env = os.environ.copy()
                env["DISABLE_GUI"] = "1"

                self.update_log(f"🔧 Comando: {' '.join(cmd)}")

                process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                           text=True, env=env)

                for line in process.stdout:
                    if line:
                        self.update_log(line.strip())

                process.wait()

                if process.returncode == 0:
                    self.update_log("✅ Procesamiento completado con éxito.")
                    self.controller.navigate_to_tab(3)
                else:
                    self.update_log("❌ El proceso terminó con errores.")

            except Exception as e:
                self.update_log(f"❌ Excepción: {str(e)}")
                messagebox.showerror("Error", f"Excepción al ejecutar: {str(e)}")
            finally:
                self.processing = False
                self.spinner.stop()
                self.process_button.config(state="normal")

        threading.Thread(target=run_command, daemon=True).start()

    def update_log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert("end", f"[{timestamp}] {message}\n")
        self.log_text.see("end")
