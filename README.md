# 🛡️ AGNO-PII-FINAL: Agentic AI System for PII Masking & Unmasking (Agno + MongoDB)

This project implements a modular, agent-based system for detecting, masking, and unmasking Personally Identifiable Information (PII) using the **Groq Agno framework**, **Presidio**, **Flair**, **Regex**, and **MongoDB**.

Built as part of an Agentic AI initiative, this solution uses CLI-driven input and leverages Groq's `agno.agent.Agent` class structure to modularize agents for future expansion or pipeline integration.

---

## 🧠 Agents Included

| Agent                    | Role                                                 |
|--------------------------|------------------------------------------------------|
| `PIIMaskingAgent`        | Detects PII (using Presidio, Flair, Regex) and replaces it with generated tokens. Stores original values in MongoDB. |
| `PIIUnmaskingAgent`      | Restores original values from MongoDB using masked token and collection ID. |
| `T&C Extraction Agent`   | Uses Groq LLaMA model to extract Terms & Conditions section from any PDF. |
| `Document Embedding Agent` | Embeds extracted T&C sections using `SentenceTransformer` and stores them in MongoDB for RAG-style retrieval. |

---

## 🏗️ Architecture (Agno)

This project follows the [Agno agent framework by Groq](https://github.com/groq/agno):

