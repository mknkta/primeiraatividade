# Programação Eficaz - Projeto 1

## Status da Entrega
<img 
    src="http://3.130.178.228/progeficaz/Projeto1/svg/mknkta/primeiraatividade" 
    alt="svg" 
    width="100%" 
    height="300px"
/>

---

# 📖 GUIA DE ESTUDO PARA A PROVA (do zero absoluto)

> Todo o código também está comentado linha por linha dentro de cada arquivo. Este README explica a **ideia geral** e o **vocabulário**. Leia na ordem.

## 1. O que é este projeto?

Um **site de notas** (tipo post-it) chamado **Getit**. Você pode:

| Ação | Nome técnico (CRUD) | Sigla |
|---|---|---|
| Criar uma nota | **C**reate | C |
| Ver a lista de notas | **R**ead | R |
| Editar uma nota | **U**pdate | U |
| Apagar uma nota | **D**elete | D |

**CRUD = Create, Read, Update, Delete.** Isso cai em prova. Quase todo site que guarda dados é um CRUD.

## 2. Vocabulário básico (decore)

| Palavra | O que é (explicação simples) |
|---|---|
| **Python** | A linguagem em que o servidor é escrito. |
| **Flask** | Biblioteca (código pronto) do Python para criar sites. |
| **Servidor** | Programa que fica ligado esperando pedidos e respondendo. |
| **Navegador / Cliente** | Chrome, Edge... Quem faz pedidos ao servidor. |
| **HTTP** | O "idioma" que navegador e servidor usam para conversar. |
| **Requisição (request)** | O PEDIDO do navegador ("me dê a página X"). |
| **Resposta (response)** | O que o servidor devolve (a página em HTML). |
| **GET** | Tipo de pedido: só **buscar/ler** (abrir página, clicar em link). |
| **POST** | Tipo de pedido: **enviar dados** (formulário). Os dados vão escondidos, não aparecem na URL. |
| **Rota (route)** | Um endereço do site (`/`, `/submit`...) ligado a uma função Python. |
| **URL** | O endereço, ex.: `http://127.0.0.1:5000/delete/3`. |
| **127.0.0.1 / localhost** | "Este mesmo computador". Porta **5000** = porta padrão do Flask. |
| **HTML** | Linguagem que descreve a página (títulos, formulários, links). |
| **Template (molde)** | HTML com "buracos" para o Python preencher depois. |
| **Banco de dados** | Lugar onde os dados ficam guardados de forma organizada. |
| **SQLite** | Banco de dados simples que vive em UM arquivo (`banco.db`). |
| **SQL** | Linguagem para conversar com o banco (`SELECT`, `INSERT`...). |
| **Tabela** | Como uma planilha do Excel: colunas (id, title, content) e linhas (cada nota). |
| **JSON** | Formato de texto para guardar dados: `{"titulo": "A", "detalhes": "B"}`. |
| **Redirect** | Mandar o navegador ir para OUTRO endereço. |
| **Estático (static)** | Arquivos que não mudam: imagens, css, templates. |
| **Biblioteca / módulo** | Código pronto de outra pessoa (ou de outro arquivo seu) que você `import`a. |

## 3. Os arquivos do projeto

```
primeiraatividade/
├── servidor.py                 <- ROTAS: recebe os pedidos do navegador
├── views.py                    <- monta as PÁGINAS (junta HTML + dados)
├── utils.py                    <- BANCO DE DADOS e leitura de arquivos
├── banco.db                    <- o banco SQLite (onde as notas ficam guardadas)
├── README.md                   <- este arquivo
└── static/
    ├── img/logo-getit.png      <- a logo
    ├── data/notes.json         <- notas de exemplo (versão antiga, não é mais usada pelo site)
    └── templates/
        ├── index.html          <- página inicial (formulário + lista)
        ├── update.html         <- página de editar
        └── components/
            └── note.html       <- molde de UMA nota da lista
```

### Quem chama quem (MEMORIZE este fluxo)

```
NAVEGADOR  ->  servidor.py  ->  views.py  ->  utils.py  ->  banco.db
 (pede)         (rota)         (monta HTML)   (SQL)         (dados)
NAVEGADOR  <-  servidor.py  <-  views.py  <-  utils.py  <-  banco.db
 (recebe)
```

Cada camada tem UMA função: **servidor** decide o endereço, **views** monta a página, **utils** fala com o banco. Separar assim deixa o código organizado.

## 4. As rotas (servidor.py)

| Endereço | Método | O que faz | Depois |
|---|---|---|---|
| `/` | GET | Mostra a página inicial com todas as notas | mostra a página |
| `/submit` | POST | Recebe o formulário e **cria** uma nota | redireciona para `/` |
| `/delete/<id>` | GET | **Apaga** a nota com aquele id | redireciona para `/` |
| `/update/<id>` | GET | Mostra a tela de **editar** a nota | mostra a página |
| `/update` | POST | Recebe o formulário de edição e **atualiza** | redireciona para `/` |

- `@app.route(...)` = "quando alguém pedir este endereço, rode a função logo abaixo".
- `<int:id>` = pedaço variável da URL, só aceita número inteiro. `/delete/7` -> `id = 7`.
- `methods=['POST']` = essa rota aceita POST. Sem isso só aceita GET.
- `request.form.get('titulo')` = pega o valor do campo `name="titulo"` do formulário.
- `redirect('/')` = "vá para a página inicial".

## 5. Funções e o que cada uma faz

### servidor.py
| Função | Faz |
|---|---|
| `index()` | Devolve a página inicial. |
| `submit_form()` | Lê título e detalhes do formulário e manda criar nota. |
| `delete(id)` | Manda apagar a nota `id`. |
| `edit(id)` | Mostra o formulário de edição da nota `id`. |
| `update()` | Lê o formulário de edição e manda atualizar. |

### views.py
| Função | Faz |
|---|---|
| `index()` | Pega todas as notas, preenche o molde `note.html` para cada uma, junta tudo e coloca dentro de `index.html`. |
| `submit(titulo, detalhes)` | Chama `add_note`. |
| `delete(id)` | Chama `delete_note`. |
| `edit(id)` | Busca a nota com `get_note` e preenche `update.html`. |
| `update(id, titulo, detalhes)` | Chama `update_note`. |

### utils.py
| Função | Comando SQL | Faz |
|---|---|---|
| `load_data(filename)` | - | Lê um arquivo JSON e devolve lista/dicionário Python. |
| `load_template(filename)` | - | Lê um HTML e devolve como texto. |
| `save_data(filename, data)` | - | Grava dados em um arquivo JSON. |
| `create_database()` | `CREATE TABLE IF NOT EXISTS` | Cria a tabela `note` se não existir. Roda ao ligar o servidor. |
| `load_notes()` | `SELECT` | Devolve TODAS as notas (lista de tuplas). |
| `add_note(titulo, detalhes)` | `INSERT INTO` | **Cria** uma nota. |
| `delete_note(id)` | `DELETE FROM ... WHERE` | **Apaga** uma nota. |
| `get_note(id)` | `SELECT ... WHERE` | Devolve UMA nota (ou `None`). |
| `update_note(id, titulo, detalhes)` | `UPDATE ... SET ... WHERE` | **Altera** uma nota. |

## 6. O banco de dados (SQLite) explicado

Tabela `note`:

| id | title | content |
|---|---|---|
| 1 | Receita | Misture tudo |
| 2 | Compras | Leite, pão |

- `id INTEGER PRIMARY KEY AUTOINCREMENT` -> número único de cada nota; o banco conta sozinho (1, 2, 3...). **PRIMARY KEY** = identificador único.
- `TEXT` = tipo texto. `INTEGER` = número inteiro.

**Os 5 passos de toda função do banco:**
1. `sqlite3.connect('banco.db')` -> abre o arquivo do banco.
2. `connection.cursor()` -> cria o cursor (quem executa SQL).
3. `cursor.execute("SQL", (valores,))` -> roda o comando.
4. `connection.commit()` -> **salva** (obrigatório em INSERT/UPDATE/DELETE; não precisa em SELECT).
5. `connection.close()` -> fecha.

**Comandos SQL (decore):**

```sql
SELECT id, title, content FROM note              -- LER tudo
SELECT id, title, content FROM note WHERE id = 3 -- LER uma
INSERT INTO note (title, content) VALUES ('a','b') -- CRIAR
UPDATE note SET title='x', content='y' WHERE id=3  -- ALTERAR
DELETE FROM note WHERE id = 3                      -- APAGAR
```

> ⚠️ **Sem `WHERE`, UPDATE e DELETE afetam TODAS as linhas!**

**Por que `?` e não colar o texto direto?** Os `?` são preenchidos pela tupla `(titulo, detalhes)`. Isso evita **SQL Injection** (alguém digitar um comando SQL malicioso no formulário). É a forma segura.

**Por que `(id,)` com vírgula?** Em Python, `(5)` é só o número 5; `(5,)` é uma **tupla** de um item. O `execute` exige tupla.

**`fetchall()` vs `fetchone()`:** `fetchall` = todas as linhas (lista de tuplas). `fetchone` = uma linha (uma tupla) ou `None`.

## 7. Templates e `.format()` (a parte mais confusa)

O HTML tem **buracos** entre chaves: `<h3>{title}</h3>`. O Python preenche:

```python
"<h3>{title}</h3>".format(title="Minha nota")   # -> "<h3>Minha nota</h3>"
```

Fluxo da página inicial:
1. `note.html` é lido e preenchido **uma vez por nota** (`{id}`, `{title}`, `{details}`) -> vira vários `<li>`.
2. Os `<li>` são juntados com `'\n'.join(...)` em um texto só.
3. Esse texto entra no buraco `{notes}` do `index.html`.
4. Flask (`render_template_string`) processa o resultado final.

**Por que `{{{{ url_for(...) }}}}` no index.html?** Porque `.format()` transforma `{{` em `{`. Então `{{{{` vira `{{` e `}}}}` vira `}}`. Aí o Flask (Jinja) entende `{{ url_for(...) }}` e troca pelo caminho da imagem. Quatro chaves = "escapar" as chaves do `.format()` para sobrarem duas para o Flask.

## 8. HTML em resumo

| Tag | Significa |
|---|---|
| `<html>` `<head>` `<body>` | Raiz / infos da página / conteúdo visível |
| `<title>` | Título na aba do navegador |
| `<h3>` | Título pequeno |
| `<p>` | Parágrafo |
| `<img src="...">` | Imagem |
| `<ul>` / `<li>` | Lista com marcadores / item da lista |
| `<a href="...">` | Link |
| `<form action="..." method="POST">` | Formulário: para onde envia e como |
| `<input type="text" name="x">` | Caixa de texto. `name` = nome que o Python usa |
| `<input type="hidden">` | Campo escondido (envia o id sem aparecer) |
| `<input type="submit">` / `<button>` | Botão de enviar |
| `<label for="id">` | Texto que descreve um campo |

## 9. Python em resumo (o que aparece no código)

| Coisa | Explicação |
|---|---|
| `import x` | Traz um módulo/arquivo. |
| `from x import y` | Traz só o `y` de dentro de `x`. |
| `def nome(a, b):` | Cria uma **função** com parâmetros `a` e `b`. |
| `return valor` | Devolve um valor e encerra a função. |
| `# texto` | Comentário (o Python ignora). |
| `@app.route(...)` | **Decorador**: "coloca uma função extra em cima" da função de baixo. |
| `f'texto {variavel}'` | **f-string**: coloca o valor da variável no texto. |
| `with open(...) as f:` | Abre um arquivo e fecha sozinho ao terminar. |
| `'r'` / `'w'` | Modo do arquivo: leitura / escrita (apaga o antigo). |
| `encoding='utf-8'` | Entende acentos. |
| `[x for x in lista]` | **List comprehension**: cria lista repetindo uma conta. |
| `'\n'.join(lista)` | Cola os itens da lista em um texto separados por quebra de linha. |
| `dados[0]` | Posição 0 (primeiro item, a contagem começa do 0). |
| `(a, b)` | **Tupla**: grupo de valores que não muda. |
| `if __name__ == '__main__':` | Só executa se rodar ESTE arquivo direto. |
| `app.run(debug=True)` | Liga o servidor; `debug` recarrega sozinho e mostra erros. |
| `None` | "Nada / vazio". |

## 10. Como rodar

```bash
pip install flask       # instala o Flask (uma vez)
python servidor.py      # liga o servidor
```
Abra no navegador: **http://127.0.0.1:5000**

## 11. Passo a passo de cada ação (perguntas clássicas de prova)

**Criar nota:** digita no formulário -> clica enviar -> navegador faz **POST /submit** -> `submit_form()` lê título/detalhes -> `views.submit` -> `add_note` faz **INSERT** -> `redirect('/')` -> página recarrega mostrando a nota nova.

**Ver notas:** **GET /** -> `index()` -> `views.index()` -> `load_notes()` faz **SELECT** -> preenche `note.html` para cada uma -> entra no `index.html` -> navegador mostra.

**Apagar:** clica em "Excluir" (link) -> **GET /delete/3** -> `delete_note(3)` faz **DELETE ... WHERE id=3** -> redireciona para `/`.

**Editar:** clica em "Editar" -> **GET /update/3** -> `get_note(3)` faz **SELECT** -> mostra `update.html` preenchido -> usuário altera e clica Salvar -> **POST /update** (com o `id` no campo escondido) -> `update_note` faz **UPDATE ... WHERE id=3** -> redireciona para `/`.

## 12. Pegadinhas e problemas do código (bons para "o que poderia melhorar?")

1. **Excluir usa GET** (um link). O correto seria POST/DELETE, porque GET deve só ler. Alguém pode apagar notas só abrindo um link.
2. **Injeção de HTML / template (XSS)**: o texto digitado nas notas é colocado direto no HTML e depois passa pelo `render_template_string`. Se alguém digitar `<script>` ou `{{ 7*7 }}`, será executado. O ideal é escapar o texto.
3. **`/update/<id>` com id que não existe**: `get_note` devolve `None` e `note[0]` dá erro `TypeError` (página 500).
4. **Conexão repetida**: cada função abre e fecha o banco. Funciona, mas repete código.
5. **`load_data` e `save_data`** (JSON) e `notes.json` **não são usados** mais; sobraram da versão antiga.
6. **`debug=True`** só deve ser usado em desenvolvimento, nunca em produção.
7. O `id` chega do formulário como **texto** (`"3"`); o SQLite converte sozinho, então funciona.

## 13. Mini-cola para decorar

- **CRUD** = Create, Read, Update, Delete = INSERT, SELECT, UPDATE, DELETE.
- **GET** = ler / **POST** = enviar dados.
- Fluxo: navegador -> servidor.py -> views.py -> utils.py -> banco.db.
- `commit()` só quando MUDA dados.
- `WHERE` sempre em UPDATE/DELETE.
- `?` no SQL = segurança contra SQL Injection.
- `redirect('/')` depois de POST = evita reenviar o formulário ao atualizar a página.
- `{{{{ }}}}` no `.format()` vira `{{ }}` do Flask.
- Servidor local: `127.0.0.1:5000`.
