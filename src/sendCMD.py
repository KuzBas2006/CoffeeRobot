import requests
import json


def send_cmd(cmd):
    # URL робота
    url = "http://192.168.1.101:8080/commands"

    # Отправляем POST запрос с JSON
    try:
        response = requests.post(url, json=cmd, timeout=0.2)

        # Проверяем статус ответа
        if response.status_code == 200:
            print("Успешно отправлено!")
            print("Ответ от C++ сервера:")
            print(json.dumps(response.json(), indent=4, ensure_ascii=False))
        else:
            print(f"Ошибка HTTP {response.status_code}")
            print(response.text)

    except requests.exceptions.ConnectionError:
        print("Ошибка: Не удалось подключиться к C++ серверу. Убедитесь, что он запущен.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")