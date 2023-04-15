import os


def main():
    """Run telegram bot."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_layer.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            'available on your PYTHONPATH environment variable? Did you '
            'forget to activate a virtual environment?'
        ) from exc
    execute_from_command_line(['manage.py', 'runbot'])


if __name__ == '__main__':
    main()
