# 🏃‍♂️ Sistema de Detección y Reconocimiento de Corredores

Este proyecto utiliza YOLOv8, DeepSORT y PaddleOCR para detectar corredores en video, capturar imágenes cuando cruzan una línea de meta, reconocer automáticamente el número del dorsal mediante OCR, y generar un reporte CSV final cruzando datos de entrada con resultados detectados.

---

## 📁 Estructura del Proyecto

```
subirGithub/
├── ambientePaddle/           # Entorno virtual con dependencias
├── deepSort.py               # Script de detección + tracking + captura de imagen
├── paddle_ocr.py             # OCR sobre imágenes capturadas
├── procesamiento_datos.py    # Procesamiento final de resultados con CSV
├── fotosCapturadas/          # Imágenes de corredores detectados
├── inputCSV/                 # CSV de entrada con datos de corredores
│   └── datos_corredores.csv
├── outputPaddle/             # Resultados intermedios del OCR
│   ├── dorsales_y_tiempos.json
│   └── dorsales_y_tiempos.csv
├── outputCSV/                # Resultados finales cruzados
│   └── resultado_final.csv
├── yolov8n.pt                # Modelo YOLOv8
├── run_all.py                # Script principal que ejecuta todo el pipeline
├── Videos3Corredores/        # Carpeta con videos de prueba
│   └── v14.mp4
├── requirements.txt          # Requerimientos de Python
└── README.md
```

---

## 🚀 Requisitos

- Python **3.12**
- pip ≥ 25.1.1
- Sistema operativo Linux (probado en Ubuntu 22.04)

---

## ⚙️ Instalación

1. **Ubícate en el directorio del proyecto**:

```bash
cd subirGithub/
```

2. **Activa el entorno virtual**:

```bash
source ambientePaddle/bin/activate
```

3. **Instala las dependencias**:

```bash
pip install -r requirements.txt
```

---

## ▶️ Ejecución

Ejecuta el pipeline completo con el siguiente comando(si no se pone el argumento output, se guardara automaticamente en outputCSV):

```bash
python run_all.py --video ./Videos3Corredores/v14.mp4 --rutacsv ./inputCSV/datos_corredores.csv --output ./aquiResultado.csv
```

Este script realiza lo siguiente:

1. 🧍‍♂️ **`deepSort.py`**  
   Detecta corredores en el video y guarda imágenes cuando cruzan la línea de meta.  
   ➤ Resultado: imágenes en `fotosCapturadas/`.

2. 🔍 **`paddle_ocr.py`**  
   Realiza OCR sobre las imágenes capturadas para extraer los dorsales.  
   ➤ Resultado:  
   - JSON: `outputPaddle/dorsales_y_tiempos.json`  
   - CSV: `outputPaddle/dorsales_y_tiempos.csv`

3. 📊 **`procesamiento_datos.py`**  
   Cruza los resultados del OCR con los datos del archivo CSV de entrada.  
   ➤ Resultado: `outputCSV/resultado_final.csv`

---

## 📌 Consideraciones importantes

- **Debes mantener los nombres de las carpetas**:  
  `fotosCapturadas/`, `outputPaddle/`, `outputCSV/`, `inputCSV/`, `Videos3Corredores/`.

- Las imágenes capturadas se guardan con el nombre:  
  `persona_<ID>_tiempo_<minutos>:<segundos>s.jpg`

- Solo se procesan dorsales con confianza OCR mayor a **0.85**.

- Asegúrate de que el video de entrada exista en la ruta indicada (`./Videos3Corredores/`).

---

## 📸 Ejemplo de imagen capturada

```
fotosCapturadas/persona_6_tiempo_5:13s.jpg
```

---

## 🧠 Tecnologías Utilizadas

- [YOLOv8](https://docs.ultralytics.com) — detección de personas.
- [DeepSORT](https://github.com/mikel-brostrom/Yolov5_DeepSort_Pytorch) — tracking de objetos.
- [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) — reconocimiento óptico de caracteres.
- Python `argparse`, `OpenCV`, `subprocess`, `json`, `csv`, entre otros.

---

## 🎥 Video Explicativo

Mira este breve video donde se muestra en acción el sistema de detección, captura y OCR:

[🔗 Ver en YouTube](https://youtu.be/yAxhWeii_Tg)

[![Ver video](https://img.youtube.com/vi/yAxhWeii_Tg/0.jpg)](https://youtu.be/yAxhWeii_Tg)

---

## 📂 Licencia

Este proyecto forma parte de una tesis universitaria. Su uso está permitido únicamente con fines académicos o de investigación.
