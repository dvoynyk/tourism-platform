#!/bin/sh
echo "=== Проверка баз данных SQLite ==="

# Проверка базы данных туров
echo "Проверка /dbdata/tours.db..."
if [ ! -f "/dbdata/tours.db" ]; then
    echo "ОШИБКА: Файл /dbdata/tours.db не найден!"
    exit 1
fi

result_tours=$(sqlite3 /dbdata/tours.db "SELECT EXISTS (SELECT * FROM sqlite_master WHERE type='table' AND name='tours');")
if [ "$result_tours" -eq 1 ]; then
    echo " Таблица 'tours' успешно найдена!"
else
    echo "ОШИБКА: Таблица 'tours' отсутствует в tours.db!"
    exit 1
fi

# Проверка базы данных бронирований
echo "Проверка /dbdata/bookings.db..."
if [ ! -f "/dbdata/bookings.db" ]; then
    echo "ОШИБКА: Файл /dbdata/bookings.db не найден!"
    exit 1
fi

result_bookings=$(sqlite3 /dbdata/bookings.db "SELECT EXISTS (SELECT * FROM sqlite_master WHERE type='table' AND name='bookings');")
if [ "$result_bookings" -eq 1 ]; then
    echo " Таблица 'bookings' успешно найдена!"
else
    echo "ОШИБКА: Таблица 'bookings' отсутствует в bookings.db!"
    exit 1
fi

echo "=== Все базы данных исправны и готовы к работе ==="
exit 0