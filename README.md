Telegram bot for reading books
----

**Цель:** Создать tg bot, с помощью которого можно будет читать книги не покидая мессенджер

**Возможности:**
- Загрузка книг в формате PDF
- Выбор книги для чтения из ранее загруженных
- Навигация по страницам
- Отображение изображений из книг
- Создание заметок

#### Зависимости

- PostgreSQL
- MinIO

> В папке ```/docker-compose``` находятся файлы для развертывания зависимостей с помощью Docker

#### Запуск

    cp .env_template .env # заполнить своими значениями

    source .venv/bin/activate

    pip install -r requirements.txt
    pip install PyMuPDF==1.23.6

    export $(cat .env)
    python -m Database.model # Create db 

    python -m GUI.TelegramEngine
