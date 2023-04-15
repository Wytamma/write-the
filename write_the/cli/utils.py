def list_python_files(directory):
    python_files = []

    for file in directory.glob('**/*.py'):
        python_files.append(file)

    return python_files
