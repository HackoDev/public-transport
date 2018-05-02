from wtforms.form import Form
from wtforms.fields import IntegerField, StringField
from wtforms.validators import NumberRange, DataRequired


class RouteStationForm(Form):

    route_id = IntegerField(validators=[DataRequired(), NumberRange(min=0)],
                            label='Маршрут')
    station_id = IntegerField(validators=[DataRequired(), NumberRange(min=0)],
                              label='Станциия')
