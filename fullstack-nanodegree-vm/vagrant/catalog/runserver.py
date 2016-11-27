"""
This script runs the catalog application using a development server.
"""

from os import environ
from catalog import app

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    app.run(HOST, 53224)
