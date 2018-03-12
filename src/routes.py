

def setup_routes(app):

    app.router.add_get('/admin/', list_view, name=' admin')
    app.router.add_static('/static/', path=config.STATIC_ROOT, name='static')
    return