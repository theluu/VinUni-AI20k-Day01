"""
Day 1 — LLM API Foundation
AICB-P1: AI Practical Competency Program, Phase 1
"""

import os
import time
from typing import Any, Callable
from openai import OpenAI

COST_PER_1K_OUTPUT_TOKENS = {
    "gpt-4o": 0.010,
    "gpt-4o-mini": 0.0006,
}

OPENAI_MODEL = "gpt-4o"
OPENAI_MINI_MODEL = "gpt-4o-mini"


# ---------------------------------------------------------------------------
# Task 1 — Call GPT-4o
# ---------------------------------------------------------------------------
def call_openai(
    prompt: str,
    model: str = OPENAI_MODEL,
    temperature: float = 0.7,
    top_p: float = 0.9,
    max_tokens: int = 256,
) -> tuple[str, float]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    start = time.time()
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
    )
    latency = time.time() - start
    return response.choices[0].message.content, latency


# ---------------------------------------------------------------------------
# Task 2 — Call GPT-4o-mini
# ---------------------------------------------------------------------------
def call_openai_mini(
    prompt: str,
    temperature: float = 0.7,
    top_p: float = 0.9,
    max_tokens: int = 256,
) -> tuple[str, float]:
    return call_openai(prompt, model=OPENAI_MINI_MODEL, temperature=temperature,
                       top_p=top_p, max_tokens=max_tokens)


# ---------------------------------------------------------------------------
# Task 3 — Compare GPT-4o vs GPT-4o-mini
# ---------------------------------------------------------------------------
def compare_models(prompt: str) -> dict:
    gpt4o_response, gpt4o_latency = call_openai(prompt)
    mini_response, mini_latency = call_openai_mini(prompt)
    token_estimate = len(gpt4o_response.split()) / 0.75
    gpt4o_cost = (token_estimate / 1000) * COST_PER_1K_OUTPUT_TOKENS["gpt-4o"]
    return {
        "gpt4o_response": gpt4o_response,
        "mini_response": mini_response,
        "gpt4o_latency": gpt4o_latency,
        "mini_latency": mini_latency,
        "gpt4o_cost_estimate": gpt4o_cost,
    }


# ---------------------------------------------------------------------------
# Task 4 — Streaming chatbot with conversation history
# ---------------------------------------------------------------------------
def streaming_chatbot() -> None:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    history = []
    print("Chatbot ready. Type 'quit' or 'exit' to stop.")
    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() in ("quit", "exit"):
            break
        history.append({"role": "user", "content": user_input})
        stream = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=history,
            stream=True,
        )
        print("Assistant: ", end="", flush=True)
        assistant_reply = ""
        for chunk in stream:
            delta = chunk.choices[0].delta.content or ""
            print(delta, end="", flush=True)
            assistant_reply += delta
        print()
        history.append({"role": "assistant", "content": assistant_reply})
        history = history[-6:]  # keep last 3 turns (user + assistant = 2 messages each)


# ---------------------------------------------------------------------------
# Bonus Task A — Retry with exponential backoff
# ---------------------------------------------------------------------------
def retry_with_backoff(
    fn: Callable,
    max_retries: int = 3,
    base_delay: float = 0.1,
) -> Any:
    last_exc = None
    for attempt in range(max_retries + 1):
        try:
            return fn()
        except Exception as e:
            last_exc = e
            if attempt < max_retries:
                time.sleep(base_delay * (2 ** attempt))
    raise last_exc


# ---------------------------------------------------------------------------
# Bonus Task B — Batch compare
# ---------------------------------------------------------------------------
def batch_compare(prompts: list[str]) -> list[dict]:
    results = []
    for prompt in prompts:
        result = compare_models(prompt)
        result["prompt"] = prompt
        results.append(result)
    return results


# ---------------------------------------------------------------------------
# Bonus Task C — Format comparison table
# ---------------------------------------------------------------------------
def format_comparison_table(results: list[dict]) -> str:
    headers = ["Prompt", "GPT-4o Response", "Mini Response", "GPT-4o Latency", "Mini Latency"]
    rows = []
    for r in results:
        rows.append([
            r.get("prompt", "")[:40],
            r.get("gpt4o_response", "")[:40],
            r.get("mini_response", "")[:40],
            f"{r.get('gpt4o_latency', 0):.2f}s",
            f"{r.get('mini_latency', 0):.2f}s",
        ])
    col_widths = [max(len(h), max((len(row[i]) for row in rows), default=0))
                  for i, h in enumerate(headers)]
    sep = "+-" + "-+-".join("-" * w for w in col_widths) + "-+"
    fmt = "| " + " | ".join(f"{{:<{w}}}" for w in col_widths) + " |"
    lines = [sep, fmt.format(*headers), sep]
    for row in rows:
        lines.append(fmt.format(*row))
    lines.append(sep)
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Entry point for manual testing
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    test_prompt = "Explain the difference between temperature and top_p in one sentence."
    print("=== Comparing models ===")
    result = compare_models(test_prompt)
    for key, value in result.items():
        print(f"{key}: {value}")

    print("\n=== Starting chatbot (type 'quit' to exit) ===")
    streaming_chatbot()
