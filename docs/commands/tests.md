---
title: Tests
---

# Automatically generate test cases for your codebase using AI

You can use the `write-the tests` command to automatically generate test cases for your codebase. The tests will use the `pytest` framework.

```bash
write-the tests [OPTIONS] [PATH_TO_SOURCE_CODE]
```

The write-the tests command will generate test cases for all the functions in the specified directory that are not already tested. By default the tests will be printed to the console, you can use the `--save` flag to write the tests to the `--out` directory (default is `tests`).

```bash
write-the tests --save write_the
```