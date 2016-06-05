#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
    ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
    SRC_PATH = os.path.join(ROOT_PATH, 'src')
    CONF_PATH = os.path.join(ROOT_PATH, 'conf')

    sys.path.insert(0, SRC_PATH)
    sys.path.insert(0, CONF_PATH)

