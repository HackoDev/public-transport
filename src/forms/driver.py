from wtforms.form import Form
from wtforms.fields import IntegerField, StringField, BooleanField
from wtforms.validators import Length, DataRequired


class DriverForm(Form):

    first_name = StringField(validators=[DataRequired()], label='Имя')
    last_name = StringField(validators=[DataRequired()], label='Фамилия')
    middle_name = StringField(validators=[DataRequired()], label='Отчество')
    experience = IntegerField(validators=[DataRequired()], label='Опыт')
    is_active = BooleanField(label='Работает')
