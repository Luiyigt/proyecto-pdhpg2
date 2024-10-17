import os
import sys
import webbrowser
from django.core.management import execute_from_command_line
import contextlib

# Suppress output when running the server to avoid AttributeError with NoneType write
@contextlib.contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pdhpg2.settings")
    
    # Open the browser automatically to the server's URL
    webbrowser.open('http://127.0.0.1:8000/')
    
    # Suppress server output and run the server
    with suppress_stdout():
        args = ["manage.py", "runserver", "--noreload", "127.0.0.1:8000"]
        execute_from_command_line(args)
