# ---------------------------------------------------------------
# servidor.py  ->  É a "porta de entrada" do site.
# Ele recebe os pedidos do navegador (ex.: "quero a página inicial")
# e decide qual função chamar para responder.
# ---------------------------------------------------------------

# "from X import Y" = pega a ferramenta Y da biblioteca X (biblioteca = código pronto de outras pessoas).
# Flask               -> a classe principal que cria o site/servidor.
# render_template_string -> pega um texto HTML e o transforma na página final (processa os {{ }} do Jinja).
# request             -> guarda os dados que o navegador enviou (ex.: o que foi digitado no formulário).
# redirect            -> manda o navegador ir para outro endereço (ex.: voltar para a página inicial).
from flask import Flask, render_template_string, request, redirect

# "import views" = traz o nosso arquivo views.py (que monta as páginas). Usamos como views.função().
import views


# Cria o aplicativo (o site). __name__ é o nome deste arquivo; o Flask usa isso para saber onde ficam as coisas.
app = Flask(__name__)

# Diz ao Flask que os arquivos "estáticos" (imagens, css...) ficam na pasta 'static'.
# Assim o navegador consegue pedir /static/img/logo-getit.png.
app.static_folder = 'static'

# @app.route('/') é um "decorador": liga o endereço '/' (página inicial) à função logo abaixo.
# Quando alguém abre http://127.0.0.1:5000/ o Flask executa index().
@app.route('/')
def index():
    # views.index() devolve o HTML (texto) da página inicial já com as notas dentro.
    # render_template_string() processa esse texto (ex.: troca o url_for(...) pelo caminho real da imagem)
    # e devolve o resultado ao navegador.
    return render_template_string(views.index())

# Endereço /submit. methods=['POST'] = só aceita o pedido do tipo POST (envio de formulário).
# (o padrão do Flask é só GET, que é "só ler/abrir uma página")
@app.route('/submit', methods=['POST'])
def submit_form():
    # request.form = os campos do formulário enviado. .get('titulo') pega o valor do campo com name="titulo".
    titulo = request.form.get('titulo')
    # Mesma coisa para o campo name="detalhes".
    detalhes = request.form.get('detalhes')

    # Manda o views.py salvar a nota nova.
    views.submit(titulo, detalhes)
    # Depois de salvar, manda o navegador voltar para '/' (assim a lista já aparece atualizada).
    return redirect('/')

# <int:id> = parte variável do endereço; só aceita número inteiro e o guarda na variável "id".
# Ex.: /delete/3 -> id = 3. Como não tem methods=..., é GET (basta clicar no link "Excluir").
@app.route('/delete/<int:id>')
def delete(id):
    # Manda apagar a nota com esse id.
    views.delete(id)
    # Volta para a página inicial.
    return redirect('/')

# Ex.: /update/3 -> abre a tela de EDITAR a nota 3 (GET).
@app.route('/update/<int:id>')
def edit(id):
    # views.edit(id) monta o HTML do formulário de edição já preenchido com a nota.
    return render_template_string(views.edit(id))


# Mesmo endereço base '/update', mas agora com POST: é o formulário de edição sendo ENVIADO.
# (o mesmo endereço pode fazer coisas diferentes dependendo se é GET ou POST)
@app.route('/update', methods=['POST'])
def update():
    # id vem de um campo escondido (hidden) do formulário; chega como texto, ex.: "3".
    id = request.form.get('id')
    titulo = request.form.get('titulo')
    detalhes = request.form.get('detalhes')

    # Manda atualizar a nota no banco.
    views.update(id, titulo, detalhes)
    return redirect('/')

# Só é verdade quando você roda ESTE arquivo direto (python servidor.py),
# e não quando ele é importado por outro arquivo.
if __name__ == '__main__':
    # Liga o servidor. debug=True = recarrega sozinho quando você altera o código e mostra erros detalhados.
    # Por padrão fica em http://127.0.0.1:5000
    app.run(debug=True)
