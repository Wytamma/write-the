![](https://raw.githubusercontent.com/Wytamma/write-the/master/images/logo.png)

AI-powered python code documentation and test generation tool

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

## Requirements
- Python 3.9 or higher  
- OpenAI API key

## Usage

To use `write-the` you must set an OPENAI_API_KEY environment variable (e.g. `export OPENAI_API_KEY=...`).

### Docs:

Add google style docstrings to you Python code with AI.

```bash
write-the docs [OPTIONS] [PATH_TO_SOURCE_CODE]
```

By default the `write-the docs` command will add docstrings to all the `nodes` in the source code that are not already documented. 

```bash
write-the docs write_the
```

#### Save 
By default the docstrings will be printed to the console, you can use the `--save` flag to write the docstrings to the source code.

```bash
write-the docs --save write_the
```

#### Generate docs for specific nodes

A node is a function, class or class.method block. You can use the `--node` (`-n`) flag to specify which nodes to document (this will overwrite existing docstrings). 

```bash
write-the docs -n function_name -n class_name -n class.method_name write_the
```

#### Force and Update

You can also use the `--force` flag to overwrite all existing docstrings in the specified folder or file.

```bash
write-the docs --force write_the/some_file.py
```

You can use the `--update` flag to update existing docstrings. For example the command that was used to update the docstrings in the `write-the` codebase in [this commit](https://github.com/Wytamma/write-the/commit/862928a4467b9afd30443fc2332384c88c780d24) was:

```bash
write-the docs --update --save write_the
```

### Model 

View and set the default model that `write-the` uses to generate documentation and tests.

```bash
write-the model [OPTIONS] [DESIRED_MODEL] 
```

The default model that `write-the` uses to generate documentation and tests is `gpt-3.5-turbo-instruct`.

You can also use the `write-the model <desired_model>` command to set the default model that `write-the` uses to generate documentation and tests. 

```bash
write-the model gpt-4
```

Use the `--list` flag to view all available models.

```bash
write-the model --list
```

### MkDocs:

Generate a Markdown based [MkDocs website with material theme](https://squidfunk.github.io/mkdocs-material/) for a project including an API reference page.

```bash
write-the mkdocs [OPTIONS] [PATH_TO_SOURCE_CODE]
```

The `write-the mkdocs` command will generate a `mkdocs.yml` file and a `docs` folder in the specified directory. In addition a github action workflow file will be generated to automatically build and deploy the documentation to github pages. The `--readme` flag can be used to specify the path to the readme file that will be used as the homepage for the documentation site.

```bash
write-the mkdocs write_the --readme README.md
```
The above command will generate the following file structure:

```bash
.
├── mkdocs.yml
├── docs
│   ├── index.md
│   └── reference
│       ├── cli.md
│       ├── commands.md
│       ├── cst.md
│       ├── errors.md
│       ├── llm.md
│       ├── models.md
│       └── utils.md
└── .github
    └── workflows
        └── mkdocs.yml
```

You can see the documentation site that was generated for the `write-the` codebase [here](https://write-the.wytamma.com/).

### Tests:

Automatically generate test cases for your codebase using AI.

```bash
write-the tests [OPTIONS] [PATH_TO_SOURCE_CODE]
```

The write-the tests command will generate test cases for all the functions in the specified directory that are not already tested. By default the tests will be printed to the console, you can use the `--save` flag to write the tests to the `--out` directory (default is `tests`).

```bash
write-the tests --save write_the
```

### Convert:

Convert code and data from any format into another using AI.

```bash
write-the convert [OPTIONS] IN_FILE [OUT_FILE]
```

By default the `write-the convert` command will convert the input file to the output file format using the file extension to determine the input and output format. You can use the `--force` flag to overwrite the output file if it already exists.

```bash
write-the convert tests/data/multiply.py multiply.rs
```
```console
$ cat multiply.rs
fn multiply(a: i32, b: i32) -> i32 {
    a * b
}
```

To give the llm model a hint about the input and output format you can use the `--input-format` and `--output-format` flags.

```bash
write-the convert tests/data/multiply.py multiply.rs -o "Verbose Rust with lots of comments" 
```
```console
$ cat multiply.rs
// This is a function named 'multiply' that takes two parameters, 'a' and 'b'.
// Both 'a' and 'b' are of type i32, which is a 32-bit integer.
// The function returns a value of type i32.
fn multiply(a: i32, b: i32) -> i32 {
    // The function body consists of a single expression, 'a * b'.
    // This expression multiplies 'a' by 'b' and returns the result.
    // In Rust, the last expression in a function is automatically returned.
    a * b
}
```

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

