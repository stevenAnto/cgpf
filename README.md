# 🏃‍♂️ Sistema de Detección y Reconocimiento de Corredores

Este proyecto utiliza YOLOv8, DeepSORT y PaddleOCR para detectar corredores en video, capturar imágenes cuando cruzan una línea de meta, y reconocer automáticamente el número del dorsal usando OCR.

---

## 📁 Estructura del Proyecto

```
tesis/yolo8/
├── ambientePaddle/          # Entorno virtual con dependencias
├── deepSort.py              # Script de detección + tracking + captura de imagen
├── paddle_ocr.py            # OCR sobre imágenes capturadas
├── fotosCapturadas/         # Imágenes de corredores detectados
├── yolov8n.pt               # Modelo YOLOv8
├── requirements.txt         # Requerimientos de Python
├── run_all.py               # Script principal que ejecuta todo
├── Videos3Corredores/       # Carpeta con videos de prueba
└── dorsales_y_tiempos.json  # Archivo generado con resultados OCR (dorsal → tiempo)
```

---

## 🚀 Requisitos

- Python **3.12**
- pip ≥ 25.1.1
- Sistema operativo Linux (probado en Ubuntu)

---

## ⚙️ Instalación

1. **Clona el repositorio** o ubica el directorio del proyecto.

2. **Activa el entorno virtual**:

```bash
source ambientePaddle/bin/activate
```

3. **Instala los requerimientos**:

```bash
pip install -r requirements.txt
```

---

## ▶️ Ejecución

Corre el script principal:

```bash
python run_all.py
```

Este script hará lo siguiente:

1. Ejecuta `deepSort.py`, que procesa el video `Videos3Corredores/v14.mp4`, detecta corredores y guarda sus imágenes en `fotosCapturadas/`.

2. Luego corre `paddle_ocr.py`, que realiza OCR sobre las imágenes y extrae los dorsales.

3. Finalmente, genera un archivo `dorsales_y_tiempos.json` con la siguiente estructura:

```json
{
    "123": "3:20",
    "127": "5:13",
    "108": "6:53"
}
```

---

## 📌 Notas

- Actualmente el sistema solo procesa el video `v14.mp4` por defecto.
- Las imágenes se guardan como: `persona_<ID>_tiempo_<minutos>:<segundos>s.jpg`.
- Solo se detectan y reconocen dorsales si tienen una **confianza mayor a 0.85**.

---

## 📸 Ejemplo de imagen capturada

```
fotosCapturadas/persona_6_tiempo_5:13s.jpg
```

---

## 🧠 Tecnologías Usadas

- [YOLOv8](https://docs.ultralytics.com) — para detección de personas.
- [DeepSORT](https://github.com/mikel-brostrom/Yolov5_DeepSort_Pytorch) — para tracking de personas.
- [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) — para reconocimiento de texto (dorsales).

---
## 🎥 Video explicativo

Mira este breve video donde se muestra en acción el sistema de detección, captura y OCR:


[🔗 Ver en YouTube](https://youtu.be/yAxhWeii_Tg)

[![Ver video](https://img.youtube.com/vi/yAxhWeii_Tg/0.jpg)](https://youtu.be/yAxhWeii_Tg)

## 📂 Licencia

Este proyecto es parte de una tesis universitaria. Uso académico o investigativo únicamente.
