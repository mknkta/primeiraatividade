from utils import (
    load_template,
    load_notes,
    add_note,
    delete_note,
    get_note,
    update_note,
    favorite_note
)

def index():
    note_template = load_template('components/note.html')

    notes_li = [
    note_template.format(
        id=dados[0],
        title=dados[1],
        details=dados[2],
        star='★' if dados[3] else '☆'
    )
    for dados in load_notes()
]

    notes = '\n'.join(notes_li)

    return load_template('index.html').format(notes=notes)

def submit(titulo, detalhes):
    add_note(titulo, detalhes)

def delete(id):
    delete_note(id)

def edit(id):
    note = get_note(id)

    return load_template('update.html').format(
        id=note[0],
        title=note[1],
        details=note[2]
    )


def update(id, titulo, detalhes):
    update_note(id, titulo, detalhes)

def favorite(id):
    favorite_note(id)