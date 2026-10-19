import sqlite3
import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DB_PATH = os.path.join('/app', 'db', 'bookings.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    return conn

@app.route('/api/booking', methods=['POST'])
def create_booking():
    data = request.get_json()

    if not data or not data.get('tour_id') or not data.get('user_name') or not data.get('phone'):
        return jsonify({'error': 'Не заполнены обязательные поля'}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO bookings (tour_id, user_name, phone, email, travel_date, guests_count)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            data.get('tour_id'),
            data.get('user_name'),
            data.get('phone'),
            data.get('email', ''),
            data.get('travel_date', ''),
            data.get('guests_count', 1)
        ))

        booking_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return jsonify({
            'status': 'success',
            'message': 'Бронирование успешно создано',
            'booking_id': booking_id
        }), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)