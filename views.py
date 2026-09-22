# ---------------------------------------------------------------
# views.py  ->  Monta as PÁGINAS (o HTML) e repassa as ordens ao banco.
# Fica no meio: servidor.py chama views.py, e views.py chama utils.py.
#   servidor.py (recebe pedido) -> views.py (monta página) -> utils.py (fala com banco/arquivos)
# ---------------------------------------------------------------

# Traz 6 funções do utils.py. Os parênteses só permitem escrever em várias linhas.
from utils import (
    load_template,   # lê um arquivo HTML e devolve como texto
    load_notes,      # busca TODAS as notas no banco
    add_note,        # cria uma nota
    delete_note,     # apaga uma nota
    get_note,        # busca UMA nota pelo id
    update_note      # altera uma nota
)

def index():
    # Lê o "molde" de UMA nota (static/templates/components/note.html). Vira um texto com buracos {id}, {title}, {details}.
    note_template = load_template('components/note.html')

    # "List comprehension": cria uma lista repetindo uma conta para cada item.
    # Para cada 'dados' (uma nota do banco) preenche o molde.
    notes_li = [
        # .format(...) troca os buracos {id}, {title}, {details} pelos valores reais.
        note_template.format(
    id=dados[0],        # posição 0 da tupla = id da nota
    title=dados[1],     # posição 1 = título
    details=dados[2]    # posição 2 = conteúdo/detalhes
)
        # load_notes() devolve algo como [(1,'titulo','texto'), (2,'...','...')]. Cada tupla vira 'dados'.
        for dados in load_notes()
    ]

    # '\n'.join(lista) cola todos os pedaços da lista em UM texto, separados por quebra de linha.
    notes = '\n'.join(notes_li)

    # Lê index.html e troca o buraco {notes} pelo texto com todas as notas. Devolve o HTML completo.
    return load_template('index.html').format(notes=notes)

def submit(titulo, detalhes):
    # Só repassa ao utils.py: cria a nota no banco.
    add_note(titulo, detalhes)

def delete(id):
    # Só repassa: apaga a nota com esse id.
    delete_note(id)

def edit(id):
    # Busca a nota no banco. Vem como tupla (id, title, content).
    note = get_note(id)

    # Lê update.html e preenche os buracos com os dados atuais da nota (formulário já vem preenchido).
    return load_template('update.html').format(
        id=note[0],
        title=note[1],
        details=note[2]
    )


def update(id, titulo, detalhes):
    # Só repassa: grava as alterações no banco.
    update_note(id, titulo, detalhes)
