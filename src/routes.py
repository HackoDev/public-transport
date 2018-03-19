import config
from views import public
from views import admin


def setup_routes(app):
    # TODO: refactor url schema- use resources.
    app.router.add_get('/', public.index_view, name='public-index')
    app.router.add_get('/admin/', admin.index, name='admin')
    app.router.add_get('/admin/drivers/', admin.drivers_list, name='admin-drivers')
    app.router.add_get('/admin/drivers/add/', admin.drivers_add, name='admin-drivers-add')
    app.router.add_post('/admin/drivers/add/', admin.drivers_add)
    app.router.add_get(r'/admin/drivers/{pk:\d+}/', admin.drivers_update, name='admin-drivers-update')
    app.router.add_post(r'/admin/drivers/{pk:\d+}/', admin.drivers_update)
    app.router.add_static('/static/', path=config.STATIC_ROOT, name='static')
