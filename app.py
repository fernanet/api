from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, current_user, login_required, logout_user

from wtform_campos import *
from models import *

# Configura app
app = Flask(__name__)
app.secret_key = 'replace later'

# Configura banco de dados
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://xrqpjawfbnmaom:2ba5d7716cd766dd20b94d1a77392fb7f32a3e5ad44114ffa8fb584314da7a19@ec2-34-197-135-44.compute-1.amazonaws.com:5432/d1rjbebpnttoen'
db = SQLAlchemy(app)

# Configura flask login
login = LoginManager(app)
login.init_app(app)

@login.user_loader
def carrega_usuario(id):

    return User.query.get(int(id))

@app.route("/", methods=['GET', 'POST'])
def index():

    cad_form = CadastroForm()

    # Banco de dados atualizado se validação ocorrer com sucesso
    if cad_form.validate_on_submit():
        nomeusuario = cad_form.nomeusuario.data
        senha = cad_form.senha.data

        # Hash senha
        senha_hashed = pbkdf2_sha256.hash(senha)

        # Adiciona usuário ao banco de dados
        usuario = User(nomeusuario=nomeusuario, senha=senha_hashed)
        db.session.add(usuario)
        db.session.commit()

        flash('Cadastrado com sucesso. Por favor, efetue login.', 'sucesso')

        return redirect(url_for('login'))

    return render_template("index.html", form=cad_form)

@app.route("/login", methods=['GET', 'POST'])
def login():

    login_form = LoginForm()

    # Permite logar se validação ocorrer com sucesso
    if login_form.validate_on_submit():
        usuario_objeto = User.query.filter_by(nomeusuario=login_form.nomeusuario.data).first()
        login_user(usuario_objeto)
        return redirect(url_for('chat'))

        return "Não está logado :("

    return render_template("login.html", form=login_form)

@app.route("/chat", methods=['GET', 'POST'])
@login_required
def chat():

    if not current_user.is_authenticated:
        flash('Por favor, efetue login.', 'perigo')
        return redirect(url_for('login'))

    return "Chat with me"

@app.route("/logout", methods=['GET'])
def logout():

    logout_user()
    flash('Você efetuou logout com sucesso', 'sucesso')
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)
