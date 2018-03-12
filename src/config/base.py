import os

DATABASE_NAME = os.getenv('DATABASE_NAME', 'test_db')
DATABASE_USER = os.getenv('DATABASE_USER', 'postgres')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD', '')
DATABASE_HOST = os.getenv('DATABASE_HOST', 'localhost')
DATABASE_PORT = os.getenv('DATABASE_PORT', 6543)

BASE_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..')

STATIC_ROOT = os.path.abspath(os.path.join(BASE_DIR, 'static/'))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
