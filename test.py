import sys
print(f"Python executable: {sys.executable}")
print(f"Python version: {sys.version}")

import tensorflow as tf
print(f"TF version: {tf.__version__}")

try:
    import pandas as pd
    print(f"Pandas version: {pd.__version__}")
    print(f"Pandas location: {pd.__file__}")
except ImportError as e:
    print(f"Pandas import error: {e}")