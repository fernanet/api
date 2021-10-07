import os

from time import localtime, strftime
from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from flask_socketio import SocketIO, send, emit, join_room, leave_room

from wtform_fields import *
from models import *

# Configura app
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET')

# Configura banco de dados
app.config['SQLALCHEMY_DATABASE_URI']=os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)

# Inicializa Flask-SocketIO
socketio = SocketIO(app)
ROOMS = ["sala", "notícias", "jogos", "codificação"]

# Configura flask login
login = LoginManager(app)
login.init_app(app)

@login.user_loader
def load_user(id):

    return User.query.get(int(id))

@app.route("/", methods=['GET', 'POST'])
def index():

    reg_form = RegForm()

    # Banco de dados atualizado se validação ocorrer com sucesso
    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data

        # Hash senha
        hashed_pswd = pbkdf2_sha256.hash(password)

        # Adiciona usuário ao banco de dados
        user = User(username=username, hashed_pswd=hashed_pswd)
        db.session.add(user)
        db.session.commit()

        flash('Cadastrado com sucesso. Por favor, efetue login.', 'sucesso')

        return redirect(url_for('login'))

    return render_template("index.html", form=reg_form)

@app.route("/login", methods=['GET', 'POST'])
def login():

    login_form = LoginForm()

    # Permite logar se validação ocorrer com sucesso
    if login_form.validate_on_submit():
        user_object = User.query.filter_by(username=login_form.username.data).first()
        login_user(user_object)
        return redirect(url_for('chat'))

    return render_template("login.html", form=login_form)

@app.route("/chat", methods=['GET', 'POST'])
def chat():

    if not current_user.is_authenticated:
        flash('Por favor, efetue login.', 'perigo')
        return redirect(url_for('login'))

    return render_template('chat.html', username=current_user.username rooms=ROOMS)

@app.route("/logout", methods=['GET'])
def logout():

    logout_user()
    flash('Você efetuou logout com sucesso', 'sucesso')
    return redirect(url_for('login'))

@app.errorhandler(404)
def page_not_found(e):
    # Note que nós configuramos o status 404 explicitamente
    return render_template('404.html'), 404

@socketio.on('incoming-msg')
def on_message(data):
    """ Mensagens de Broadcast """

    msg = data["msg"]
    username = data["username"]
    room = data["room"]
    # Configura timestamp
    time_stamp = time.strftime('%d/%b %H:%M', localtime())
    send({"username": username, "msg": msg, 'time_stamp': time_stamp}, room=room)

@socketio.on('join')
def on_join(data):
    """Usuário junta-se a uma sala"""

    username = data["username"]
    room = data["room"]
    join_room(room)

    # Broadcast that new user has joined
    send({"msg": username + " tem se juntado a " + room + " room."}, room=room)

@socketio.on('leave')
def on_leave(data):
    """Usuário deixou uma sala"""

    username = data['username']
    room = data['room']
    leave_room(room)
    send({"msg": username + " tem deixado a sala"}, room=room)

if __name__ == "__main__":
    app.run(debug=True)
