from pathlib import Path
from collections import defaultdict
from write_the.utils import list_python_files

from .templates import action_template, mkdocs_template


def write_the_mkdocs(
    code_dir: Path, readme: Path = None, out_dir: Path = Path("."), project_name=None
):
    """
    Generates a mkdocs project from a directory of python files.
    Args:
      code_dir (Path): The directory containing the python files.
      readme (Path, optional): The readme file to include in the project. Defaults to None.
      out_dir (Path, optional): The directory to write the project to. Defaults to the current directory.
      project_name (str, optional): The name of the project. Defaults to the name of the code_dir.
    Notes:
      If readme is not provided, the project will not have a home page.
      If project_name is not provided, the project will be named after the code_dir.
    Side Effects:
      Creates a mkdocs project in the out_dir.
      Creates a .github/workflows/mkdocs.yml file in the out_dir.
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
            if f"{code_dir.name}/{group}/" in str(
                file
            ) or f"{code_dir.name}/{group}." in str(file):
                key = group
                break
        module = str(file).rstrip(".py").replace("/", ".")  # breaks on windows?
        references[key].append(f"::: {module}")
    docs_dir = out_dir / "docs"
    reference_path = docs_dir / "reference"
    reference_path.mkdir(parents=True, exist_ok=True)
    for doc in references:
        with open(f"{reference_path}/{doc}.md", "w") as f:
            for ref in references[doc]:
                f.write(ref + "\n\n")
    if readme:
        index_text = f"---\ntitle: Home\n---\n{readme.read_text()}"
        (docs_dir / "index.md").write_text(index_text)
    if not (out_dir / "mkdocs.yml").exists():
        (out_dir / "mkdocs.yml").write_text(mkdocs)
    action_path = out_dir / ".github" / "workflows" / "mkdocs.yml"
    if not action_path.exists():
        action_path.parent.mkdir(parents=True, exist_ok=True)
        action_path.write_text(action_template)
