import threading
import time
import cv2
import mediapipe as mp
import pydirectinput
import math


# Constantes e configurações
VIDEO_PATH = 0                          # caminho do vídeo
VIDEO_SIZE = (640, 480)                 # tamanho do vídeo
JUMP_NOSE_HEIGHT_THRESHOLD = 35         # altura do nariz para calibrar o pulo (Quanto maior, mais alto o pulo)
SQUAT_NOSE_HEIGHT_THRESHOLD = 70        # altura do nariz para calibrar o agachamento (Quanto maior, mais baixo o agachamento)
DISTANCE_INDEX_SHOULDER_THRESHOLD = 80  # distância entre o dedo indicador e o ombro para mover o personagem
DISTANCE_INDEX_NOSE_THRESHOLD = 50      # distância entre o dedo indicador e o nariz para calibrar a altura do nariz

# Variaveis Globais
jump_nose_height = None                 # altura do nariz para pular
squat_nose_height = None                # altura do nariz para agachar

# Flags
is_jumping = False                      # flag para detectar pulo
is_squatting = False                    # flag para detectar agachamento
key_pressed = False                     # flag para detectar tecla pressionada
key_right_pressed = False               # flag para detectar tecla direita pressionada
key_left_pressed = False                # flag para detectar tecla esquerda pressionada


def press_key_in_background(key, command):
    thread = threading.Thread(target=press_key, args=(key, command,))
    thread.start()


# Pressiona a tecla no programa
def press_key(key, command):
    if command == 'press':
        pydirectinput.keyDown(key)
        time.sleep(0.8)
        pydirectinput.keyUp(key)
    elif command == 'keydown':
        pydirectinput.keyDown(key)
    elif command == 'keyup':
        pydirectinput.keyUp(key)


# Calibra a zona de pulo e agachamento
def calibrate(nose_position):
    global jump_nose_height
    global squat_nose_height
    jump_nose_height = nose_position - JUMP_NOSE_HEIGHT_THRESHOLD
    squat_nose_height = nose_position + SQUAT_NOSE_HEIGHT_THRESHOLD


# Inicialização do mediapipe
video = cv2.VideoCapture(VIDEO_PATH)
pose = mp.solutions.pose
mp_pose = pose.Pose(min_tracking_confidence=0.5, min_detection_confidence=0.5)
mp_draw = mp.solutions.drawing_utils

while True:
    success, img = video.read()
    img = cv2.resize(img, (VIDEO_SIZE[0], VIDEO_SIZE[1]))
    video_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = mp_pose.process(video_rgb)
    points = results.pose_landmarks
    mp_draw.draw_landmarks(img, points, pose.POSE_CONNECTIONS)
    height, width, _ = img.shape

    if points:
        # extração de coordenadas dos pontos
        right_index_y = int(points.landmark[pose.PoseLandmark.RIGHT_INDEX].y * height)
        right_index_x = int(points.landmark[pose.PoseLandmark.RIGHT_INDEX].x * width)
        right_shoulder_y = int(points.landmark[pose.PoseLandmark.RIGHT_SHOULDER].y * height)
        right_shoulder_x = int(points.landmark[pose.PoseLandmark.RIGHT_SHOULDER].x * width)
        left_index_y = int(points.landmark[pose.PoseLandmark.LEFT_INDEX].y * height)
        left_index_x = int(points.landmark[pose.PoseLandmark.LEFT_INDEX].x * width)
        left_shoulder_y = int(points.landmark[pose.PoseLandmark.LEFT_SHOULDER].y * height)
        left_shoulder_x = int(points.landmark[pose.PoseLandmark.LEFT_SHOULDER].x * width)
        nose_y = int(points.landmark[pose.PoseLandmark.NOSE].y * height)
        nose_x = int(points.landmark[pose.PoseLandmark.NOSE].x * width)

        dist_maoDireita_ombro = int(math.hypot(right_index_x - right_shoulder_x, right_index_y - right_shoulder_y))

        # calculo de distâncias entre o dedo indicador direito e o ombro direito.
        dis_right_index_right_shoulder = int(
            math.sqrt((right_index_x - right_shoulder_x) ** 2 + (right_index_y - right_shoulder_y) ** 2))

        # calculo de distâncias entre o dedo indicador esquerdo e o ombro esquerdo.
        dis_left_index_left_shoulder = int(
            math.sqrt((left_index_x - left_shoulder_x) ** 2 + (left_index_y - left_shoulder_y) ** 2))

        # calculo de distâncias entre o dedo indicador direito e o nariz.
        dis_right_index_nose = int(
            math.sqrt((right_index_x - nose_x) ** 2 + (right_index_y - nose_y) ** 2))

        # calculo de distâncias entre o dedo indicador esquerdo e o nariz.
        dis_left_index_nose = int(
            math.sqrt((left_index_x - nose_x) ** 2 + (left_index_y - nose_y) ** 2))

        # calibra o limite de altura do nariz ao colocar a mão direita e esquerda na altura do nariz
        if dis_left_index_nose < DISTANCE_INDEX_NOSE_THRESHOLD and dis_right_index_nose < DISTANCE_INDEX_NOSE_THRESHOLD:
            calibrate(nose_y)

        # Insere a altura do nariz na imagem
        cv2.putText(img, str(nose_y), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Desenha uma linha na altura do nariz
        cv2.line(img, (0, nose_y), (640, nose_y), (0, 255, 0), 1)

        # Calibra o ponto de início do pulo e do agachamento
        if jump_nose_height is None or squat_nose_height is None:
            calibrate(nose_y)

        # desenha uma linha na altura do início do pulo
        cv2.line(img, (0, jump_nose_height), (640, jump_nose_height), (0, 0, 255), 1)
        cv2.putText(img, "Jump Start", (0, jump_nose_height - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

        # desenha uma linha na altura do início do agachamento
        cv2.line(img, (0, squat_nose_height), (640, squat_nose_height), (0, 0, 255), 1)
        cv2.putText(img, "Squat Start", (0, squat_nose_height - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

        # detecta pulo
        if nose_y < jump_nose_height:
            cv2.putText(img, "Jump Detected", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            if is_jumping is False:
                press_key_in_background('c', 'press')
                is_jumping = True
        else:
            is_jumping = False

        # detecta agachamento
        if nose_y > squat_nose_height:
            cv2.putText(img, "Squat Detected", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            if is_squatting is False:
                press_key_in_background('down', 'keydown')
                is_squatting = True
                key_pressed = True

        else:
            if key_pressed:
                press_key_in_background('down', 'keyup')
                key_pressed = False
            is_squatting = False

        # detecta mão direita
        if dis_right_index_right_shoulder < DISTANCE_INDEX_SHOULDER_THRESHOLD:
            if key_right_pressed is False:
                press_key_in_background('right', 'keydown')
                key_right_pressed = True
        else:
            if key_right_pressed:
                if key_right_pressed:
                    press_key_in_background('right', 'keyup')
                key_right_pressed = False

        # detecta mão esquerda
        if dis_left_index_left_shoulder < DISTANCE_INDEX_SHOULDER_THRESHOLD:
            if key_left_pressed is False:
                press_key_in_background('left', 'keydown')
                key_left_pressed = True
        else:
            if key_left_pressed:
                if key_left_pressed:
                    press_key_in_background('left', 'keyup')
                key_left_pressed = False

        # verifica se a tecla 'q' foi pressionada para calibrar a altura do nariz
        if cv2.waitKey(1) & 0xFF == ord('q'):
            calibrate(nose_y)

    cv2.imshow("Image", img)
    cv2.waitKey(10)
