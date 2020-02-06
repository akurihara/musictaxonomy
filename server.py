import os

from musictaxonomy.auth.handlers import LoginHandler, OauthCallbackHandler
from musictaxonomy.graph.handlers import TaxonomyGraphHandler
from musictaxonomy.handlers import IndexHandler, StatusHandler
from settings import settings
from tornado.ioloop import IOLoop
from tornado.options import options
from tornado.web import Application


def make_app():
    return Application(
        [
            (r"/", IndexHandler),
            (r"/status", StatusHandler),
            (r"/taxonomy_graphs", TaxonomyGraphHandler),
            (r"/login", LoginHandler),
            (r"/callback/oauth", OauthCallbackHandler),
        ],
        **settings
    )


if __name__ == "__main__":
    options.parse_command_line()

    # Prefer command line option, fallback to environment variable
    port = options.port if options.port else int(os.environ.get("PORT", 8080))
    app = make_app()
    app.listen(port)
    print("Starting server on http://127.0.0.1:{}".format(port))

    try:
        IOLoop.instance().start()
    except KeyboardInterrupt:
        print("\nStopping server")
