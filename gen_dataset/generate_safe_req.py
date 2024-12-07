import random
import json

# Примеры безопасных параметров
params = [
    "book", "shoes", "electronics", "laptop", "phone", 
    "apple", "banana", "category1", "username1", "password123",
    "query", "search_term", "action1", "value1"
]
# Пути для запросов
paths = ["/order", "/search", "/cart", "/checkout", "/login", "/products", "/wishlist", "/api"]

params_value = ["123","shoes","2","price_desc","color:red","laptop","electronics","add_to_cart","admin","abc123xyz"]


def generate_safe_get_requests(num_queries):
    """Генерация безопасных GET-запросов."""
    queries = []
    for _ in range(num_queries):
        path = random.choice(paths)
        param = random.choice(params)
        param_value = random.choice(params_value)
        # Формируем безопасный GET-запрос
        if random.random() < 0.5:
            query = f"{path}?{param}={params_value}"
    return queries



safe_get_requests = generate_safe_get_requests(1000)

# Сохранение в файл txt
with open("safe_dataset.txt", "w") as file:
    json.dump(safe_get_requests, file, indent=4)

print(f"Сгенерировано {len(safe_get_requests)} безопасных запросов (GET и POST), сохранено в 'safe_dataset.json'.")
