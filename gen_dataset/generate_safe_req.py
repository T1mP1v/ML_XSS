import random

def load_file(file_path):
    with open(file_path, 'r') as file:
        payloads = [line.strip() for line in file if line.strip()]
    return payloads

# Пути для запросов
paths = load_file("directory-list-2.3-small.txt")
params = load_file("burp-parameter-names.txt")
num_queries = 10000

def generate_safe_get_requests(num_queries):
    """Генерация безопасных GET-запросов."""
    queries = []
    for _ in range(num_queries):
        path = random.choice(paths)
        param = random.choice(params)
        # Формируем безопасный GET-запрос
        if random.random() < 0.5:
            query = f"/{path}?{param}={param}"  # Исправлено на param вместо params
            queries.append(query)
    return queries

safe_get_requests = generate_safe_get_requests(num_queries)

# Сохранение в файл txt
with open("safe_dataset.txt", "w") as file:
    for request in safe_get_requests:
        file.write(request + "\n")  # Записываем каждую строку в файл

print(f"Сгенерировано {len(safe_get_requests)} безопасных запросов (GET), сохранено в 'safe_dataset.txt'.")