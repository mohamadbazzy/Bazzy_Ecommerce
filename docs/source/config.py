import os
import sys
sys.path.insert(0, os.path.abspath('../../'))  # Adjust the path to include the project root

# Add extensions
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',  # Supports Google and NumPy style docstrings
    'sphinx_autodoc_typehints',  # Enhances type hint support
]

# Set the theme
html_theme = 'sphinx_rtd_theme'

# Project information
project = 'E-commerce API'
author = 'Your Name'
release = '1.0.0'

