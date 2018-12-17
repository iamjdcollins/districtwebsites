#!/usr/bin/env python
import os
import sys
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


if __name__ == '__main__':
    os.environ.setdefault(
        'DJANGO_SETTINGS_MODULE',
        get_secret('DJANGO_SETTINGS_MODULE')
    )
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
