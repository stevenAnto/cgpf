import argparse
import subprocess

# Definir y parsear argumentos
parser = argparse.ArgumentParser(description="Ejecuta el tracking y OCR con argumentos.")
parser.add_argument("--video", required=True, help="Ruta del video a procesar")
parser.add_argument("--rutacsv", required=True, help="Ruta del archivo CSV de salida ")
parser.add_argument("--output", help="Ruta opcional para el archivo CSV de resultados finales")
args = parser.parse_args()

# Pasar los argumentos a deepSort.py y paddle_ocr.py como variables de entorno o argumentos
print("Ejecutando deepSort.py...")
subprocess.run(["python", "deepSort.py", "--video", args.video], check=True)


# Ejecutar paddle_ocr.py después que deepSort.py termine
print("deepSort.py terminó. Ejecutando paddle_ocr.py...")
subprocess.run(["python", "paddle_ocr.py"], check=True)

# Ejecutar procesamiento_datos.py
print("paddle_ocr.py terminó. Ejecutando procesamiento_datos.py...")
cmd = ["python", "procesamiento_datos.py", "--rutacsv", args.rutacsv]
if args.output:
    cmd.extend(["--output", args.output])
subprocess.run(cmd, check=True)

