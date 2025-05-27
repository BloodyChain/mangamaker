from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, PasswordField, BooleanField, SubmitField, HiddenField
from wtforms.validators import Email, DataRequired, Length, EqualTo, Regexp


class LoginForm(FlaskForm):
    email = StringField("Email: ", validators=[Email("Некорректный Email")], render_kw={"placeholder": "Пример: mangamaker@mail.com"})
    psw = PasswordField("Пароль: ", validators=[DataRequired(), Length(min=4, max=100, message="Пароль должен быть от 4 до 100 символов")], render_kw={"placeholder": "Пароль от 4 до 100 символов"})
    remember = BooleanField("Запомнить меня", default=False)
    submit = SubmitField("Войти")


class RegisterForm(FlaskForm):
    name = StringField("Имя: ", validators=[Length(min=4, max=100, message="Имя должно содержать от 4 до 100 символов"), Regexp('^[а-яА-Яa-zA-Z\\-]+$')], render_kw={"placeholder": "Имя от 4 до 100 символов"})
    email = StringField("Email: ", validators=[Email("Некорректный Email")], render_kw={"placeholder": "Пример: mangamaker@mail.com"})
    psw = PasswordField("Пароль: ", validators=[DataRequired(), Length(min=4, max=100, message="Пароль должен быть от 4 до 100 символов")], render_kw={"placeholder": "Пароль от 4 до 100 символов"})
    psw2 = PasswordField("Повтор пароля: ", validators=[DataRequired(), EqualTo('psw', message="Пароли не совпадают")], render_kw={"placeholder": "Повторите пароль"})
    submit = SubmitField("Регистрация")
