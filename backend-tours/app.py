import sqlite3
import os
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DB_PATH = os.path.join('/app', 'db', 'tours.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/tours', methods=['GET'])
def get_tours():
    # Получаем поисковый запрос из URL (например, /api/tours?search=Алтай)
    search_query = request.args.get('search', '').strip()

    try:
        conn = get_db_connection()

        if search_query:
            # SQL-поиск по названию туров и описанию (без учета регистра)
            sql = "SELECT * FROM tours WHERE title LIKE ? OR description LIKE ?"
            param = f"%{search_query}%"
            tours_raw = conn.execute(sql, (param, param)).fetchall()
        else:
            # Если поиск пустой — отдаем все туры
            tours_raw = conn.execute('SELECT * FROM tours').fetchall()

        conn.close()

        tours = []
        for tour in tours_raw:
            tours.append({
                'id': tour['id'],
                'title': tour['title'],
                'description': tour['description'],
                'price': tour['price'],
                'stars': tour['stars'],
                'image': tour['image']
            })

        return jsonify(tours), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)