import json
from src.sendCMD import send_cmd

# Глобальные переменные
state = "ready"

# Конфигурация
MIN_ANGLE = 10.0
MIN_DISTANCE = 20.0


def process_state(json_input):
    global state

    # Парсим JSON
    data = json.loads(json_input)
    angle = data['angle']
    distance = data['distance']

    # Состояние 1: Проверка угла
    if angle > MIN_ANGLE:
        cmd = {
            "ROTATE": angle
        }
        send_cmd(cmd)
        #print(cmd)

    # Состояние 2: Проверка дистанции
    if distance > MIN_DISTANCE:
        cmd = {
            "MOVE" :distance
        }
        send_cmd(cmd)
        #print(cmd)

    # Сбрасываем состояние
    state = "ready"
    return 0
