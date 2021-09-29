from flask import Flask, render_template
from wtform_campos import *


# Configura app
app = Flask(__name__)
app.secret_key = 'replace later'

@app.route("/", methods=['GET', 'POST'])
def index():

    cad_form = CadastroForm()
    if cad_form.validate_on_submit():
        return "Usuário cadastrado com sucesso!"
        
    return render_template("index.html", form=cad_form)

if __name__ == "__main__":
    app.run(debug=True)
