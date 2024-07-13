"""
Invokes the mediadata application when executed from the command line.

python -m mediadata
"""

from mediadata.core import management

if __name__ == "__main__":
    management.execute()
