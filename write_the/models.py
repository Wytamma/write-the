models = {
    # ───────────────────────────── GPT-4o family ───────────────────────────── #
    "gpt-4o": {
        "description": "Flagship multimodal GPT-4-level model (text, vision, audio).",
        "context_window": 128_000,
        "training_data": "Up to Jun 2024"
    },
    "chatgpt-4o-latest": {
        "description": "ChatGPT alias that always points to the latest gpt-4o.",
        "context_window": 128_000,
        "training_data": "Up to Jun 2024"
    },
    "gpt-4o-mini": {
        "description": "Smaller, lower-latency, lower-cost 4o variant (text & vision).",
        "context_window": 128_000,
        "training_data": "Up to Oct 2023"
    },
    "gpt-4o-audio-preview": {
        "description": "4o preview that accepts/returns audio as well as text.",
        "context_window": 128_000,
        "training_data": "Up to Oct 2023"
    },
    "gpt-4o-audio-preview-2024-12-17": {
        "description": "Dated audio-preview snapshot of gpt-4o.",
        "context_window": 128_000,
        "training_data": "Up to Oct 2023"
    },
    "gpt-4o-audio-preview-2024-10-01": {
        "description": "Earlier audio-preview snapshot of gpt-4o.",
        "context_window": 128_000,
        "training_data": "Up to Oct 2023"
    },
    "gpt-4o-mini-audio-preview": {
        "description": "Audio-enabled version of gpt-4o-mini.",
        "context_window": 128_000,
        "training_data": "Up to Oct 2023"
    },
    "gpt-4o-mini-audio-preview-2024-12-17": {
        "description": "Dated snapshot of gpt-4o-mini-audio-preview.",
        "context_window": 128_000,
        "training_data": "Up to Oct 2023"
    },

    # ───────────────────────────── GPT-4.1 family ──────────────────────────── #
    "gpt-4.1": {
        "description": "Long-context successor to 4o; up to 32 768 output tokens.",
        "context_window": 1_000_000,
        "training_data": "Up to Jun 2024"
    },
    "gpt-4.1-mini": {
        "description": "Cost-efficient small 4.1 model; matches or beats 4o.",
        "context_window": 1_000_000,
        "training_data": "Up to Jun 2024"
    },
    "gpt-4.1-nano": {
        "description": "Fastest, cheapest 4.1 variant; ideal for classification/autocomplete.",
        "context_window": 1_000_000,
        "training_data": "Up to Jun 2024"
    },

    # ───────────────────────────── GPT-4 / 4-Turbo / 4-preview ─────────────── #
    "gpt-4": {
        "description": "Stable GPT-4 alias (currently points to gpt-4-0613).",
        "context_window": 8_192,
        "training_data": "Up to Sep 2021"
    },
    "gpt-4-32k": {
        "description": "Legacy GPT-4 with 32 k context (points to gpt-4-32k-0613).",
        "context_window": 32_768,
        "training_data": "Up to Sep 2021"
    },
    "gpt-4-1106-preview": {
        "description": "First GPT-4 Turbo preview (JSON mode, reproducible outputs, etc.).",
        "context_window": 128_000,
        "training_data": "Up to Apr 2023"
    },
    "gpt-4-0125-preview": {
        "description": "Second GPT-4 Turbo preview; improved ‘laziness’ fix.",
        "context_window": 128_000,
        "training_data": "Up to Dec 2023"
    },
    "gpt-4-turbo-2024-04-09": {
        "description": "Production GPT-4 Turbo snapshot (cheaper, faster).",
        "context_window": 128_000,
        "training_data": "Up to Dec 2023"
    },
    "gpt-4-turbo": {
        "description": "Alias (gpt-4-turbo-preview / 4-turbo / 4t) → gpt-4-turbo-2024-04-09.",
        "context_window": 128_000,
        "training_data": "Up to Dec 2023"
    },

    # ───────────────────────────── GPT-4.5 preview ─────────────────────────── #
    "gpt-4.5-preview-2025-02-27": {
        "description": "Research preview of GPT-4.5 (128 k ctx, larger parameter count).",
        "context_window": 128_000,
        "training_data": "Up to Apr 2024"
    },
    "gpt-4.5-preview": {
        "description": "Alias to gpt-4.5-preview-2025-02-27.",
        "context_window": 128_000,
        "training_data": "Up to Apr 2024"
    },

    # ───────────────────────────── GPT-3.5 family ──────────────────────────── #
    "gpt-3.5-turbo": {
        "description": "Default GPT-3.5 Turbo (16 k ctx) alias → gpt-3.5-turbo-0125.",
        "context_window": 16_385,
        "training_data": "Up to Sep 2021"
    },
    "gpt-3.5-turbo-16k": {
        "description": "Explicit 16 k-context variant (legacy alias chatgpt-16k).",
        "context_window": 16_385,
        "training_data": "Up to Sep 2021"
    },
    "gpt-3.5-turbo-instruct": {
        "description": "Completions-endpoint version of 3.5; GPT-3-era capabilities.",
        "context_window": 4_096,
        "training_data": "Up to Sep 2021"
    },

    # ───────────────────────────── OpenAI o-series reasoning models ────────── #
    "o1": {
        "description": "First-generation reasoning model (agentic tool use).",
        "context_window": 128_000,
        "training_data": "Up to Oct 2023"
    },
    "o1-2024-12-17": {
        "description": "Dated snapshot of o1 (same capabilities).",
        "context_window": 128_000,
        "training_data": "Up to Oct 2023"
    },
    "o1-preview": {
        "description": "Early preview alias for o1.",
        "context_window": 128_000,
        "training_data": "Up to Oct 2023"
    },
    "o1-mini": {
        "description": "Smaller, cheaper o1 variant.",
        "context_window": 128_000,
        "training_data": "Up to Oct 2023"
    },
    "o3": {
        "description": "Second-generation reasoning model (best overall reasoning; full tool access).",
        "context_window": 128_000,
        "training_data": "Up to Jun 2024"
    },
    "o3-mini": {
        "description": "Compact o3 variant for high-throughput reasoning.",
        "context_window": 128_000,
        "training_data": "Up to Jun 2024"
    },
    "o4-mini": {
        "description": "Newest small reasoning model; faster & cheaper than o3-mini.",
        "context_window": 128_000,
        "training_data": "Up to Jun 2024"
    }
}
