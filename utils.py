import json


def load_data(filename):
    with open(f'static/data/{filename}', 'r', encoding='utf-8') as arquivo:
        return json.load(arquivo)


def load_template(filename):
    with open(f'static/templates/{filename}', 'r', encoding='utf-8') as arquivo:
        return arquivo.read()

def save_data(filename, data):
    with open('static/data/' + filename, 'w', encoding='utf-8') as arquivo:
        json.dump(data, arquivo, ensure_ascii=False, indent=2)

