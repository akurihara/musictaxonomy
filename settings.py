import os

import tornado
import tornado.options
from tornado.options import define

define('port', help='run on the given port', type=int)
tornado.options.parse_command_line()

settings = {
    # debug: If True the application runs in debug mode
    'debug': True,

    # gzip: If True, responses in textual formats will be gzipped automatically.
    'gzip': True,

    # log_function: This function will be called at the end of every request
    # to log the result (with one argument, the RequestHandler object).
    # The default implementation writes to the logging module's root logger.
    # May also be customized by overriding Application.log_request.
    # 'log_function': function_name,

    # ui_modules and ui_methods: http://www.tornadoweb.org/en/stable/overview.html#ui-modules

    # Used by RequestHandler.get_secure_cookie and set_secure_cookie to sign cookies.
    'cookie_secret': 'uxmRinfK8e7HC59jU4QKAGyEsnecPZHuVGUhmtAqHY5rdScC7FM',

    # login_url: The authenticated decorator will redirect to this url
    # if the user is not logged in. Can be further customized by
    # overriding RequestHandler.get_login_url
    # 'login_url': '/login/',

    # xsrf_cookies: If true, Cross-site request forgery protection will be enabled.
    'xsrf_cookies': False,

    # autoescape: Controls automatic escaping for templates.
    # May be set to None to disable escaping, or to the name of a function
    # that all output should be passed through.
    # 'autoescape': "xhtml_escape",

    # template_path: Directory containing template files.
    # Can be further customized by overriding RequestHandler.get_template_path
    'template_path': os.path.join(os.path.dirname(__file__), "templates"),

    # static_path: Directory from which static files will be served.
    'static_path': os.path.join(os.path.dirname(__file__), "static"),

    # static_url_prefix: Url prefix for static files, defaults to "/static/".
    # 'static_url_prefix': '/static/',
}


#
# Application Settings
#

# Spotify
SPOTIFY_CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET')

# Database
DATABASE_URL = os.environ.get('DATABASE_URL')
