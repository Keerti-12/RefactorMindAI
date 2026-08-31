# RefactorMind AI 🧠⚙️

> *"RefactorMind modernizes legacy Java code and unlike every other tool, it proves the modernized code still behaves identically to the original — and hard-blocks any change that doesn't."*

## Status: Phase 1 Complete — Visual Graph UI In Progress

---

## 🚨 The Problem

Enterprise legacy Java codebases are brittle, undocumented, and expensive to modify. Developers face one fundamental fear: **"If I change this code, what else might I break?"**

Existing tools fall short — static tools can't handle semantic refactoring, and LLM generators can't guarantee behavior is preserved.

---

## 💡 What We've Built

A **code intelligence graph engine** that parses any Java repository and maps its entire structure — files, classes, interfaces, methods, constructors, fields, and every relationship between them — into a queryable graph.

> *You cannot safely refactor what you don't understand. RefactorMind builds the understanding first.*

---

## 💡 Our Innovation: Understand First, Refactor Safely

RefactorMind is built on a simple but powerful principle: **you cannot safely refactor what you don't understand.**

Before any refactoring begins, RefactorMind builds a complete structural understanding of your codebase — a visual, interactive code intelligence graph that maps every file, class, method, field, and the relationships between them. From there, refactoring happens incrementally, one method at a time, with behavioral verification at every step.

**AI proposes. Engineering constrains. Testing verifies. The system decides.**

---

## 📈 Graph Engine

RefactorMind parses your entire Java repository using JavaParser and builds a semantic dependency graph:

- **Nodes:** Files, Classes, Interfaces, Methods, Constructors, Fields
- **Edges:** CONTAINS, CALLS, DEPENDS_ON, IMPORTS, EXTENDS, IMPLEMENTS

This graph answers questions like: *"If I change this method, what else breaks?"* — deterministically, with zero LLM tokens.

---

## 🛠️ Tech Stack

| Layer                        | Technology                                             |
| ---------------------------- | ------------------------------------------------------ |
| AST parsing + graph building | JavaParser                                             |
| Static analysis              | PMD                                                    |
| LLM inference                | Groq API — Qwen3-27B (primary), GPT-OSS-20B (fallback) |
| Backend                      | Django + Celery + Redis                                |
| Frontend                     | Next.js                                                |
| Storage                      | PostgreSQL                                             |
| Infrastructure               | Docker Compose, GitHub Actions                         |

---

*AI proposes. Engineering constrains. Testing verifies. The system decides.*
