import pandas as pd
import random

# Чтение данных из файлов
with open("safe_queries.txt", "r") as safe_file:
    safe_queries = [line.strip() for line in safe_file if line.strip()]  # Убираем пустые строки

with open("xss_queries.txt", "r") as xss_file:
    xss_queries = [line.strip() for line in xss_file if line.strip()]  # Убираем пустые строки

# Создаем список данных
data = [{"text": query, "label": 0} for query in safe_queries] + \
       [{"text": query, "label": 1} for query in xss_queries]

# Перемешиваем данные
random.shuffle(data)

# Создаем DataFrame
df = pd.DataFrame(data)

# Сохраняем в CSV
df.to_csv("data.csv", index=False)

print("Файл data.csv успешно создан!")
