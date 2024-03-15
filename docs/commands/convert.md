---
title: Convert
---
# Convert code and data from any format into another using AI

You can use the `write-the convert` command to convert code and data from any format into another.

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
write-the convert \
  tests/data/multiply.py \
  multiply.rs \
  -o "Verbose Rust with lots of comments" 
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