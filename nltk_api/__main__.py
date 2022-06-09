import os
from gevent.pywsgi import WSGIServer
from nltk_api.application import app


def main():
    port = 5000
    try:
        port = int(os.environ['APP_PORT'])
    except (ValueError, KeyError):
        print(f'Environment variable for APP_PORT is not defined. Using the default port:{port}')

    http_server = WSGIServer(('', port), app)
    http_server.serve_forever()
    pass

if __name__ == '__main__':
    main()
