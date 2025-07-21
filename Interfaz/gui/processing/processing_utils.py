import os
import subprocess
from datetime import datetime

def validar_campos(video_path, csv_path, project_name):
    if not video_path:
        return False, "Selecciona un video."
    if not csv_path:
        return False, "Selecciona un archivo CSV."
    if not project_name.strip():
        return False, "El nombre del proyecto no puede estar vacío."
    return True, ""

def generar_output_path(project_name):
    os.makedirs("resultados", exist_ok=True)
    return os.path.join("resultados", f"{project_name}.csv")

def generar_comando(video_path, csv_path, output_path):
    return [
        "python", "run_all.py",
        "--video", video_path,
        "--rutacsv", csv_path,
        "--output", output_path
    ]

def ejecutar_script(cmd, log_callback):
    log_callback("⏳ Ejecutando script...")
    log_callback(f"🔧 Comando: {' '.join(cmd)}")

    env = os.environ.copy()
    env["DISABLE_GUI"] = "1"

    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            env=env
        )

        for line in process.stdout:
            if line:
                log_callback(line.strip())

        process.wait()
        return process.returncode == 0
    except Exception as e:
        log_callback(f"❌ Error: {e}")
        raise e

def log_with_timestamp(widget, message):
    timestamp = datetime.now().strftime("%H:%M:%S")
    widget.insert("end", f"[{timestamp}] {message}\n")
    widget.see("end")
