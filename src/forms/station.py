from wtforms.form import Form
from wtforms.fields import StringField
from wtforms.validators import DataRequired


class StationForm(Form):

    name = StringField(validators=[DataRequired()], label='Название')
    coord = StringField(validators=[DataRequired()],
                        label='Координаты станции')
