---
title: Home
---
![](https://raw.githubusercontent.com/Wytamma/write-the/master/images/logo.png)

AI-powered python code documentation and test generation tool

[![PyPI - Version](https://img.shields.io/pypi/v/write-the.svg)](https://pypi.org/project/write-the)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/write-the.svg)](https://pypi.org/project/write-the)
[![write-the - docs](https://badgen.net/badge/write-the/docs/blue?icon=https://raw.githubusercontent.com/Wytamma/write-the/master/images/write-the-icon.svg)](https://write-the.wytamma.com/)
[![write-the - test](https://badgen.net/badge/write-the/tests/green?icon=https://raw.githubusercontent.com/Wytamma/write-the/master/images/write-the-icon.svg)](https://github.com/Wytamma/write-the/actions/workflows/tests.yml)
[![codecov](https://codecov.io/gh/Wytamma/write-the/branch/master/graph/badge.svg?token=yEDn56L76k)](https://app.codecov.io/gh/Wytamma/write-the/tree/master)

Write-the is an AI-powered documentation and test generation tool that leverages Generative Pre-trained Transformers (GPTs) / Large Language Models (LLMs) to automatically write tests, generate documentation, and refactor code. It is designed to streamline the development process, improve code quality, and increase productivity.

![](https://raw.githubusercontent.com/Wytamma/write-the/master/images/write-the-docs.gif)

## Real-world examples

- [`write-the docs` to write the docs for the `write-the docs` command 🤖](https://github.com/Wytamma/write-the/blob/5d7a5a22d082be6ee870c694ef2d24e6d1610758/write_the/commands/docs/docs.py#L26)
- [`write-the mkdocs` to build the documentation site for `write-the` 🤖](https://write-the.wytamma.com/)
- [`write-the tests` to write tests for `write-the docs` 🤖](https://github.com/Wytamma/write-the/commit/6b6c8a08d7991e07e4972281c471f7842c04dda0)
- [`write-the docs` and `write-the mkdocs` to build documenation for `autoresearcher` 🤖](https://github.com/eimenhmdt/autoresearcher/pull/17)
- [`write-the docs` and `write-the mkdocs` to build documenation for `CUPCAKEAGI` 🤖](https://github.com/AkshitIreddy/CUPCAKEAGI/pull/4)

## Installation
```console
pip install write-the
```

`write-the` should ideally be installed in an isolated enviroment with a tool like [`pipx`](https://github.com/pypa/pipx).

```console
pipx install write-the
```

## Features

Write-the offers the following AI-driven features:

- [Write-the Docs](https://write-the.wytamma.com/commands/docs/): Automatically generate documentation for your codebase, including class and function descriptions, parameter explanations, and examples.
- [Write-the Tests](https://write-the.wytamma.com/commands/tests/): Create test cases for your code, ensuring thorough test coverage and better code quality.
- [Write-the Convert](https://write-the.wytamma.com/commands/convert/): Convert code and data from any format into another. 

In addition write-the can also [manage OpenAI models](https://write-the.wytamma.com/commands/model/) and [scaffold MkDocs websites](https://write-the.wytamma.com/commands/mkdocs/).

## Requirements
- Python 3.9 or higher  
- OpenAI API key

!!! note

    To use `write-the` you must set an `OPENAI_API_KEY` environment variable (e.g. `export OPENAI_API_KEY=...`).

See [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys) for details.

## Documentation

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

