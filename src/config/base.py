import os

DATABASE_NAME = os.getenv('POSTGRES_DB', 'test_db')
DATABASE_USER = os.getenv('POSTGRES_USER', 'postgres')
DATABASE_PASSWORD = os.getenv('POSTGRES_PASSWORD', '')
DATABASE_HOST = os.getenv('POSTGRES_HOST', 'localhost')
DATABASE_PORT = os.getenv('POSTGRES_PORT', 5432)

BASE_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..')

STATIC_ROOT = os.path.abspath(os.path.join(BASE_DIR, 'static/'))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
