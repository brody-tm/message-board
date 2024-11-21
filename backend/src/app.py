from flask import Flask, jsonify, request, render_template
from datetime import datetime
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Get all messages
@app.route('/messages', methods=['GET'])
def get_messages():
    conn = get_db_connection()
    messages = conn.execute('SELECT * FROM messages').fetchall()
    conn.close()

    messages_list = [dict(row) for row in messages]
    return render_template('index.html', messages = messages_list)

# Get message by ID
@app.route('/messages/<int:message_id>', methods=['GET'])
def get_message(message_id):
    conn = get_db_connection()
    message = conn.execute(
        'SELECT * FROM messages WHERE id = ?',
        (message_id,)
    ).fetchone()
    conn.close()

    # Check if a message with the given id exists
    if message is None:
        return jsonify({"error": "Message not found"}), 404

    # Convert the result to a dictionary
    message_dict = dict(message)
    return jsonify(message_dict)


# Create new message
@app.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()

    if not data or 'content' not in data:
        return jsonify({"error": "Invalid input. 'content' is required."}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('INSERT INTO messages (content) VALUES (?)', (data['content'],))
    conn.commit()

    new_message_id = cursor.lastrowid
    conn.close()

    new_message = {
        "id": new_message_id,
        "content": data['content']
    }
    return jsonify(new_message), 201

# Update message by ID
@app.route('/messages/<int:message_id>', methods=['PUT'])
def update_message(message_id):
    data = request.get_json()

    if not data or 'content' not in data:
        return jsonify({"error": "Invalid input. 'content' is required."}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('UPDATE messages SET content = ? WHERE id = ?', (data['content'], message_id))
    conn.commit()

    conn.close()

    new_message = {
        "id": message_id,
        "content": data['content']
    }
    return jsonify(new_message), 201

# Delete message by ID
@app.route('/messages/<int:message_id>', methods=['DELETE'])
def delete_message(message_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('DELETE FROM messages WHERE id = ?', (message_id,))
    conn.commit()

    conn.close()

    new_message = {
        "id": message_id,
        "message": 'message deleted'
    }
    return jsonify(new_message), 201

if __name__ == '__main__':
    app.run(debug=True)
