import subprocess

# Ejecutar deepSort.py
print("Ejecutando deepSort.py...")
subprocess.run(["python", "deepSort.py"], check=True)

# Ejecutar paddle_ocr.py después que deepSort.py termine
print("deepSort.py terminó. Ejecutando paddle_ocr.py...")
subprocess.run(["python", "paddle_ocr.py"], check=True)

