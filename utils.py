# ---------------------------------------------------------------
# utils.py  ->  Funções "ajudantes": ler arquivos e conversar com o BANCO DE DADOS.
# É aqui que as notas são realmente guardadas/lidas (CRUD: Create, Read, Update, Delete).
# ---------------------------------------------------------------

import json      # biblioteca para ler/escrever arquivos .json
import sqlite3   # biblioteca para usar o SQLite (banco de dados que vive num arquivo só: banco.db)

# ---- Funções de ARQUIVOS (as duas primeiras são de JSON; a app atual usa o banco) ----

def load_data(filename):
    # open(caminho, 'r') abre para Leitura (r = read). encoding='utf-8' entende acentos (ç, ã...).
    # f'...{filename}' = f-string: coloca o valor da variável dentro do texto.
    # "with ... as arquivo" abre o arquivo e FECHA sozinho no final (mesmo se der erro).
    with open(f'static/data/{filename}', 'r', encoding='utf-8') as arquivo:
        # json.load transforma o texto JSON em lista/dicionário do Python.
        return json.load(arquivo)


def load_template(filename):
    # Abre um arquivo HTML de static/templates/ para leitura.
    with open(f'static/templates/{filename}', 'r', encoding='utf-8') as arquivo:
        # .read() devolve o arquivo inteiro como um único texto.
        return arquivo.read()

def save_data(filename, data):
    # 'w' = write (escrever). CUIDADO: apaga o que tinha antes e escreve de novo.
    # Aqui a pasta é juntada com + (outra forma de montar o texto, igual ao f'').
    with open('static/data/' + filename, 'w', encoding='utf-8') as arquivo:
        # json.dump grava a lista/dicionário como JSON no arquivo.
        # ensure_ascii=False = mantém acentos; indent=2 = deixa bonito e identado.
        json.dump(data, arquivo, ensure_ascii=False, indent=2)

# ---- Funções do BANCO DE DADOS (SQLite) ----
# Padrão de TODAS elas:
#   1) connect  -> abre a conexão com o arquivo banco.db
#   2) cursor   -> cria o "cursor" (o objeto que executa comandos SQL)
#   3) execute  -> manda o comando SQL
#   4) commit   -> SALVA de verdade (só necessário se mudou dados: INSERT/UPDATE/DELETE)
#   5) close    -> fecha a conexão

def create_database():
    # Abre (ou cria, se não existir) o arquivo banco.db.
    connection = sqlite3.connect('banco.db')
    # Cursor = "a caneta" que escreve os comandos SQL no banco.
    cursor = connection.cursor()

    # Comando SQL, escrito entre ''' ''' (aspas triplas permitem várias linhas).
    # CREATE TABLE IF NOT EXISTS note = cria a tabela "note" SÓ SE ainda não existir (não dá erro se já existe).
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS note (
            id INTEGER PRIMARY KEY AUTOINCREMENT,   -- número inteiro, identifica cada nota, cresce sozinho (1,2,3...)
            title TEXT,                             -- coluna do título (texto)
            content TEXT                            -- coluna do conteúdo (texto)
        )
    ''')

    # Salva a alteração no banco.
    connection.commit()
    # Fecha a conexão.
    connection.close()

def load_notes():
    connection = sqlite3.connect('banco.db')
    cursor = connection.cursor()

    # SELECT = "me mostre". Pede as colunas id, title, content de TODAS as linhas da tabela note.
    cursor.execute('SELECT id, title, content FROM note')
    # fetchall() = pega TODOS os resultados: lista de tuplas [(1,'a','b'), (2,'c','d')].
    notes = cursor.fetchall()

    # SELECT não muda nada, então não precisa de commit.
    connection.close()

    # Devolve a lista para quem chamou (views.index).
    return notes

def add_note(titulo, detalhes):
    connection = sqlite3.connect('banco.db')
    cursor = connection.cursor()

    cursor.execute(
        # INSERT INTO = "adicione uma linha". Os ? são espaços reservados, preenchidos pela tupla abaixo.
        # Não é preciso informar o id: o AUTOINCREMENT cria sozinho.
        'INSERT INTO note (title, content) VALUES (?, ?)',
        # 1º ? = titulo, 2º ? = detalhes. Usar ? (em vez de colar texto) evita "SQL Injection" (ataque).
        (titulo, detalhes)
    )

    # INSERT muda o banco -> precisa de commit para salvar.
    connection.commit()
    connection.close()
def delete_note(id):
    connection = sqlite3.connect('banco.db')
    cursor = connection.cursor()

    cursor.execute(
        # DELETE FROM = apaga linhas. WHERE id = ? = SÓ a linha com esse id (sem WHERE apagaria TUDO!).
        'DELETE FROM note WHERE id = ?',
        # (id,) tem vírgula porque é uma tupla de UM item. Sem a vírgula seria só um número, e daria erro.
        (id,)
    )

    connection.commit()
    connection.close()
def get_note(id):
    connection = sqlite3.connect('banco.db')
    cursor = connection.cursor()

    cursor.execute(
        # Busca só a nota cujo id é o informado.
        'SELECT id, title, content FROM note WHERE id = ?',
        (id,)
    )

    # fetchone() = pega SÓ UMA linha (uma tupla (id, title, content)) ou None se não achar.
    note = cursor.fetchone()

    connection.close()

    return note


def update_note(id, titulo, detalhes):
    connection = sqlite3.connect('banco.db')
    cursor = connection.cursor()

    cursor.execute(
        # UPDATE = altera linhas existentes. SET = quais colunas mudam. WHERE = qual linha.
        'UPDATE note SET title = ?, content = ? WHERE id = ?',
        # A ORDEM da tupla segue a ordem dos ? : título, conteúdo, id.
        (titulo, detalhes, id)
    )

    connection.commit()
    connection.close()

# Esta linha fica FORA de qualquer função: roda uma vez, assim que o utils.py é importado
# (ou seja, quando o servidor liga). Garante que a tabela note existe antes de usá-la.
create_database()
