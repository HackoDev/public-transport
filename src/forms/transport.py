from wtforms.form import Form
from wtforms.fields import FloatField, StringField, IntegerField
from wtforms.validators import NumberRange, DataRequired


class TransportForm(Form):
    route_id = StringField(validators=[DataRequired()], label='Маршрут')
    driver_id = IntegerField(validators=[DataRequired()], label='Водитель')
    position = StringField(label='Координаты')
