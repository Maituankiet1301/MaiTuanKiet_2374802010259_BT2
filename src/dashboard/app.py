"""
Streamlit Dashboard module entrypoint
"""
import os
import sys

# Chuyen huong ve app.py goc o thu muc du an
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, base_dir)

import app

if __name__ == "__main__":
    pass
