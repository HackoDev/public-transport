import config
from views import index
from views.base_admin_view import AdminSite
from views import admin


def setup_routes(app):
    """
    Helper function for setup app routes.

    :param app: app instance
    """
    app.router.add_get('/', index.index_view, name='public-index')
    app.router.add_static('/static/', path=config.STATIC_ROOT, name='static')
    # register admin classes with admin routes
    admin_site = AdminSite(app)
    admin_site.register_model(admin.DriverAdmin)
    admin_site.register_model(admin.TransportAdmin)
    admin_site.register_model(admin.RoutesAdmin)
    admin_site.register_model(admin.RouteStationAdmin)
    admin_site.register_model(admin.StationsAdmin)
