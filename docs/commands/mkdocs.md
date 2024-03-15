---
title: MkDocs website
---

# Use write-the to generate a fully featured MkDocs website for your project

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
