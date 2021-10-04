from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError

from models import User

def credenciais_invalida(form, campo):
    """ Validador de nome de usuário e senha """

    nomeusuario_in = form.nomeusuario.data
    senha_in = campo.data

    # Verifica se as credenciais são válidas
    usuario_objeto = User.query.filter_by(nomeusuario=nomeusuario_in).first()
    if usuario_objeto is None:
        raise ValidationError("Nome de usuário ou senha está incorreto!")
    elif senha_in != usuario_objeto.senha:
        raise ValidationError("Nome de usuário ou senha está incorreto!")


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

    def valida_nomeusuario(self, nomeusuario):
        usuario_objeto = User.query.filter_by(nomeusuario=nomeusuario.data).first()
        if usuario_objeto:
            raise ValidationError("O nome de usuário já existe. Escolha outro nome de usuário.")

class LoginForm(FlaskForm):
    """ Formulário de login """

    nomeusuario = StringField('nomeusuario_label',
        validators=[InputRequired(message="Nome de usuário é obrigatório!")])
    senha=StringField('senha_label',
        validators=[InputRequired(message="Senha é obrigatória!"),
        credenciais_invalida])
    botao_cadastrar = SubmitField('Entrar')
