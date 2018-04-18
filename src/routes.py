import config
from views import public
from views import admin
from views.admin.driver import DriverAdmin, TransportAdmin, RoutesAdmin


def setup_routes(app):
    # TODO: refactor url schema- use resources.
    app.router.add_get('/', public.index_view, name='public-index')
    app.router.add_get('/admin/', admin.index, name='admin')
    app.router.add_static('/static/', path=config.STATIC_ROOT, name='static')
    register_admin(app, DriverAdmin)
    register_admin(app, TransportAdmin)
    register_admin(app, RoutesAdmin)


def register_admin(app, admin_cls):

    admin_instance = admin_cls(app)
    for method, handler, (url_path, url_reverse_name) in \
            admin_instance.get_urls():
        app.router.add_route(method, url_path, handler, name=url_reverse_name)
