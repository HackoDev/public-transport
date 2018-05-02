from typing import Type
import aiohttp_jinja2
from aiohttp.web_exceptions import HTTPFound
import sqlalchemy as sa
from sqlalchemy import update, delete

from forms.paginator import PageForm


class AdminSite(object):
    def __init__(self, app):
        self.app = app
        self._registry = []
        self.app.router.add_route('GET', '/admin/', self.index_view,
                                  name='admin')

    def register_model(self, admin_cls: Type['TableAdminView']):
        admin_instance = admin_cls(self.app)
        url, _ = admin_instance.get_url_name('list')
        self._registry.append({
            'admin': admin_instance,
            'name': admin_instance.verbose_name,
            'name_plural': admin_instance.verbose_name_plural,
            'url': url
        })
        for method, handler, (url_path, url_reverse_name) in \
                admin_instance.get_urls():
            self.app.router.add_route(method, url_path, handler,
                                      name=url_reverse_name)

    @aiohttp_jinja2.template('admin/index.html')
    async def index_view(self, request):
        context = {'apps': self._registry}
        return context

    def get_registered_models(self):
        for item in self._registry:
            yield item


class TableAdminView(object):
    list_display = None
    form_class = None
    table = None
    verbose_name = None
    verbose_name_plural = None
    pagination_form = PageForm
    page_size = 10
    change_form_template = 'admin/form-view.html'
    list_view_template = 'admin/list-view.html'
    delete_view_template = 'admin/delete-view.html'

    def __init__(self, app):
        self._app = app
        self._list_display_columns = list([
            getattr(self.table.c, column_name)
            for column_name in self.list_display
        ])
        self.list_view_url, _ = self.get_url_name('list')
        self.add_view_url, _ = self.get_url_name('add')

    def transform_input_data(self, data):
        return data

    def transform_output_data(self, data):
        return data

    def get_each_context(self):
        return {
            'list_view_url': self.list_view_url,
            'add_view_url': self.add_view_url,
            'verbose_name': self.verbose_name,
            'verbose_name_plural': self.verbose_name_plural
        }

    @classmethod
    def get_form_fields(cls):
        form = cls.form_class()
        return form._fields.keys()

    @classmethod
    def format_to_dict(cls, instance):
        result_dict = dict((
            (field, getattr(instance, field))
            for field in cls.get_form_fields()
        ))
        return result_dict

    async def create_view(self, request):
        assert self.table is not None
        assert self.form_class is not None
        assert self.list_display is not None
        engine = request.app['engine']
        if request.method == 'POST':
            data = await request.post()
            form = self.form_class(data)
            if form.validate():
                insert_data = self.transform_input_data(form.data.copy())

                async with engine.acquire() as conn:
                    await conn.execute(self.table.insert().values(
                        **insert_data))
                    return HTTPFound(self.list_view_url)
        else:
            form = self.form_class()
        context = self.get_each_context()
        context.update({
            'form': form,
            'list_view_url': self.list_view_url,
            'add_view_url': self.add_view_url,
            'verbose_name': self.verbose_name,
            'verbose_name_plural': self.verbose_name_plural
        })
        return aiohttp_jinja2.render_template(self.change_form_template,
                                              request, context)

    async def list_view(self, request):
        engine = request.app['engine']
        form = self.pagination_form(data={'page': request.get('page')})
        if form.validate():
            page = form.data['page']
        else:
            page = 0
        items = []
        async with engine.acquire() as conn:
            query = sa.select(self._list_display_columns) \
                .offset(page * self.page_size).limit(self.page_size) \
                .select_from(self.table)
            async for row in conn.execute(query):
                items.append({
                    'values_list': list(
                        (getattr(row, field) for field in self.list_display)
                    ),
                    'object_id': row.id
                })
        _, reverse_name = self.get_url_name('update', with_name=True)

        context = self.get_each_context()
        context.update({
            'list_display': self.list_display,
            'count_header': len(self.list_display) + 1,
            'object_list': items,
            'detail_reverse_name': '',
            'change_url_name': reverse_name,
        })
        return aiohttp_jinja2.render_template(self.list_view_template,
                                              request, context)

    async def update_view(self, request):
        engine = request.app['engine']
        object_id = request.match_info['pk']
        instance_data = None
        async with engine.acquire() as conn:
            query = self.table.select().where(self.table.c.id == object_id) \
                .limit(1)
            async for row in conn.execute(query):
                instance_data = self.format_to_dict(row)
        if instance_data is None:
            return {
                'form': None,
                'instance': None,
                'list_view_url': self.list_view_url,
                'add_view_url': self.add_view_url,
                'verbose_name': self.verbose_name,
                'verbose_name_plural': self.verbose_name_plural
            }

        if request.method == 'POST':
            data = await request.post()
            form = self.form_class(data=data)
            if form.validate():
                updated_data = self.transform_input_data(form.data.copy())
                async with engine.acquire() as conn:
                    query = update(self.table) \
                        .where(self.table.c.id == object_id).values(
                        **updated_data)
                    await conn.execute(query)
                return HTTPFound(self.list_view_url)
        else:
            output_data = self.transform_output_data(instance_data)
            form = self.form_class(**output_data)
        context = self.get_each_context()
        _, reverse_name = self.get_url_name('delete', with_name=True)
        context.update({
            'form': form,
            'instance': instance_data,
            'list_view_url': self.list_view_url,
            'add_view_url': self.add_view_url,
            'verbose_name': self.verbose_name,
            'verbose_name_plural': self.verbose_name_plural,
            'delete_url': request.app.router[reverse_name].url(
                parts={'pk': object_id})
        })
        return aiohttp_jinja2.render_template(self.change_form_template,
                                              request, context)

    async def delete_view(self, request):
        engine = request.app['engine']
        driver_id = request.match_info['pk']
        data = None
        context = self.get_each_context()
        async with engine.acquire() as conn:
            query = self.table.select().where(self.table.c.id == driver_id) \
                .limit(1)
            async for row in conn.execute(query):
                data = self.format_to_dict(row)
        if data is None:
            context.update({
                'form': None,
                'instance': None,
            })
            return aiohttp_jinja2.render_template(self.delete_view_template,
                                                  request, context)
        if request.method == 'POST':
            async with engine.acquire() as conn:
                await conn.execute(
                    delete(self.table).where(self.table.c.id == driver_id)
                )
            return HTTPFound(self.list_view_url)
        context['instance'] = data
        return aiohttp_jinja2.render_template(self.delete_view_template,
                                              request, context)

    def get_url_name(self, url_name, with_name=False):
        tb_name = self.table.name.lower()
        list_url = '/admin/{}/'.format(tb_name)
        mapper = {
            'add': list_url + r'add/',
            'update': list_url + r'{pk:\d+}/',
            'list': list_url,
            'delete': list_url + r'{pk:\d+}/delete/'
        }
        url = mapper.get(url_name)
        assert url
        reverse_name = 'admin-{}-{}'.format(tb_name, url_name)
        if with_name:
            return url, reverse_name
        return url, None

    def get_urls(self):
        urls = [
            ('get', self.list_view, self.get_url_name('list', with_name=True)),
            (
                'get', self.create_view,
                self.get_url_name('add', with_name=True)),
            ('post', self.create_view, self.get_url_name('add')),
            ('get', self.update_view,
             self.get_url_name('update', with_name=True)),
            ('post', self.update_view, self.get_url_name('update')),
            ('get', self.delete_view,
             self.get_url_name('delete', with_name=True)),
            ('post', self.delete_view, self.get_url_name('delete')),
        ]
        return urls
