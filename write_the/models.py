models = {
    "gpt-4-0125-preview": {
        "description": "New GPT-4 Turbo intended to reduce cases of 'laziness'. Returns a maximum of 4,096 output tokens.",
        "context_window": 128000,
        "training_data": "Up to Dec 2023"
    },
    "gpt-4-turbo-preview": {
        "description": "Currently points to gpt-4-0125-preview.",
        "context_window": 128000,
        "training_data": "Up to Dec 2023"
    },
    "gpt-4-1106-preview": {
        "description": "GPT-4 Turbo model featuring improved instruction following, JSON mode, reproducible outputs, parallel function calling, and more. Returns a maximum of 4,096 output tokens. This is a preview model.",
        "context_window": 128000,
        "training_data": "Up to Apr 2023"
    },
    "gpt-4-vision-preview": {
        "description": "GPT-4 with the ability to understand images, in addition to all other GPT-4 Turbo capabilities. Currently points to gpt-4-1106-vision-preview.",
        "context_window": 128000,
        "training_data": "Up to Apr 2023"
    },
    "gpt-4-1106-vision-preview": {
        "description": "GPT-4 with the ability to understand images, in addition to all other GPT-4 Turbo capabilities. Returns a maximum of 4,096 output tokens. This is a preview model version.",
        "context_window": 128000,
        "training_data": "Up to Apr 2023"
    },
    "gpt-4": {
        "description": "Currently points to gpt-4-0613. See continuous model upgrades.",
        "context_window": 8192,
        "training_data": "Up to Sep 2021"
    },
    "gpt-4-0613": {
        "description": "Snapshot of gpt-4 from June 13th 2023 with improved function calling support.",
        "context_window": 8192,
        "training_data": "Up to Sep 2021"
    },
    "gpt-4-32k": {
        "description": "Currently points to gpt-4-32k-0613. This model was never rolled out widely in favor of GPT-4 Turbo.",
        "context_window": 32768,
        "training_data": "Up to Sep 2021"
    },
    "gpt-4-32k-0613": {
        "description": "Snapshot of gpt-4-32k from June 13th 2023 with improved function calling support. This model was never rolled out widely in favor of GPT-4 Turbo.",
        "context_window": 32768,
        "training_data": "Up to Sep 2021"
    },
    "gpt-3.5-turbo-0125": {
        "description": "New Updated GPT 3.5 Turbo with higher accuracy at responding in requested formats and a fix for a bug which caused a text encoding issue for non-English language function calls. Returns a maximum of 4,096 output tokens.",
        "context_window": 16385,
        "training_data": "Up to Sep 2021"
    },
    "gpt-3.5-turbo": {
        "description": "Currently points to gpt-3.5-turbo-0613. The gpt-3.5-turbo model alias will be automatically upgraded from gpt-3.5-turbo-0613 to gpt-3.5-turbo-0125 on February 16th.",
        "context_window": 4096,
        "training_data": "Up to Sep 2021"
    },
    "gpt-3.5-turbo-1106": {
        "description": "GPT-3.5 Turbo model with improved instruction following, JSON mode, reproducible outputs, parallel function calling, and more. Returns a maximum of 4,096 output tokens.",
        "context_window": 16385,
        "training_data": "Up to Sep 2021"
    },
    "gpt-3.5-turbo-instruct": {
        "description": "Similar capabilities as GPT-3 era models. Compatible with legacy Completions endpoint and not Chat Completions.",
        "context_window": 4096,
        "training_data": "Up to Sep 2021"
    },
    "gpt-3.5-turbo-16k": {
        "description": "Legacy Currently points to gpt-3.5-turbo-16k-0613.",
        "context_window": 16385,
        "training_data": "Up to Sep 2021"
    },
    "gpt-3.5-turbo-0613": {
        "description": "Legacy Snapshot of gpt-3.5-turbo from June 13th 2023. Will be deprecated on June 13, 2024.",
        "context_window": 4096,
        "training_data": "Up to Sep 2021"
    },
    "gpt-3.5-turbo-16k-0613": {
        "description": "Legacy Snapshot of gpt-3.5-16k-turbo from June 13th 2023. Will be deprecated on June 13, 2024.",
        "context_window": 16385,
        "training_data": "Up to Sep 2021"
    },
}