import json
import time

from src.sendCMD import send_cmd

# Глобальные переменные
state = "ready"

# Конфигурация
MIN_ANGLE = 10.0
MIN_DISTANCE = 50.0
ANGLE_K = 5.0
FORWARD_DUR = 400.0


def process_state(json_input):
    global state

    # Парсим JSON
    data = json.loads(json_input)
    angle = data['angle']
    distance = data['distance']

    # Состояние 1: Проверка угла
    if abs(angle) > MIN_ANGLE:
        if angle > 0:
            cmd = {
                "command": "RIGHT/ms",
                "duration": angle * ANGLE_K
            }
        else:
            cmd = {
                "command": "LEFT/ms",
                "duration": abs(angle) * ANGLE_K
            }
        send_cmd(cmd)
        state = "rotating"
        return None


    # Состояние 2: Проверка дистанции
    if distance > MIN_DISTANCE:
        cmd = {
            "command": "FORWARD/ms",
            "duration": FORWARD_DUR
        }
        send_cmd(cmd)
        state = "moving"
    else:
        cmd = {
            "command": "STOP",
            "duration": 0
        }
        send_cmd(cmd)

    # Сбрасываем состояние
    state = "ready"
    return 0
