import json
import sqlite3

def load_data(filename):
    with open(f'static/data/{filename}', 'r', encoding='utf-8') as arquivo:
        return json.load(arquivo)


def load_template(filename):
    with open(f'static/templates/{filename}', 'r', encoding='utf-8') as arquivo:
        return arquivo.read()

def save_data(filename, data):
    with open('static/data/' + filename, 'w', encoding='utf-8') as arquivo:
        json.dump(data, arquivo, ensure_ascii=False, indent=2)

def create_database():
    connection = sqlite3.connect('banco.db')
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS note (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            content TEXT
        )
    ''')

    try:
        cursor.execute(
            'ALTER TABLE note ADD COLUMN favorite INTEGER DEFAULT 0'
        )
    except sqlite3.OperationalError:
        pass

    connection.commit()
    connection.close()

def load_notes():
    connection = sqlite3.connect('banco.db')
    cursor = connection.cursor()

    cursor.execute(
        'SELECT id, title, content, favorite FROM note ORDER BY favorite DESC, id ASC'
    )

    notes = cursor.fetchall()

    connection.close()

    return notes

def add_note(titulo, detalhes):
    connection = sqlite3.connect('banco.db')
    cursor = connection.cursor()

    cursor.execute(
        'INSERT INTO note (title, content) VALUES (?, ?)',
        (titulo, detalhes)
    )

    connection.commit()
    connection.close()
def delete_note(id):
    connection = sqlite3.connect('banco.db')
    cursor = connection.cursor()

    cursor.execute(
        'DELETE FROM note WHERE id = ?',
        (id,)
    )

    connection.commit()
    connection.close()
def get_note(id):
    connection = sqlite3.connect('banco.db')
    cursor = connection.cursor()

    cursor.execute(
        'SELECT id, title, content FROM note WHERE id = ?',
        (id,)
    )

    note = cursor.fetchone()

    connection.close()

    return note


def update_note(id, titulo, detalhes):
    connection = sqlite3.connect('banco.db')
    cursor = connection.cursor()

    cursor.execute(
        'UPDATE note SET title = ?, content = ? WHERE id = ?',
        (titulo, detalhes, id)
    )

    connection.commit()
    connection.close()


def favorite_note(id):
    connection = sqlite3.connect('banco.db')
    cursor = connection.cursor()

    cursor.execute(
        '''
        UPDATE note
        SET favorite = CASE
            WHEN favorite = 0 THEN 1
            ELSE 0
        END
        WHERE id = ?
        ''',
        (id,)
    )

    connection.commit()
    connection.close()
