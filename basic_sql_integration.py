# SQL connector installieren
# pip install mysql-connector-python

from flask import Flask, request
import mysql.connector
import os

app = Flask(__name__)

# Datenbankkonfiguration, das was in MariaDB festgelgt wurde
db_config = {
    'user': 'username',
    'password': 'password',
    'host': 'localhost',
    'database': 'pdf_database'
}

def insert_file(name, description, file_data):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    
    query = "INSERT INTO pdf_files (name, description, file_data) VALUES (%s, %s, %s)"
    cursor.execute(query, (name, description, file_data))
    
    conn.commit()
    cursor.close()
    conn.close()

def get_file(file_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    query = "SELECT name, file_data FROM pdf_files WHERE id = %s"
    cursor.execute(query, (file_id,))

    file_data = cursor.fetchone()
    cursor.close()
    conn.close()

    if file_data:
        return file_data
    else:
        return None
    
def create_table():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pdf_files (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            description TEXT,
            file_data LONGBLOB
        );
    """)

    conn.commit()
    cursor.close()
    conn.close()    

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file provided'

    file = request.files['file']
    if file.filename == '':
        return 'No selected file'

    if file and file.filename.endswith('.pdf'):
        file_data = file.read()
        insert_file(file.filename, 'File description', file_data)
        return 'File uploaded & inserted.'

    return 'Invalid file.'

if __name__ == '__main__':
    create_table() # beim startup die Tabelle erstellen, muss ggf. anders gelöst werden (Prüfung ob Table schon existiert oder so)
    app.run(debug=True)
