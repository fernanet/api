from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo

class CadastroForm(FlaskForm):
    """ Formulário de Cadastro """

    nomeusuario = StringField('nomeusuario_label',
        validators=[InputRequired(message="O nome de usuário é obrigatório!"),
        Length(min=5, max=15, message="O nome de usuário deve ter entre 5 e 15 caracteres!")])
    senha = PasswordField('senha_label',
        validators=[InputRequired(message="A senha é obrigatória!"),
        Length(min=5, max=15, message="A senha deve ter entre 5 e 15 caracteres!")])
    confirmar_senha = PasswordField('confirmar_senha_label',
        validators=[InputRequired(message="A senha é obrigatória!"),
        EqualTo('senha', message="As senhas devem ser iguais!")])
    botao_cadastrar = SubmitField('Cadastrar')