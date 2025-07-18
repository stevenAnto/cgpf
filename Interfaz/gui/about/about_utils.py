import platform
import sys

def get_about_description():
    return (
        "Este sistema usa inteligencia artificial para analizar videos de carreras, "
        "detectando corredores y generando rankings automáticos.\n\n"
        "Características:\n"
        "• Detección con YOLOv8\n"
        "• Seguimiento en tiempo real\n"
        "• Reconocimiento de dorsales\n"
        "• Exportación de resultados\n\n"
        "Tecnologías:\n"
        "• Python 3.8+\n"
        "• OpenCV, EasyOCR\n"
        "• Docker, Tkinter"
    )

def get_system_info():
    return {
        "os": f"{platform.system()} {platform.release()}",
        "arch": platform.machine(),
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    }
