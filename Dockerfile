# Интерпритатор python
FROM python:3.12

# Устанавливаем необходимые системные зависимости
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get clean

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта в контейнер
COPY main.py .
COPY src /app/src
COPY templates /app/templates

# Устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Команда для запуска приложения
CMD ["python3", "main.py"]