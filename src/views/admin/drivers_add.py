import aiohttp_jinja2
from aiohttp.web_exceptions import HTTPFound

from models import drivers_tbl
from forms.driver import DriverForm


@aiohttp_jinja2.template('admin/drivers-add.html')
async def drivers_add(request):
    engine = request.app['engine']
    if request.method == 'POST':
        data = await request.post()
        form = DriverForm(data)
        if form.validate():
            async with engine.acquire() as conn:
                result = await conn.execute(drivers_tbl.insert().values(
                    first_name=form.data['first_name'],
                    last_name=form.data['last_name'],
                    middle_name=form.data['middle_name'],
                    experience=form.data['experience'],
                    is_active=form.data['is_active']
                ))
                print(result)
                return HTTPFound(request.app.router['admin-drivers'].url())
    else:
        form = DriverForm()
    return {
        'form': form
    }
