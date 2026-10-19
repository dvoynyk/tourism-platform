import sqlite3
import os

# Создаем папку db-init/db, если ее еще нет
os.makedirs('db-init/db', exist_ok=True)

# -------------------------------------------------------------
# 1. СОЗДАНИЕ И НАПОЛНЕНИЕ БАЗЫ ДАННЫХ ТУРОВ (tours.db)
# -------------------------------------------------------------
tours_db_path = os.path.join('db-init', 'db', 'tours.db')
conn_tours = sqlite3.connect(tours_db_path)
cursor_tours = conn_tours.cursor()

# Создаем таблицу
cursor_tours.execute('''
CREATE TABLE IF NOT EXISTS tours (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    price INTEGER NOT NULL,
    stars INTEGER NOT NULL DEFAULT 5,
    image TEXT NOT NULL
)
''')

# Проверяем, есть ли уже данные, чтобы не дублировать
cursor_tours.execute("SELECT COUNT(*) FROM tours")
if cursor_tours.fetchone()[0] == 0:
    tours_data = [
        ('Турция, Анталия', 'Всё включено, 7 ночей, 5-звёздочный отель на первой линии.', 45000, 5, 'images/tour1.jpg'),
        ('Италия, Рим', 'Экскурсионный тур, 5 ночей, завтраки, перелёт включён.', 62000, 4, 'images/tour2.png'),
        ('Египет, Шарм-эль-Шейх', 'Рай для дайверов, 10 ночей, всё включено, коралловый риф.', 52000, 5, 'images/tour3.png'),
        ('Россия, Алтай', 'Активный отдых, 7 ночей, конные прогулки, перелёт и гид включены.', 38000, 4, 'images/tour4.png'),
        ('ОАЭ, Дубай', 'Роскошный отдых, 6 ночей, отель с видом на небоскребы, завтраки.', 75000, 5, 'images/tour5.png'),
        ('США','Тур 7 дней по северо-восточному побережью США: более 11 городов и Ниагарский водопад', 155000, 4.5 ,'images/tour6.png')
    ]
    cursor_tours.executemany('''
    INSERT INTO tours (title, description, price, stars, image)
    VALUES (?, ?, ?, ?, ?)
    ''', tours_data)
    print(" База данных tours.db успешно создана и заполнена 6 турами!")

conn_tours.commit()
conn_tours.close()


# -------------------------------------------------------------
# 2. СОЗДАНИЕ БАЗЫ ДАННЫХ БРОНИРОВАНИЙ (bookings.db)
# -------------------------------------------------------------
bookings_db_path = os.path.join('db-init', 'db', 'bookings.db')
conn_bookings = sqlite3.connect(bookings_db_path)
cursor_bookings = conn_bookings.cursor()

# Создаем пустую таблицу бронирований
cursor_bookings.execute('''
CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tour_id INTEGER NOT NULL,
    user_name TEXT NOT NULL,
    phone TEXT NOT NULL,
    email TEXT,
    travel_date TEXT NOT NULL,
    guests_count INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

print(" База данных bookings.db успешно создана!")

conn_bookings.commit()
conn_bookings.close()