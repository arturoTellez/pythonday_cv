import cv2
import torch
from ultralytics import YOLO
import requests
from dotenv import load_dotenv
from collections import deque
import os


# Cargar variables del archivo .env
load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')



# Validar que las claves existan
if not TELEGRAM_TOKEN or not CHAT_ID:
    print("Error: Faltan las configuraciones de Telegram en el archivo .env.")
    exit()



# Función para enviar alertas por Telegram
def enviar_alerta(mensaje):
    url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
    data = {'chat_id': CHAT_ID, 'text': mensaje}
    response = requests.post(url, data=data)
    if response.status_code == 200:
        print("Alerta enviada con éxito.")
    else:
        print("Error al enviar la alerta.")

# Función para enviar imágenes por Telegram
def enviar_imagen(image_path):
    url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto'
    with open(image_path, 'rb') as photo_file:
        response = requests.post(url, data={'chat_id': CHAT_ID}, files={'photo': photo_file})
    if response.status_code == 200:
        print("Imagen enviada con éxito.")
    else:
        print("Error al enviar la imagen:", response.text)

# Función para enviar videos por Telegram
def enviar_video(video_path):
    url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendVideo'
    with open(video_path, 'rb') as video_file:
        response = requests.post(url, data={'chat_id': CHAT_ID}, files={'video': video_file})
    if response.status_code == 200:
        print("Video enviado con éxito.")
    else:
        print("Error al enviar el video:", response.text)




# Parámetros de video
video_source = 0  # Cambiar a 'ruta/video.mp4' si usas un archivo de video
output_video = 'evento.mp4'
buffer = deque(maxlen=50)  # Buffer para 50 frames antes del evento
post_event_frames = 50  # Frames posteriores al evento
video_frames = []  # Frames para el video del evento

# Cargar el modelo YOLOv5
model = YOLO('yolov5n.pt')  # YOLOv5n: Versión nano, más rápida

# Conexión a la fuente de video
cap = cv2.VideoCapture(video_source)

if not cap.isOpened():
    print("Error al abrir la fuente de video.")
    exit()

print("Procesando video. Presiona 'q' para salir.")

evento_detectado = False
post_event_counter = 0  # Contador para frames posteriores al evento


# TODO: ¿Qué ocurre si hay múltiples detecciones de personas? ¿Cómo manejar casos de detección repetitiva de la misma persona?
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("No se pudo leer el frame. Finalizando...")
        break

    # Agregar frame al buffer
    buffer.append(frame)

    # Detección de objetos en el frame
    results = model(frame)

    for result in results:
        for box in result.boxes:
            cls = int(box.cls[0])
            label = model.names[cls]
            if label == 'person':
                # Si se detecta una persona
                if not evento_detectado:
                    print("¡Evento detectado! Guardando frames...")
                    video_frames.extend(list(buffer))  # Añadir 50 frames previos
                    cv2.imwrite('evento.jpg', frame)  # Guardar el frame como imagen
                    #enviar_imagen('evento.jpg')  # Enviar la imagen por Telegram
                evento_detectado = True
                post_event_counter = 0  # Reiniciar el contador posterior

    # Si el evento está en curso, agregar frames posteriores
    if evento_detectado:
        video_frames.append(frame)
        post_event_counter += 1
        if post_event_counter > post_event_frames:
            break

    # Mostrar el frame con las detecciones
    annotated_frame = results[0].plot()
    cv2.imshow('Detección en Tiempo Real', annotated_frame)

    # Salir al presionar 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Guardar el video capturado
if video_frames:
    height, width, _ = video_frames[0].shape
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video, fourcc, 30, (width, height))
    for frame in video_frames:
        out.write(frame)
    out.release()
    print(f"Video guardado como {output_video}. Enviando por Telegram...")
    enviar_video(output_video)

cap.release()
cv2.destroyAllWindows()
