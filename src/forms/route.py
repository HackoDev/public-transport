from wtforms.form import Form
from wtforms.fields import IntegerField, StringField, BooleanField
from wtforms.validators import Length, DataRequired


class RouteForm(Form):

    name = StringField(validators=[DataRequired()], label='Имя')
    forward_direction = StringField(label='Прямое направление')
    backward_direction = BooleanField(label='Обратное направление')
