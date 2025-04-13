# 🛡️ AGNO PII Masking & Unmasking System

This project is a CLI-based Agentic AI system that performs **PII masking and unmasking** using:
- 🧠 `Presidio` (NER + Pattern-based detection)
- ✨ `Flair` (Deep learning-based NER)
- 📚 `Regex` (Custom patterns)
- 🗃️ `MongoDB` (for original PII mapping storage)
- 🧩 Built on the **Groq Agno framework** to support modular, reusable AI agents.

---

## 🚀 Features

- Mask sensitive PII from any `.txt` or `.pdf` file
- Unmask content using a unique `collection_id`
- Follows the `agno.agent.Agent` structure for future integration into LLM pipelines or workflows
- Stores and retrieves original values securely using MongoDB

---

## 🧠 Agents Implemented

| Agent             | Description |
|------------------|-------------|
| `PIIMaskingAgent` | Detects and replaces PII with unique tags. Stores original values in MongoDB. |
| `PIIUnmaskingAgent` | Replaces masked tokens with original PII using the collection ID. |

Each agent defines:
- `name`
- `role`
- `instructions`
- `run()` method

---

## 🛠️ Setup

Install dependencies:
```bash
pip install -r requirements.txt
