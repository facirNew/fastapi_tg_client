# FastAPI Telegram Client


## Описание

Проект **FastAPI Telegram Client** предоставляет API для взаимодействия с Telegram через веб-интерфейс, используя FastAPI. Этот клиент может быть использован для отправки сообщений и управления ботами в Telegram.

## Функционал

- Отправка сообщений в чаты Telegram
- Получение обновлений от бота
- Управление ботами
- Легкий в использовании REST API интерфейс


## Установка

1. Клонируйте репозиторий:
    ```bash
    git clone https://github.com/facirNew/fastapi_tg_client.git
    cd fastapi_tg_client
    ```

2. Для конфигурации параметров создайте файл `.env` в корне проекта на основе .env.example

3. Создайте и активируйте виртуальное окружение:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Для Windows используйте `venv\Scripts\activate`
    ```

4. Установите зависимости:
    ```bash
    pip install -r requirements.txt
    ```

## Использование

1. Запустите FastAPI приложение:
    ```bash
    uvicorn main:app
    ```

2. Откройте в браузере `http://127.0.0.1:8000/docs` для доступа к автоматической документации Swagger UI.


## Запуск через Docker

1. Клонируйте репозиторий:
    ```bash
    git clone https://github.com/facirNew/fastapi_tg_client.git
    cd fastapi_tg_client
    ```
2. Запустите docker compose:
    ```bash
    docker compose up -d
    ```
3. Откройте в браузере `http://127.0.0.1:8000/docs` для доступа к автоматической документации Swagger UI.

