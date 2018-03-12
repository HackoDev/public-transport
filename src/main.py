import asyncio
from aiohttp import web
from app import make_app

if __name__ == '__main__':
    app = make_app()
    handler = app.make_handler()
    loop = asyncio.get_event_loop()
    srv = loop.run_until_complete(
        loop.create_server(handler, host='127.0.0.1', port=8080)
    )
    print('Server started on 127.0.0.1:{}'.format(8080))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        srv.close()
        loop.run_until_complete(srv.wait_closed())
        loop.close()
