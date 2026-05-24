import sys

try:
    import pyperclip
except ImportError:
    print("Error: The 'pyperclip' library is not installed.")
    print("Run: pip install pyperclip")
    sys.exit(1)

from ui.application import Application

def main():
    app = Application()
    app.run()

if __name__ == "__main__":
    main()