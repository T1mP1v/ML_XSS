import random
import json
import urllib.parse

# Примеры XSS-атак
def load_file(file_path):
    with open(file_path, 'r') as file:
        payloads = [line.strip() for line in file if line.strip()]
    return payloads

xss_payloads = load_file("XSS-payloadbox.txt")
# Пути для запросов
paths = load_file("directory-list-2.3-small.txt")
params = load_file("burp-parameter-names.txt")

def generate_get_requests(num_requests):
    requests = []
    
    for _ in range(num_requests):
        # Выбираем случайный payload из списка
        payload = random.choice(xss_payloads)
        # Кодируем payload в URL
        encoded_payload = urllib.parse.quote(payload)
        
        # Создаем GET-запрос с закодированным payload
        request = f"/{random.choice(paths)}?{random.choice(params)}={encoded_payload}"
        requests.append(request)
    
    return requests

# Генерация GET-запросов
num_get_queries = 5000

get_requests = generate_get_requests(num_get_queries)

#Сохранение в файл строками
with open("xss_dataset.txt", "w") as file:
    for request in get_requests:
        file.write(request + "\n")

print(f"Сгенерировано  запросов (GET и POST), сохранено в 'xss_dataset.json'.")
