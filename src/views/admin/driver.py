from forms.driver import DriverForm
from forms.transport import TransportForm
from forms.route import RouteForm
from models import drivers_tbl, transports_tbl, routes_tbl
from views.admin import TableAdminView


class DriverAdmin(TableAdminView):
    table = drivers_tbl
    list_display = ('id', 'first_name', 'last_name', 'middle_name')
    form_class = DriverForm
    verbose_name = 'Водитель'
    verbose_name_plural = 'Водители'


class TransportAdmin(TableAdminView):
    table = transports_tbl
    list_display = ('id',)
    form_class = TransportForm
    verbose_name = 'Траноспорт'
    verbose_name_plural = 'Траноспорт'


class RoutesAdmin(TableAdminView):
    table = routes_tbl
    list_display = ('id', 'name', 'forward_direction', 'backward_direction')
    form_class = RouteForm
    verbose_name = 'Маршрут'
    verbose_name_plural = 'Маршруты'
    change_form_template = 'admin/route-form.html'
