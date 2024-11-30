# Taller de OpenCV: Creando tus Cámaras Inteligentes

# Importación de librerías necesarias
import cv2  # Librería principal para visión por computadora
import numpy as np  # Para operaciones numéricas y matrices

# Descargar la imagen del logo de Python
import urllib.request  # Para realizar solicitudes a URLs
url = 'https://www.python.org/static/img/python-logo@2x.png'  # URL de la imagen
urllib.request.urlretrieve(url, 'python_logo.png')  # Guarda la imagen como 'python_logo.png'

# Lectura y visualización de la imagen
imagen = cv2.imread('python_logo.png')  # Lee la imagen desde el archivo
cv2.imshow('Logo de Python', imagen)  # Muestra la imagen en una ventana
cv2.waitKey(0)  # Espera a que se presione una tecla
cv2.destroyAllWindows()  # Cierra todas las ventanas abiertas

# Dibujar un rectángulo en la imagen
inicio = (50, 50)  # Punto superior izquierdo del rectángulo (x, y)
fin = (200, 200)  # Punto inferior derecho del rectángulo (x, y)
color_rect = (0, 255, 0)  # Color del rectángulo en formato BGR (Verde)
grosor_rect = 3  # Grosor de la línea del rectángulo
cv2.rectangle(imagen, inicio, fin, color_rect, grosor_rect)  # Dibuja el rectángulo en la imagen
cv2.imshow('Rectángulo en Logo', imagen)  # Muestra la imagen con el rectángulo
cv2.waitKey(0)
cv2.destroyAllWindows()

# Escribir texto en la imagen
texto = 'OpenCV'  # Texto a escribir
ubicacion = (50, 50)  # Coordenadas donde se colocará el texto (x, y)
fuente = cv2.FONT_HERSHEY_SIMPLEX  # Tipo de fuente
escala = 1  # Escala del texto
color_texto = (255, 0, 0)  # Color del texto en formato BGR (Azul)
grosor_texto = 2  # Grosor del texto
cv2.putText(imagen, texto, ubicacion, fuente, escala, color_texto, grosor_texto)  # Escribe el texto en la imagen
cv2.imshow('Texto en Logo', imagen)  # Muestra la imagen con el texto
cv2.waitKey(0)
cv2.destroyAllWindows()

# Conversión a escala de grises
gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)  # Convierte la imagen a escala de grises
cv2.imshow('Imagen en Grises', gris)  # Muestra la imagen en escala de grises
cv2.waitKey(0)
cv2.destroyAllWindows()

# Aplicar desenfoque Gaussiano
desenfoque = cv2.GaussianBlur(imagen, (5, 5), 0)  # Aplica un filtro de desenfoque Gaussiano
cv2.imshow('Imagen Desenfocada', desenfoque)  # Muestra la imagen desenfocada
cv2.waitKey(0)
cv2.destroyAllWindows()

# Detección de bordes con Canny
bordes = cv2.Canny(gris, 100, 200)  # Detecta bordes en la imagen en escala de grises
cv2.imshow('Bordes con Canny', bordes)  # Muestra los bordes detectados
cv2.waitKey(0)
cv2.destroyAllWindows()

# Desplazar (shift) la imagen
filas, columnas = imagen.shape[:2]  # Obtiene las dimensiones de la imagen
M = np.float32([[1, 0, 50], [0, 1, 100]])  # Matriz de transformación para desplazar la imagen
# Desplaza la imagen 50 píxeles a la derecha y 100 píxeles hacia abajo
imagen_desplazada = cv2.warpAffine(imagen, M, (columnas, filas))
cv2.imshow('Imagen Desplazada', imagen_desplazada)  # Muestra la imagen desplazada
cv2.waitKey(0)
cv2.destroyAllWindows()

# Captura de video desde la cámara web y mostrar en tiempo real
cap = cv2.VideoCapture(0)  # Inicia la captura de video desde la cámara por defecto
while True:
    ret, frame = cap.read()  # Lee un frame de la cámara
    if not ret:
        break
    cv2.imshow('Video en Vivo', frame)  # Muestra el frame capturado
    if cv2.waitKey(1) == ord('q'):  # Espera a que se presione 'q' para salir
        break
cap.release()  # Libera la cámara
cv2.destroyAllWindows()

# Aplicar filtro de desenfoque en tiempo real
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if not ret:
        break
    desenfoque = cv2.GaussianBlur(frame, (15, 15), 0)  # Aplica desenfoque al frame
    cv2.imshow('Video Desenfocado', desenfoque)  # Muestra el frame desenfocado
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()

# Convertir video a escala de grises en tiempo real
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if not ret:
        break
    gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convierte el frame a escala de grises
    cv2.imshow('Video en Grises', gris)  # Muestra el frame en escala de grises
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()

# Guardar video procesado (invertir colores)
cap = cv2.VideoCapture(0)  # Inicia la captura de video
fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Define el codec para el video de salida
out = cv2.VideoWriter('video_salida.avi', fourcc, 20.0, (640, 480))  # Crea el objeto de escritura de video
while True:
    ret, frame = cap.read()
    if not ret:
        break
    invertido = cv2.bitwise_not(frame)  # Invierte los colores del frame
    out.write(invertido)  # Escribe el frame invertido en el archivo de salida
    cv2.imshow('Video Invertido', invertido)  # Muestra el frame invertido
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
out.release()  # Libera el objeto de escritura de video
cv2.destroyAllWindows()

# Ejercicio 1: Mostrar una imagen y dibujar un círculo
imagen = cv2.imread('python_logo.png')  # Lee la imagen
centro = (imagen.shape[1] // 2, imagen.shape[0] // 2)  # Calcula el centro de la imagen (x, y)
radio = 50  # Radio del círculo
color_circulo = (0, 0, 255)  # Color del círculo en formato BGR (Rojo)
grosor_circulo = 5  # Grosor de la línea del círculo
cv2.circle(imagen, centro, radio, color_circulo, grosor_circulo)  # Dibuja el círculo en la imagen
cv2.imshow('Círculo en Logo', imagen)  # Muestra la imagen con el círculo
cv2.waitKey(0)
cv2.destroyAllWindows()

# Ejercicio 2: Aplicar filtro de desenfoque en tiempo real
cap = cv2.VideoCapture(0)  # Inicia la captura de video
while True:
    ret, frame = cap.read()
    if not ret:
        break
    desenfoque = cv2.GaussianBlur(frame, (15, 15), 0)  # Aplica desenfoque al frame
    cv2.imshow('Video Desenfocado', desenfoque)  # Muestra el frame desenfocado
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()

# Ejercicio 3: Convertir video a escala de grises
cap = cv2.VideoCapture(0)  # Inicia la captura de video
while True:
    ret, frame = cap.read()
    if not ret:
        break
    gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convierte el frame a escala de grises
    cv2.imshow('Video en Grises', gris)  # Muestra el frame en escala de grises
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()

# Ejercicio 4: Detección de bordes en una imagen
imagen = cv2.imread('python_logo.png')  # Lee la imagen
gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)  # Convierte la imagen a escala de grises
bordes = cv2.Canny(gris, 100, 200)  # Detecta los bordes en la imagen
cv2.imshow('Bordes en Logo', bordes)  # Muestra los bordes detectados
cv2.waitKey(0)
cv2.destroyAllWindows()
