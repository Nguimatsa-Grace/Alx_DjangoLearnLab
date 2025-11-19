#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

# --- CRITICAL FIX START ---
# Force the current directory onto the path so Python can find nested modules like 'core_config'.
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
# --- CRITICAL FIX END ---


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core_config.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()