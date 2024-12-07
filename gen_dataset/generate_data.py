import pandas as pd
import random

# Путь к данным
safe_file_path = "safe_queries.txt"
xss_file_path = "xss_dataset.txt"

# Чтение содержимого файлов
with open(safe_file_path, "r") as safe_file:
    safe_queries = [line.strip() for line in safe_file if line.strip()]

with open(xss_file_path, "r") as xss_file:
    xss_queries = [line.strip() for line in xss_file if line.strip()]

# Создание списка данных с метками
data = [{"text": query, "label": 0} for query in safe_queries] + \
       [{"text": query, "label": 1} for query in xss_queries]

# Перемешивание данных
random.shuffle(data)

# Создаем DataFrame
df = pd.DataFrame(data)

# Сохраняем в CSV
df.to_csv("data.csv", index=False)

print("Файл data.csv успешно создан!")
