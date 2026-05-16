import json
import time

from src.sendCMD import send_cmd

# Глобальные переменные
state = "ready"

# Конфигурация
MIN_ANGLE = 10.0
MIN_DISTANCE =15.0


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
                "RIGHT": angle
            }
        else:
            cmd = {
                "LEFT": abs(angle)
            }
        send_cmd(cmd)
        time.sleep(abs(angle) // 45)
        state = "rotating"
        return None



    # Состояние 2: Проверка дистанции
    if distance > MIN_DISTANCE:
        cmd = {
            "MOVE": distance
        }
        send_cmd(cmd)
        time.sleep(1)
        state = "moving"

    # Сбрасываем состояние
    state = "ready"
    return 0
