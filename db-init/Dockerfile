FROM alpine:latest

# Устанавливаем sqlite и bash
RUN apk add --no-cache sqlite bash

# Переходим в рабочую папку /app внутри контейнера
WORKDIR /app

# Копируем скрипт в папку /app (чтобы volume его не стирал)
COPY check-db.sh /app/check-db.sh
RUN chmod +x /app/check-db.sh

# Запускаем скрипт проверки
CMD ["/app/check-db.sh"]