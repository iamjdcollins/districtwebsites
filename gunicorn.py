import glob
import multiprocessing
import os
import json

from django.core.exceptions import ImproperlyConfigured

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# Load Secrets
def load_secrets(file=os.path.join(BASE_DIR, '.secrets.json')):
    try:
        with open(file) as f:
            secrets = json.loads(f.read())
            return secrets
    except FileNotFoundError:
        raise ImproperlyConfigured(
            'Secrets file not found. Please create the secrets file or correct'
            ' the configuration.'
        )


secrets = load_secrets()


# Get a secret
def get_secret(key, secrets=secrets or load_secrets()):
    try:
        val = secrets[key]
        if val == 'True':
            val = True
        elif val == 'False':
            val = False
        return val
    except KeyError:
        error_msg = (
            "ImproperlyConfigured: Set {0} environment variable"
        ).format(key)
        raise ImproperlyConfigured(error_msg)


def watch_extra_files():
    files = set()
    patterns = [
        {'path': '**/*.html', 'recursive': True, },
        {'path': '**/*.py', 'recursive': True, },
    ]
    for pattern in patterns:
        files = files.union(glob.glob(pattern['path'], recursive=pattern[
            'recursive']))
    return files

proc_name = 'districtwebsites'
pidfile = '/run/gunicorn/districtwebsites.pid'
worker_tmp_dir = '/srv/gunicorn/districtwebsites'
bind = 'unix:/run/gunicorn/districtwebsites.sock'
workers = multiprocessing.cpu_count() * 3 + 1
worker_class = 'gevent'
timeout = 3600
raw_env = [
    'DJANGO_SETTINGS_MODULE={0}'.format(get_secret('DJANGO_SETTINGS_MODULE')),
]
reload = get_secret('GUNICORN_RELOAD')
if reload:
    reload_extra_files = watch_extra_files()

