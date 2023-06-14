---
title: Home
---
![](https://raw.githubusercontent.com/Wytamma/write-the/master/images/logo.png)

AI-powered Documentation and Test Generation Tool

[![PyPI - Version](https://img.shields.io/pypi/v/write-the.svg)](https://pypi.org/project/write-the)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/write-the.svg)](https://pypi.org/project/write-the)
[![write-the - docs](https://badgen.net/badge/write-the/docs/blue?icon=https://raw.githubusercontent.com/Wytamma/write-the/master/images/write-the-icon.svg)](https://write-the.wytamma.com/)
[![write-the - test](https://badgen.net/badge/write-the/tests/green?icon=https://raw.githubusercontent.com/Wytamma/write-the/master/images/write-the-icon.svg)](https://github.com/Wytamma/write-the/actions/workflows/tests.yml)
[![codecov](https://codecov.io/gh/Wytamma/write-the/branch/master/graph/badge.svg?token=yEDn56L76k)](https://app.codecov.io/gh/Wytamma/write-the/tree/master)
[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2FWytamma%2Fwrite-the&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false)](https://github.com/Wytamma/write-the)

Write-the is an AI-powered documentation and test generation tool that leverages GPTs to automatically write tests, generate documentation, and refactor code. It is designed to streamline the development process, improve code quality, and increase productivity.

![](https://raw.githubusercontent.com/Wytamma/write-the/master/images/write-the-docs.gif)

## Real-world examples

- [`write-the docs` to write the docs for the `write-the docs` command 🤖](https://github.com/Wytamma/write-the/blob/5d7a5a22d082be6ee870c694ef2d24e6d1610758/write_the/commands/docs/docs.py#L26)
- [`write-the mkdocs` to build the documentation site for `write-the` 🤖](https://write-the.wytamma.com/)
- [`write-the tests` to write tests for `write-the docs` 🤖](https://github.com/Wytamma/write-the/commit/6b6c8a08d7991e07e4972281c471f7842c04dda0)
- [`write-the docs` and `write-the mkdocs` to build documenation for `autoresearcher` 🤖](https://github.com/eimenhmdt/autoresearcher/pull/17)
- [`write-the docs` and `write-the mkdocs` to build documenation for `hyperspec` 🤖](https://github.com/smutch/hyperspec/pull/1)
- [`write-the docs` and `write-the mkdocs` to build documenation for `CUPCAKEAGI` 🤖](https://github.com/AkshitIreddy/CUPCAKEAGI/pull/4)

## Installation
```console
pip install write-the
```
## Features

Write-the offers the following AI-driven features:

- Write-the Docs: Automatically generate documentation for your codebase, including class and function descriptions, parameter explanations, and examples.
- Write-the Tests: Create test cases for your code, ensuring thorough test coverage and better code quality.
- Write-the Convert: Convert code and data from any format into another. 
- Write-the Refactor: Receive refactoring suggestions, reduce code complexity, optimize performance, and fix bugs (TBD).

## Requirements
- Python 3.9 or higher  
- OpenAI API key

## Usage

To use `write-the` you must set an OPENAI_API_KEY environment variable (e.g. `export OPENAI_API_KEY=...`).

### Docs:
```bash
write-the docs [OPTIONS] [PATH_TO_SOURCE_CODE]
```

![](https://raw.githubusercontent.com/Wytamma/write-the/master/images/docs-help.png)


### Mkdocs:
```bash
write-the mkdocs [OPTIONS] [PATH_TO_SOURCE_CODE]
```

![](https://raw.githubusercontent.com/Wytamma/write-the/master/images/mkdocs-help.png)


### Tests:
```bash
write-the tests [OPTIONS] [PATH_TO_SOURCE_CODE]
```

![](https://raw.githubusercontent.com/Wytamma/write-the/master/images/tests-help.png)


### Convert:
```bash
write-the convert [OPTIONS] IN_FILE [OUT_FILE]
```

![](https://raw.githubusercontent.com/Wytamma/write-the/master/images/convert-help.png)

For detailed information on available options and parameters, refer to the official (`write-the` generated) [documentation](https://write-the.wytamma.com/).

## Roadmap

The main goal for write-the is to develop a generic module system to document, test, and optimise code in any language in a reliable and repatable way.

For a detailed project roadmap, including planned features, improvements, and milestones, please see our Project Timeline (TBD).

## Contributing
We welcome contributions from the community. If you would like to contribute to Write-The, please follow these steps:

- Fork the repository and create a new branch for your feature or bugfix.
- Develop your changes and ensure that your code follows the project's coding standards.
- Create a pull request with a clear description of your changes and any relevant documentation.
- For more information on contributing, please see our Contributing Guide.

## License
`write-the` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.

