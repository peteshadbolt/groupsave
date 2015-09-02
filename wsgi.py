#!/usr/bin/python
import os

#virtenv = os.environ['OPENSHIFT_PYTHON_DIR'] + '/virtenv/'
#virtualenv = os.path.join(virtenv, 'bin/activate_this.py')
#try:
    #execfile(virtualenv, dict(__file__=virtualenv))
#except IOError:
    #pass

from flaskapp import app as application

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    httpd = make_server('localhost', 8051, application)
    # Serve forever
    httpd.serve_forever()
