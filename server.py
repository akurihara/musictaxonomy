import os

from tornado.ioloop import IOLoop
from tornado.web import Application

from musictaxonomy.auth.handlers import LoginHandler, OauthCallbackHandler
from musictaxonomy.graph.handlers import CreateTaxonomyGraphHandler
from musictaxonomy.handlers import IndexHandler, StatusHandler
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
    port = int(os.environ.get('PORT', 8080))
    app = make_app()
    app.listen(port)
    print('Starting server on http://127.0.0.1:{}'.format(port))

    try:
        IOLoop.instance().start()
    except KeyboardInterrupt:
        print('\nStopping server')
