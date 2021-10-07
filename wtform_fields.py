from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError
from passlib.hash import pbkdf2_sha256
from models import User

def invalid_credentials(form, field):
    """ Validador de nome de usuário e senha """

    password = field.data
    username = form.username.data

    # Verifica se as credenciais são válidas
    user_object = User.query.filter_by(username=username).first()
    if user_object is None:
        raise ValidationError("Nome de usuário ou senha está incorreto!")
    elif not pbkdf2_sha256.verify(password, user_object.hashed_pswd):
        raise ValidationError("Nome de usuário ou senha está incorreto!")


class RegForm(FlaskForm):
    """ Formulário de Cadastro """

    username = StringField('username',
        validators=[InputRequired(message="O nome de usuário é obrigatório!"),
        Length(min=5, max=15, message="O nome de usuário deve ter entre 5 e 15 caracteres!")])
    password = PasswordField('password',
        validators=[InputRequired(message="A senha é obrigatória!"),
        Length(min=5, max=15, message="A senha deve ter entre 5 e 15 caracteres!")])
    confirm_pswd = PasswordField('confirm_pswd',
        validators=[InputRequired(message="A senha é obrigatória!"),
        EqualTo('password', message="As senhas devem ser iguais!")])

    def validate_username(self, username):
        user_object = User.query.filter_by(username=username.data).first()
        if user_object:
            raise ValidationError("O nome de usuário já existe. Escolha outro nome de usuário.")

class LoginForm(FlaskForm):
    """ Formulário de login """

    username = StringField('username',
        validators=[InputRequired(message="Nome de usuário é obrigatório!")])
    password=StringField('password',
        validators=[InputRequired(message="Senha é obrigatória!"),
        credenciais_invalida])
