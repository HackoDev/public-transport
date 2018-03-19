import logging
import asyncio

from app import make_app

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    app = make_app()
    handler = app.make_handler()
    loop = asyncio.get_event_loop()
    srv = loop.run_until_complete(
        loop.create_server(handler, host='0.0.0.0', port=8080)
    )
    logger.info('Server started on 127.0.0.1:{}'.format(8080))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        srv.close()
        loop.run_until_complete(srv.wait_closed())
        loop.close()
