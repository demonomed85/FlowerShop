#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import threading
import asyncio
from django.core.management import execute_from_command_line

#from myshop.TG_bot.tg_manager_bot import start_bot


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc


#def run_bot():
#    asyncio.run(start_bot())

#    t = threading.Thread(target=run_bot)
#    t.start()

# Запуск бота
# asyncio.run(start_bot())

# Запуск Django
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()