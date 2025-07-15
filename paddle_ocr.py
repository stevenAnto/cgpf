import json
import re
import os
import cv2
from paddleocr import PaddleOCR
import matplotlib.pyplot as plt
import glob

BASE_DIR = os.getcwd()  # Esto es ~/tesis/yolo8 si corres el script desde ahí
DEBUG = False

ocr = PaddleOCR(
    use_doc_orientation_classify=False, 
    use_doc_unwarping=False, 
    use_textline_orientation=False,
)

def preprocess(img):
    original_height, original_width = img.shape[:2]
    new_width = 1200
    aspect_ratio = new_width / original_width
    new_height = int(original_height * aspect_ratio)
    resized_img = cv2.resize(img, (new_width, new_height))
    return resized_img

def read_dorsal(img, should_debug=False, should_paint=False, id=-1):
    should_debug = DEBUG
    img = preprocess(img)
    result = ocr.predict(img)
    dorsal_data = {"text": None, "accuracy": None}
    
    for res in result:
        if should_debug:
            save_path = f"output/video-{id}"
            res.save_to_img(save_path=save_path)
            res.save_to_json(save_path=save_path)
        
        n = len(res["rec_texts"])
        for i in range(n):
            if res["rec_texts"][i].isdigit() and res["rec_scores"][i] > 0.85:
                dorsal_data["text"]     = res["rec_texts"][i]
                dorsal_data["accuracy"] = res["rec_scores"][i]

                if should_paint:
                    for j in range(len(res["dt_polys"][i])):
                        pt1 = res["dt_polys"][i][j]
                        pt2 = res["dt_polys"][i][(j + 1) % len(res["dt_polys"][i])]
                        cv2.line(img, pt1, pt2, color=(0, 255, 0), thickness=5)

    if should_paint:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        plt.imshow(img)
        plt.show()
    
    return dorsal_data
##para sacar el tiempo del archivo
def extract_time_from_filename(filename):
    match = re.search(r"tiempo_(.+?)s\.jpg", filename)
    if match:
        return match.group(1)
    return None

##Guardar en un json
def guardar_diccionario_json(diccionario, nombre_archivo="dorsales_y_tiempos.json", carpeta_salida="."):
    """
    Guarda un diccionario como archivo JSON.

    Parámetros:
    - diccionario: dict — El diccionario a guardar.
    - nombre_archivo: str — Nombre del archivo JSON (por defecto: 'dorsales_y_tiempos.json').
    - carpeta_salida: str — Carpeta donde se guardará el archivo (por defecto: carpeta actual).

    Retorna:
    - ruta completa del archivo JSON guardado.
    """
    ruta_completa = os.path.join(carpeta_salida, nombre_archivo)
    with open(ruta_completa, 'w', encoding='utf-8') as f:
        json.dump(diccionario, f, ensure_ascii=False, indent=4)
    print(f"\n✅ Diccionario guardado como JSON en: {ruta_completa}")
    return ruta_completa

if __name__ == "__main__":
    DEBUG = False

    # Carpeta con tus imágenes
    image_folder = os.path.join(BASE_DIR, "fotosCapturadas")

    # Buscar todas las imágenes (.jpg, .jpeg, .png)
    image_paths = glob.glob(os.path.join(image_folder, "*.jpg")) + \
                  glob.glob(os.path.join(image_folder, "*.jpeg")) + \
                  glob.glob(os.path.join(image_folder, "*.png"))
    
    print(f"[INFO] Se encontraron {len(image_paths)} image:")

    dorsal_to_time = {}

    # Procesar cada imagen
    for idx, image_path in enumerate(sorted(image_paths)):
        filename = os.path.basename(image_path)

        print(f"\n[INFO] Procesando imagen {idx + 1}/{len(image_paths)}: {filename}")

        img = cv2.imread(image_path)

        if img is None:
            print(f"[ERROR] No se pudo leer la imagen: {image_path}")
            continue

        result = read_dorsal(img, should_debug=False, should_paint=False, id=idx)
        
        print(f"{filename} → {result['text']} (confianza: {result['accuracy']})")

        dorsal = result['text']
        tiempo = extract_time_from_filename(filename)


        if dorsal is not None and tiempo is not None:
            dorsal_to_time[dorsal] = tiempo


    print("\n📋 Diccionario dorsal → tiempo:")
    for dorsal, tiempo in dorsal_to_time.items():
        print(f"{dorsal}: {tiempo}")

    guardar_diccionario_json(dorsal_to_time)

