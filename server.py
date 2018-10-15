from tornado.ioloop import IOLoop
from tornado.options import options
from tornado.web import Application, RequestHandler

from auth.handlers import LoginHandler, SpotifyAuthorizeCallbackHandler
from graph.handlers import CreateTaxonomyGraphHandler, TaxonomyGraphExampleHandler
from settings import settings


class StatusHandler(RequestHandler):
    def get(self):
        response = {
            'message': 'ok',
            'status': 200,
            'version': '1.0.0',
        }
        self.write(response)


def make_app():
    return Application(
        [
            (r"/", StatusHandler),
            (r"/taxonomy_graphs", CreateTaxonomyGraphHandler),
            (r"/taxonomy_graphs/example", TaxonomyGraphExampleHandler),
            (r"/login", LoginHandler),
            (r"/callback", SpotifyAuthorizeCallbackHandler),
        ],
        **settings
    )


if __name__ == '__main__':
    options.parse_command_line()
    app = make_app()
    app.listen(options.port)
    print 'Starting server on http://127.0.0.1:{port}'.format(port=options.port)

    try:
        IOLoop.instance().start()
    except KeyboardInterrupt:
        print '\nStopping server'
