import os
from pathlib import Path
from collections import defaultdict
from write_the.utils import list_python_files


def write_the_mkdocs(code_dir: Path, readme: Path = None, project_name=None):
    """
    Generates a mkdocs.yml file and reference files for a project.
    Args:
      readme (Path): Path to the project's README.
      code_dir (Path): Path to the project's code directory.
      project_name (str, optional): Name of the project. Defaults to the name of the current working directory.
      force (bool, optional): If True, overwrite existing mkdocs.yml and index.md files. Defaults to False.
    Notes:
      If `project_name` is not provided, the name of the current working directory is used.
      If `force` is False, existing mkdocs.yml and index.md files will not be overwritten.
    Returns:
      None
    """
    files = list_python_files(code_dir)
    groups = [path.stem for path in code_dir.glob("*") if not path.stem.startswith("_")]

    if not project_name:
        project_name = code_dir.name
    mkdocs = mkdocs_template.format(project_name=project_name)
    references = defaultdict(list)
    for file in files:
        if file.name.startswith("_"):
            continue
        key = "index"
        for group in groups:
            if f"{code_dir.name}/{group}/" in str(file) or f"{code_dir.name}/{group}." in str(file):
                key = group
                break
        module = str(file).rstrip(".py").replace("/", ".")  # breaks on windows?
        references[key].append(f"::: {module}")

    reference_path = Path("./docs/reference/")
    reference_path.mkdir(parents=True, exist_ok=True)
    for doc in references:
        with open(f"{reference_path}/{doc}.md", "w") as f:
            for ref in references[doc]:
                f.write(ref + "\n\n")
    if readme:
        index_text = f"---\ntitle: Home\n---\n{readme.read_text()}"
        Path("./docs/index.md").write_text(index_text)
    if not Path("./mkdocs.yml").exists():
        Path("./mkdocs.yml").write_text(mkdocs)
    action_path = Path(".github/workflows/mkdocs.yml")
    if not action_path.exists():
        action_path.parent.mkdir(parents=True, exist_ok=True)
        action_path.write_text(action_template)


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
      name: Generate with write-the

plugins:
- search
- mkdocstrings
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