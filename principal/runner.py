import sys
import os
from streamlit.web import cli as stcli

sys.argv = ["streamlit", "run", "Estatística.py"]
sys.exit(stcli.main())
