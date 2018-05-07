from wtforms.form import Form
from wtforms.fields import IntegerField as BaseIntegerField
from wtforms.validators import NumberRange, DataRequired


class IntegerField(BaseIntegerField):

    def pre_validate(self, form):
        try:
            self.data = int(self.data)
        except Exception as e:
            self.errors.append(str(e))


class PageForm(Form):
    page = IntegerField(validators=[DataRequired(), NumberRange(min=0)])
