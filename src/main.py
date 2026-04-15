import requests
import json

# URL C++ сервера
url = "http://localhost:8080/api/data"

# Формируем JSON сообщение
data = {
    "message": "Привет",
    "value": 42,
    "items": ["один", "два", "три"]
}

# Отправляем POST запрос с JSON
try:
    response = requests.post(url, json=data)

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