---
title: "T3AS — Prerequisites Custom LLM"
description: "T3AS — Prerequisites Custom LLM."
keywords:
  - "TYPO3"
  - "T3Planet"
sidebarTitle: "T3AS"
---

## Recommended AI Models Matrix

| TYPO3 Pages | LLM (On-Prem) | LLM (Cloud) | Embedding Model | Vector DB | Hardware Notes |
| --- | --- | --- | --- | --- | --- |
| 1K – 5K pages | Mistral-7B, Llama 3 8B, Gemma 7B, Ollama’s GPT:OSS-120B | GPT-3.5, Claude Haiku, Gemini Pro | all-MiniLM-L6-v2 | ChromaDB, Pinecone | 16 GB RAM, 4+ cores (GPU optional) |
| 5K – 20K pages | Llama 3 8B, Mistral-7B, Llama 3 70B, Ollama’s GPT:OSS-120B | GPT-4, Claude Sonnet | text-embedding-3-small | ChromaDB, Pinecone | 32 GB RAM, GPU 8–24 GB VRAM |
| 20K+ pages | Llama 3 70B, Mistral 8x7B, Ollama’s GPT:OSS-120B | GPT-4o, Claude Opus, Gemini Ultra | text-embedding-3-large | Pinecone, ChromaDB | 64 GB+ RAM, GPU 24+ GB VRAM |

## Supported AI Providers and Models

| Provider | Category | Models |
| --- | --- | --- |
| OpenAI | openai | gpt-5, nova-2-lite, gpt-4.1, gpt-4o, gpt-4, gpt-3.5-turbo |
| Anthropic (Claude) | claude | claude-3.5-sonnet-latest, claude-3.5-haiku-latest, claude-3-opus-latest |
| Google (Gemini) | gemini | gemini-1.5-pro, gemini-1.5-flash, gemini-2.0-flash, gemini-2.0-flash-lite, gemini-2.0-pro-exp |
| Mistral | mistral | mistral-large-latest |
| Custom LLM | customllm | User-defined (when enable_custom_llm_model is enabled) |

## Prerequisites of Hardware & Software

### Server Requirements

- **OS:** Ubuntu 20.04+ (Linux)
- **CPU:** 4+ cores
- **RAM:** 16 GB minimum (32+ GB recommended)
- **Disk:** 100 GB free + 10–100 GB storage for embeddings
- **GPU:** Based on model matrix above

### System Access

- SSH access (terminal)
- Admin/root rights to install software & Docker

### TYPO3 Access

- TYPO3 Backend System Administrator access

### Network & Security

- Open ports (e.g., 8000, 443)
- SSL/TLS for public endpoints
- Firewall as required

### Required Software

- Python 3.8+ with pip
- Docker
- NVIDIA GPU drivers + CUDA (if GPU used)
- Python packages: - torch - transformers - sentence-transformers - others as required

### Vector Database (Embedding/Search)

- **Local:** ChromaDB (recommended)
- **Cloud-managed:** Pinecone (recommended for large scale)

# T3AS – Scope of Work (SOW) Custom AI LLM Integration

## Scope Overview

- Installation of LLM Model
- Installation of required software & libraries
- Pre-processing: chunking + embedding of all content
- Secure embedding storage in:
  - On-prem: ChromaDB
  - Cloud: Pinecone
- Deployment of on-prem open-source LLMs for RAG
- Secure, documented FastAPI delivery
- Daily/weekly incremental updates
- Admin documentation
- Onboarding & training

## Workflow & Implementation Steps

1. **Automated Ingestion** - Retrieve content from TYPO3 Database - Schedule recurring updates
2. **Data Processing & Embedding** - Pre-process and chunk data - Generate semantic embeddings
3. **Vector Database Integration** - Store embeddings in:
  - ChromaDB (on-prem)
  - Pinecone (cloud, if needed)
4. **LLM Deployment & API Layer**
5. **Training & Handover** - Admin/technical guide - Live training - Go-live support
