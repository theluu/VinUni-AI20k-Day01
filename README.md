# Day 1 — LLM API Foundation

**AICB-P1: AI Practical Competency Program, Phase 1**

## Cài đặt

```bash
# Tạo virtual environment và cài dependencies
python3 -m venv venv
venv/bin/pip install -r requirements.txt

# Thiết lập API key
export OPENAI_API_KEY="sk-..."
```

---

## Chạy kiểm thử

```bash
venv/bin/python -m pytest tests/ -v
```

Tất cả 19 tests dùng mock — không cần API key thật.

---

## Test thủ công từng task

Mở Python shell:

```bash
OPENAI_API_KEY="sk-..." venv/bin/python
```

**Task 1 — GPT-4o:**
```python
from solution.solution import call_openai
text, latency = call_openai("What is 2+2?")
print(text, latency)
```

**Task 2 — GPT-4o-mini:**
```python
from solution.solution import call_openai_mini
text, latency = call_openai_mini("What is 2+2?")
print(text, latency)
```

**Task 3 — So sánh 2 models:**
```python
from solution.solution import compare_models
result = compare_models("Explain gravity in one sentence.")
for k, v in result.items():
    print(f"{k}: {v}")
```

**Task 4 — Streaming chatbot:**
```python
from solution.solution import streaming_chatbot
streaming_chatbot()
# Gõ câu hỏi, token hiện ra từng chữ. Gõ 'quit' để thoát.
```

---

## Cấu trúc dự án

```
├── solution/
│   ├── solution.py       # Bài làm hoàn chỉnh
│   └── exercises.md      # Câu trả lời lý thuyết
├── tests/
│   └── test_solution.py  # Test suite (19 tests)
├── template.py           # Template gốc
├── conftest.py           # Fix Python 3.14 mock patch compatibility
└── requirements.txt
```

---

## Kết quả

| Task | Mô tả | Kết quả |
|------|-------|---------|
| Task 1 | `call_openai` — gọi GPT-4o, trả về `(text, latency)` | 3/3 tests pass |
| Task 2 | `call_openai_mini` — gọi GPT-4o-mini | 3/3 tests pass |
| Task 3 | `compare_models` — so sánh 2 models + ước tính chi phí | 4/4 tests pass |
| Task 4 | `streaming_chatbot` — streaming CLI, giữ 3 lượt gần nhất | 2/2 tests pass |
| Bonus A | `retry_with_backoff` — exponential backoff | 3/3 tests pass |
| Bonus B | `batch_compare` — xử lý nhiều prompt | 2/2 tests pass |
| Bonus C | `format_comparison_table` — xuất bảng so sánh | 2/2 tests pass |

**Tổng: 19/19 tests pass**
