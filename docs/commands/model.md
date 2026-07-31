---
title: Mange OpenAI Models
---

# Mange the default model used by `write-the`

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

### OpenRouter

Use the `--list-open-router` flag to list all the OpenRouter models available. Search for specific company offerings by using the additional `--company` flag. 

```bash
write-the model --list-open-router --company google
```

Add the `--free` flag to show models without any cost.