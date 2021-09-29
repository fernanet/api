from flask import Flask, render_template
from wtform_campos import *
from models import *

# Configura app
app = Flask(__name__)
app.secret_key = 'replace later'

# Configura banco de dados
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://xrqpjawfbnmaom:2ba5d7716cd766dd20b94d1a77392fb7f32a3e5ad44114ffa8fb584314da7a19@ec2-34-197-135-44.compute-1.amazonaws.com:5432/d1rjbebpnttoen'
db = SQLAlchemy(app)

@app.route("/", methods=['GET', 'POST'])
def index():

    cad_form = CadastroForm()
    if cad_form.validate_on_submit():
        nomeusuario = cad_form.nomeusuario.data
        senha = cad_form.senha.data

        # Verifica se nomeusuario existe
        usuario_objeto = User.query.filter_by(nomeusuario=nomeusuario).first()
        if usuario_objeto:
            return "Esse nome de usuário já existe!"

        # Adiciona usuário ao banco de dados
        usuario = User(nomeusuario=nomeusuario, senha=senha)
        db.session.add(usuario)
        db.session.commit()
        return "Inserido no banco de dados"

    return render_template("index.html", form=cad_form)

if __name__ == "__main__":
    app.run(debug=True)
