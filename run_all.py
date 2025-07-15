import argparse
import subprocess

# Definir y parsear argumentos
parser = argparse.ArgumentParser(description="Ejecuta el tracking y OCR con argumentos.")
parser.add_argument("--video", required=True, help="Ruta del video a procesar")
args = parser.parse_args()

# Pasar los argumentos a deepSort.py y paddle_ocr.py como variables de entorno o argumentos
print("Ejecutando deepSort.py...")
subprocess.run(["python", "deepSort.py", "--video", args.video], check=True)


# Ejecutar paddle_ocr.py después que deepSort.py termine
print("deepSort.py terminó. Ejecutando paddle_ocr.py...")
subprocess.run(["python", "paddle_ocr.py"], check=True)

