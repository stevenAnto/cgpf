import argparse
import os
import cv2
from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort

# Leer argumento del video
parser = argparse.ArgumentParser()
parser.add_argument("--video", required=True, help="Ruta al video a procesar")
args = parser.parse_args()

# Verificar si se deben mostrar ventanas
mostrar_ventanas = os.environ.get("DISABLE_GUI", "0") != "1"

# Cargar el modelo YOLOv8
model = YOLO('yolov8n.pt')

# Inicializar el tracker DeepSORT
tracker = DeepSort(max_age=60, n_init=10)

# Línea de meta (puedes ajustar)
line_y = 550

# Abrir el video
cap = cv2.VideoCapture(args.video)
ids_cruzaron = set()

if mostrar_ventanas:
    cv2.namedWindow("Detección + Tracking", cv2.WINDOW_AUTOSIZE)

# Procesar cada frame
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frameOriginal = frame.copy()
    results = model(frame)[0]
    detections = []

    if results.boxes is not None and len(results.boxes) > 0:
        cuantos_hay = len(results.boxes)
        if mostrar_ventanas:
            cv2.putText(frame, f"Detectados por Yolo: {cuantos_hay}", (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        for r in results.boxes:
            cls = int(r.cls.cpu().numpy()[0])
            if cls == 0:
                x1, y1, x2, y2 = r.xyxy.cpu().numpy()[0]
                conf = float(r.conf.cpu().numpy()[0])
                detections.append(([x1, y1, x2 - x1, y2 - y1], conf, cls))

        if mostrar_ventanas:
            cv2.putText(frame, f"Lista Detection: {len(detections)}", (500, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    tracks = tracker.update_tracks(detections, frame=frame)
    if mostrar_ventanas:
        cv2.line(frame, (0, line_y), (frame.shape[1], line_y), (0, 255, 255), 2)
        cv2.putText(frame, f"Tracks activos: {len(tracks)}", (500, 500),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    for track in tracks:
        if not track.is_confirmed():
            continue

        track_id = track.track_id
        l, t, r, b = map(int, track.to_tlbr())
        cx, cy = (l + r) // 2, (t + b) // 2

        if mostrar_ventanas:
            cv2.rectangle(frame, (l, t), (r, b), (0, 255, 0), 2)
            cv2.putText(frame, f"ID: {track_id}", ((l + r) // 2, (t + b) // 2),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        if (b >= line_y) and (track_id not in ids_cruzaron):
            print(f"Persona ID {track_id} cruzó la meta!")
            ids_cruzaron.add(track_id)

            tiempo_ms = cap.get(cv2.CAP_PROP_POS_MSEC)
            tiempo_seg = tiempo_ms / 1000

            crop = frameOriginal[t:b, l:r]
            filename = f"fotosCapturadas/persona_{track_id}_tiempo_{tiempo_seg:.2f}s.jpg".replace('.', '-', 1)
            cv2.imwrite(filename, crop)

    if mostrar_ventanas:
        cv2.imshow("Detección + Tracking", frame)
        if cv2.waitKey(1) == 27:
            break

cap.release()
if mostrar_ventanas:
    cv2.destroyAllWindows()
