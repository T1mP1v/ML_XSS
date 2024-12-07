import re
import time
from joblib import load
from sklearn.feature_extraction.text import TfidfVectorizer
import os

print('''
██╗  ██╗███████╗███████╗         █████╗ ███╗   ██╗ █████╗ ██╗     ██╗███████╗ █████╗ ████████╗ ██████╗ ██████╗ 
╚██╗██╔╝██╔════╝██╔════╝        ██╔══██╗████╗  ██║██╔══██╗██║     ██║╚══███╔╝██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗
 ╚███╔╝ ███████╗███████╗        ███████║██╔██╗ ██║███████║██║     ██║  ███╔╝ ███████║   ██║   ██║   ██║██████╔╝
 ██╔██╗ ╚════██║╚════██║        ██╔══██║██║╚██╗██║██╔══██║██║     ██║ ███╔╝  ██╔══██║   ██║   ██║   ██║██╔══██╗
██╔╝ ██╗███████║███████║███████╗██║  ██║██║ ╚████║██║  ██║███████╗██║███████╗██║  ██║   ██║   ╚██████╔╝██║  ██║
╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝╚═╝╚══════╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝''')

# Загрузка предобученной модели и векторизатора
try:
    model = load("xss_detection_model.joblib")
    vectorizer = load("tfidf_vectorizer.joblib")
    print("Модель и векторизатор успешно загружены.")
except Exception as e:
    print(f"Ошибка загрузки модели: {e}")
    exit()

# Путь к лог-файлу сервера
LOG_FILE_PATH = "/var/www/html/xss/access.log"  # Укажите путь к вашему лог-файлу

# Регулярное выражение для парсинга логов (например, для Nginx)
LOG_REGEX = r'(?P<ip>(?:[\d\.]+|[a-fA-F0-9:]+)) - - \[(?P<datetime>[^\]]+)] "(?P<method>[A-Z]+) (?P<url>[^\s]+) HTTP/[\d.]+" (?P<status>\d{3}) [\d-]+ "(?P<referrer>[^"]*)" "(?P<user_agent>[^"]*)"'

# Функция для определения XSS
def detect_xss(query):
    query_tfidf = vectorizer.transform([query])
    prediction = model.predict(query_tfidf)
    return prediction[0] == 1  # 1 означает XSS

# Функция для обработки логов
def analyze_logs():
    print(f"📂 Открываем лог-файл: {LOG_FILE_PATH}")
    
    # Проверим, существует ли лог-файл
    if not os.path.exists(LOG_FILE_PATH):
        print(f"Ошибка: Лог-файл {LOG_FILE_PATH} не найден!")
        return

    with open(LOG_FILE_PATH, "r") as logfile:
        logfile.seek(0, os.SEEK_END)  # Переходим в конец файла

        print("⏳ Ожидание новых запросов...")
        try:
            while True:
                line = logfile.readline()
                if not line:
                    time.sleep(1)  # Ждем появления новых строк
                    continue

                # Парсим строку лога
                # print(f"Чтение строки лога: {line.strip()}")
                match = re.match(LOG_REGEX, line)
                if match:
                    log_data = match.groupdict()
                    request_query = f"{log_data['method']} {log_data['url']}"
                    ##print(request_query)
                    # Проверка на XSS
                    if detect_xss(request_query):
                        print(f'''\n⚠️ Обнаружена XSS-атака!\nIP: {log_data['ip']}\nДата и время: {log_data['datetime']}\nЗапрос: {request_query}\nUser-Agent: {log_data['user_agent']}''')
                        my_file = open("xss_log.txt", "w")
                        my_file.write(f'''\n⚠️ Обнаружена XSS-атака!\nIP: {log_data['ip']}\nДата и время: {log_data['datetime']}\nЗапрос: {request_query}\nUser-Agent: {log_data['user_agent']}''')
                        my_file.close()
                else:
                    print(f"Не удалось обработать строку: {line.strip()}")

        except KeyboardInterrupt:
            print("\n🚪 Завершение работы.")

# Запуск анализа логов
analyze_logs()
