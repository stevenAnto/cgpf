import argparse
import cv2
from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort

# Cargar el modelo YOLOv8 (puede ser 'yolov8n.pt', 'yolov8s.pt', etc.)
model = YOLO('yolov8n.pt')

# Inicializar el tracker DeepSORT
# max_age: cuántos frames esperar antes de eliminar una pista perdida
tracker = DeepSort(max_age=60,n_init=10) #Si en 30 frames, no vuelve eliminarla para siempre

# Línea de meta (posición vertical en píxeles del frame)
line_y = 550 #puedes ajustarla a donde esté tu meta

# Parsear argumento del video
parser = argparse.ArgumentParser()
parser.add_argument("--video", required=True, help="Ruta al video a procesar")
args = parser.parse_args()

# Abrir el video (puede ser una cámara si usas 0)
cap = cv2.VideoCapture(args.video)

# Conjunto para guardar los IDs de personas que ya cruzaron la meta
ids_cruzaron = set()

# ESTA LÍNEA ANTES DEL BUCLE while True:

cv2.namedWindow("Detección + Tracking", cv2.WINDOW_AUTOSIZE)
# Bucle principal: procesar cada frame del video
while True:
    ret, frame = cap.read()
    if not ret:
        break  # si no hay más frames, se termina

    # Ejecutar YOLO en el frame actual
    frameOriginal = frame.copy()
    results = model(frame)[0]  # resultados del modelo
    detections = []  # lista para guardar solo personas


        # Verificar si hay detecciones
    if results.boxes is not None and len(results.boxes) > 0:
        # Filtrar solo personas
        cuantos_hay = len(results.boxes)
        cv2.putText(frame, f"Detectados por Yolo: {cuantos_hay}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        for r in results.boxes:
            cls = int(r.cls.cpu().numpy()[0])
            if cls == 0:  # clase 0 = persona
                x1, y1, x2, y2 = r.xyxy.cpu().numpy()[0]
                conf = float(r.conf.cpu().numpy()[0])
                detections.append(([x1, y1, x2 - x1, y2 - y1], conf, cls))
        cv2.putText(frame, f"Lista Detection: {len(detections)}", (500, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)


    # Preparar detecciones para el tracker en formato [x1, y1, x2, y2, conf]
    dets_for_tracker =detections
    # Actualizar el tracker con las detecciones del frame actual
    tracks = tracker.update_tracks(dets_for_tracker, frame=frame)

    # Dibujar la línea de meta en el frame
    cv2.line(frame, (0, line_y), (frame.shape[1], line_y), (0, 255, 255), 2)

    # Recorrer todas las pistas activas (personas detectadas y seguidas)
    cv2.putText(frame, f"Tracks activos: {len(tracks)}", (500, 500),
            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
    for track in tracks:
        if not track.is_confirmed():#Solo aquellos, que estan siendo detectadas varios frames seguidos
            continue  # ignorar pistas no confirmadas

        track_id = track.track_id  # ID único de esta persona

        # Obtener coordenadas del bounding box como top-left/bottom-right
        l, t, r, b = map(int, track.to_tlbr())

        # Calcular el centro del bounding box (para verificar cruce)
        cx, cy = (l + r) // 2, (t + b) // 2

        # Dibujar el bbox y el ID sobre el frame
        cv2.rectangle(frame, (l, t), (r, b), (0, 255, 0), 2)
        cv2.putText(frame, f"ID: {track_id}", ((l+r)//2, (t+b)//2),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        # Verificar si el centro del bbox está muy cerca de la línea de meta
        if (b >= line_y) and (track_id not in ids_cruzaron):
            print(f"Persona ID {track_id} cruzó la meta!")  # registrar el cruce
            ids_cruzaron.add(track_id)  # guardar que ya cruzó
            # Obtener el tiempo actual del video en segundos
            tiempo_ms = cap.get(cv2.CAP_PROP_POS_MSEC)
            tiempo_seg = tiempo_ms / 1000  # redondear hacia abajo

            # Recortar la imagen de la persona
            crop = frameOriginal[t:b, l:r]
            filename = f"fotosCapturadas/persona_{track_id}_tiempo_{tiempo_seg:.2f}s.jpg".replace('.','-',1)

            # Guardar la imagen con nombre único por ID
            cv2.imwrite(filename, crop)

    # Mostrar el frame con anotaciones en una ventana
    cv2.imshow("Detección + Tracking", frame)

    # Salir si el usuario presiona la tecla ESC
    if cv2.waitKey(1) == 27:
        break

# Liberar el video y cerrar ventanas al terminar
cap.release()
cv2.destroyAllWindows()
