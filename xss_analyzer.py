import re
import time
from joblib import load
from sklearn.feature_extraction.text import TfidfVectorizer
import os
from enum import Enum
import logging
import random

os_windows = (os.name == 'nt')

HEADER = '''
██╗  ██╗███████╗███████╗         █████╗ ███╗   ██╗ █████╗ ██╗     ██╗███████╗ █████╗ ████████╗ ██████╗ ██████╗ 
╚██╗██╔╝██╔════╝██╔════╝        ██╔══██╗████╗  ██║██╔══██╗██║     ██║╚══███╔╝██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗
 ╚███╔╝ ███████╗███████╗        ███████║██╔██╗ ██║███████║██║     ██║  ███╔╝ ███████║   ██║   ██║   ██║██████╔╝
 ██╔██╗ ╚════██║╚════██║        ██╔══██║██║╚██╗██║██╔══██║██║     ██║ ███╔╝  ██╔══██║   ██║   ██║   ██║██╔══██╗
██╔╝ ██╗███████║███████║███████╗██║  ██║██║ ╚████║██║  ██║███████╗██║███████╗██║  ██║   ██║   ╚██████╔╝██║  ██║
╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝╚═╝╚══════╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝'''
class Style(Enum):
    """
    Bash escape sequences, see:
    https://misc.flogisoft.com/bash/tip_colors_and_formatting
    """
    BOLD = 1
    FG_BLACK = 30
    FG_RED = 31
    FG_GREEN = 32
    FG_YELLOW = 33
    FG_BLUE = 34
    FG_MAGENTA = 35
    FG_CYAN = 36
    FG_LIGHT_GRAY = 37

BRIGHT_COLORS = [Style.FG_RED, Style.FG_GREEN, Style.FG_BLUE,
                 Style.FG_MAGENTA, Style.FG_CYAN]

VERBOSE_LINES = 5
def highlight(text, style=None):
    if os_windows:
        return text

    if style is None:
        style = [Style.BOLD, random.choice(BRIGHT_COLORS)]
    return '\033[{}m'.format(';'.join(str(item.value) for item in style)) + text + '\033[0m'
log_format = '%(asctime)s {} %(message)s'.format(highlight('%(levelname)s', [Style.FG_YELLOW]))
logging.basicConfig(format=log_format, datefmt='%H:%M:%S', level=logging.DEBUG)
print(highlight(HEADER))
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
