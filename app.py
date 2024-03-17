# Importações necessárias do Flask
from flask import Flask, render_template, request, url_for, redirect
# Importação do SQLAlchemy para interagir com o banco de dados
from flask_sqlalchemy import SQLAlchemy

# Criação de uma instância do Flask
app = Flask(__name__)

# Configuração do URI do banco de dados SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

# Criação de uma instância do SQLAlchemy, passando a instância do Flask como parâmetro
db = SQLAlchemy(app)

# Definição de uma classe Pessoa, que herda de db.Model (um modelo do SQLAlchemy)
class Pessoa(db.Model):
    __tablename__='cliente'# Nome da tabela no banco de dados
    __id = db.Column(db.Integer, primary_key=True, autoincrement=True)# Coluna para o ID,tipo Int, primary_key indica que é uma chave primária e autoincrement=True indica que será autoincrementada
    nome = db.Column(db.String)# Coluna para o nome, com tipo String
    telefone = db.Column(db.String)# Coluna para o telefone, com tipo String
    cpf = db.Column(db.String)# Coluna para o CPF, com tipo String
    email = db.Column(db.String)# Coluna para o email, com tipo String

    # Método construtor para inicializar os atributos da classe
    def __init__(self, nome, telefone, cpf, email):
        self.nome = nome
        self.telefone = telefone
        self.cpf = cpf
        self.email = email

# Rota para a página inicial ("/index"), que renderiza o template "index.html"
@app.route("/index")
def index():
    return render_template("index.html")

# Rota para a página de cadastro ("/cadastrar"), que renderiza o template "cadastro.html"
@app.route("/cadastrar")
def cadastrar():
    return render_template("cadastro.html")

@app.route("/cadastro", methods=['GET', 'POST'])
def cadastro():
    if request.method == "POST":
        nome = request.form.get('nome')
        telefone = request.form.get('telefone')
        cpf = request.form.get('cpf')
        email = request.form.get('email')

        if nome and telefone and cpf and email: 
            p = Pessoa(nome, telefone, cpf, email)
            db.session.add(p)
            db.session.commit()
    return redirect(url_for("index"))

@app.route("/lista")
def lista():
    pessoas = Pessoa.query.all()
    return render_template("lista.html", pessoas=pessoas)


@app.route("/excluir/<int:id>")
def excluir(id):
    pessoa = Pessoa.query.filter_by(_id=id).first()

    db.session.delete(pessoa)
    db.session.commit()

    pessoas = Pessoa.query.all()
    return render_template("lista.html", pessoas=pessoas)

@app.route("/atualizar/<int:id>", methods=['GET', 'POST'])
def atualizar(id):
    pessoa = Pessoa.query.filter_by(_id=id).first()
    
    if request.method == "POST":
        nome = request.form.get('nome')
        telefone = request.form.get('telefone')
        cpf = request.form.get('cpf')
        email = request.form.get('email')

        if nome and telefone and cpf and email:
            pessoa.nome = nome
            pessoa.telefone = telefone
            pessoa.cpf = cpf
            pessoa.emai = email

            db.session.commit()

            return redirect(url_for("lista"))
        
    return render_template("atualizar.html", pessoa=pessoa)

# Verifica se o arquivo atual está sendo executado diretamente
if __name__ == '__main__':
    # Entra no contexto da aplicação Flask para evitar erros de contexto
    with app.app_context():
        # Cria todas as tabelas definidas nos modelos SQLAlchemy
        db.create_all()
    # Inicia o servidor Flask em modo de depuração
    app.run(debug=True)
