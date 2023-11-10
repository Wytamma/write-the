mkdocs_template = """
site_name: {project_name}
# repo_url: https://github.com/wytamma/write-the

theme:
  name: "material"
  # homepage: https://write-the.wytamma.com
  # logo: assets/logo.png
  # favicon: images/favicon.png
  palette: 
    - scheme: default
      toggle:
        icon: material/brightness-7 
        name: Switch to dark mode
    - scheme: slate
      toggle:
        icon: material/brightness-4
        name: Switch to light mode
  features:
    - toc.follow
    - content.action.edit

extra:
  social:
    - icon: fontawesome/solid/robot
      link: https://github.com/Wytamma/write-the
      name: Generated with write-the

plugins:
- search
- mkdocstrings:
    handlers:
      python:
        options:
          docstring_style: "google"

markdown_extensions:
  - pymdownx.highlight:
      anchor_linenums: true
      line_spans: __span
      pygments_lang_class: true
  - pymdownx.inlinehilite
  - pymdownx.snippets
  - pymdownx.superfences
"""

action_template = """
name: mkdocs 
on:
  push:
    branches:
      - master 
      - main
permissions:
  contents: write
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: 3.x
      - uses: actions/cache@v2
        with:
          key: ${{ github.ref }}
          path: .cache
      - run: pip install "mkdocstrings[python]" "mkdocs-material"
      - run: mkdocs gh-deploy --force
"""
