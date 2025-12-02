from flask import Flask, Response, jsonify
import requests
import sqlite3
from datetime import datetime
import hashlib
import base64

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('cats.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            image_hash TEXT UNIQUE,
            image_data BLOB,
            created_at TEXT,
            last_called_at TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/api/cat', methods=['GET'])
def get_cat():
    response = requests.get('https://cataas.com/cat')
    image_data = response.content
    image_hash = hashlib.md5(image_data).hexdigest()
    now = datetime.now().isoformat()
    
    conn = sqlite3.connect('cats.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT id FROM images WHERE image_hash = ?', (image_hash,))
    existing = cursor.fetchone()
    
    if existing:
        cursor.execute('UPDATE images SET last_called_at = ? WHERE image_hash = ?', (now, image_hash))
    else:
        cursor.execute(
            'INSERT INTO images (image_hash, image_data, created_at, last_called_at) VALUES (?, ?, ?, ?)',
            (image_hash, image_data, now, now)
        )
    
    conn.commit()
    conn.close()
    
    return Response(image_data, mimetype='image/png')

@app.route('/api/count', methods=['GET'])
def get_count():
    conn = sqlite3.connect('cats.db')
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM images')
    count = cursor.fetchone()[0]
    conn.close()
    return jsonify({'total_images': count})

@app.route('/api/image/<int:id>', methods=['GET'])
def get_image(id):
    conn = sqlite3.connect('cats.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT image_data, created_at, last_called_at FROM images WHERE id = ?', (id,))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        return jsonify({'error': 'Imagen no encontrada'}), 404
    
    return jsonify({
        'id': id,
        'created_at': row[1],
        'last_called_at': row[2]
    })

@app.route('/api/delete/<int:id>', methods=['DELETE'])
def delete_img(id):
    conn = sqlite3.connect('cats.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT id FROM images WHERE id = ?', (id,))
    existing = cursor.fetchone()
    
    if not existing:
        conn.close()
        return jsonify({'error': 'Imagen no encontrada'}), 404
    
    cursor.execute('DELETE FROM images WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Imagen eliminada'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
