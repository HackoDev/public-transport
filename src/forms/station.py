from wtforms.form import Form
from wtforms.fields import IntegerField
from wtforms.validators import NumberRange


class PageForm(Form):

    page = IntegerField(validators=[NumberRange(min=0)])
