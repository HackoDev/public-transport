import json

from wtforms.form import Form
from wtforms.fields import IntegerField, StringField, BooleanField
from wtforms.validators import Length, DataRequired


class LineStringField(StringField):

    def post_validate(self, form, validation_stopped):
        super(LineStringField, self).post_validate(
            form, validation_stopped=validation_stopped)
        print(self.data)
        # try:
        #     value = json.loads(self.data)
        # except Exception as e:
        #     self.errors.append(str(e))


class RouteForm(Form):

    id = StringField(validators=[DataRequired()], label='Номер')
    name = StringField(validators=[DataRequired()], label='Имя')
    forward_direction = LineStringField(label='Прямое направление')
    backward_direction = LineStringField(label='Обратное направление')
