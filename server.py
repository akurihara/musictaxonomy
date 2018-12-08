from tornado.ioloop import IOLoop
from tornado.options import options
from tornado.web import Application

from auth.handlers import LoginHandler, OauthCallbackHandler
from graph.handlers import CreateTaxonomyGraphHandler
from handlers import IndexHandler, StatusHandler
from settings import settings


def make_app():
    return Application(
        [
            (r"/", IndexHandler),
            (r"/status", StatusHandler),
            (r"/taxonomy_graphs", CreateTaxonomyGraphHandler),
            (r"/login", LoginHandler),
            (r"/callback/oauth", OauthCallbackHandler),
        ],
        **settings
    )


if __name__ == '__main__':
    options.parse_command_line()
    app = make_app()
    app.listen(options.port)
    print('Starting server on http://127.0.0.1:{port}'.format(port=options.port))

    try:
        IOLoop.instance().start()
    except KeyboardInterrupt:
        print('\nStopping server')
