# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import sys
from pathlib import Path

this_dir = Path(__file__).resolve().parent.parent
about = {}
with open(this_dir / "opsparser" / "__about__.py") as f:
    exec(f.read(), about)
__version__ = about["__version__"]

# include pkg root folder to sys.path
os.environ["PYTHONPATH"] = ":".join((str(this_dir), os.environ.get("PYTHONPATH", "")))
sys.path.append(str(this_dir))

project = "OpenSeesParser"
copyright = "2025, Lingyun Gou, Yexiang Yan"
author = "Lingyun Gou, Yexiang Yan"
release = __version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    'sphinx.ext.napoleon',
    "sphinx_autodoc_typehints",
    "sphinx.ext.mathjax",
    "sphinx.ext.viewcode",
    "sphinx_design",
    "sphinx.ext.autosummary",
    "nbsphinx",
    # "myst_nb",
    "jupyter_sphinx",
    "sphinx_copybutton",
]

# autodoc config
autodoc_default_options = {  
    'members': True,  
    'member-order': 'bysource',  
    'special-members': '__init__',  
    'undoc-members': True,  
    'exclude-members': '__weakref__'  
}  
autodoc_member_order = "bysource"
autodoc_typehints = "both"
autodoc_typehints_description_target = "documented_params"

# napoleon config
napoleon_google_docstring = True  
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_ivar = True

# nbsphinx config
nbsphinx_execute_arguments = [
    "--InlineBackend.figure_formats={'svg', 'pdf'}",
    "--InlineBackend.rc=figure.dpi=96",
]

# templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

sd_custom_directives = {
    "dropdown": {
        "inherit": "dropdown",
        "options": {
            "icon": "pencil",
            "class-container": "sn-dropdown-default",
        },
    }
}

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# html_theme = "sphinx_rtd_theme"
# html theme
html_theme = "furo"
html_static_path = ["_static"]
html_css_files = ["_css/shared.css"]
html_css_files += ["_css/furo.css"]
html_css_files += ["_css/notebook_scroll.css"]
# html_css_files += ["_css/collapse_output.css"]
html_favicon = "_static/logo.png"
html_theme_options = {
    "light_logo": "logo.png",  # add light mode logo
    "dark_logo": "logo_dark.png",  # add dark mode logo
    "sidebar_hide_name": True,  # hide the name of a project in the sidebar (already in logo)
    "source_repository": "https://github.com/SeismoExt/OpsParser",
    "source_branch": "master",
    "source_directory": "docs/",
    "top_of_page_buttons": ["view", "edit"],
}
templates_path = ["_templates/furo", "_templates"]
html_sidebars = {
    "**": [
        "sidebar/brand.html",
        "sidebar/search.html",
        "sidebar/scroll-start.html",
        "sidebar/navigation.html",
        "sidebar/ethical-ads.html",
        "sidebar/scroll-end.html",
        "side-github.html",
        "sidebar/variant-selector.html",
    ]
}
pygments_style = "gruvbox-light"
pygments_dark_style = "paraiso-dark"
