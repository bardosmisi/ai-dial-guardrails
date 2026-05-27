# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an educational Python project for learning AI guardrails implementation - specifically prompt injection defense and PII (Personally Identifiable Information) leak prevention. The project contains three progressive tasks that teach different guardrail techniques.

**Important Context:**
- All PII data in this project is **fake** and generated for educational purposes
- Uses `gpt-4.1-nano-2025-04-14` intentionally (more vulnerable to prompt injections for learning)
- Designed for EPAM internal use with DIAL API access
- Requires VPN connection to EPAM network

## Environment Setup

**Install dependencies:**
```bash
pip install -r requirements.txt
```

**Set DIAL API key:**
```bash
export DIAL_API_KEY="your-api-key-here"
```

**Required:** Python 3.11+

## Running Tasks

Each task is a standalone Python script:
```bash
# Task 1: Basic prompt injection defense
python tasks/t_1/prompt_injection.py

# Task 2: Input validation guardrail
python tasks/t_2/input_llm_based_validation.py

# Task 3A: Output validation
python tasks/t_3/output_llm_based_validation.py

# Task 3B: Streaming PII filtering
python tasks/t_3/streaming_pii_guardrail.py
```

## Architecture

**Configuration:**
- `tasks/_constants.py` - API configuration (DIAL_URL, API_KEY from env)

**Task Structure:**
1. **Task 1** (`t_1/prompt_injection.py`) - Demonstrates prompt injection attacks and system prompt hardening
2. **Task 2** (`t_2/input_llm_based_validation.py`) - Input validation using LLM to detect malicious prompts before processing
3. **Task 3** (`t_3/`) - Output protection with two approaches:
   - `output_llm_based_validation.py` - LLM-based validation of generated responses with blocking/soft filtering modes
   - `streaming_pii_guardrail.py` - Real-time PII redaction during streaming responses using Presidio or regex patterns

**Key Dependencies:**
- `langchain-community` & `langchain-openai` - LLM interaction, structured outputs via Pydantic
- `presidio-analyzer` & `presidio-anonymizer` - Microsoft's PII detection/redaction library
- Uses Azure OpenAI API format through DIAL proxy

**Validation Pattern:**
Tasks 2 and 3 use similar LLM-based validation pattern:
- Structured Pydantic models for validation responses
- `PydanticOutputParser` + `ChatPromptTemplate` chain
- Validation prompts detect malicious patterns or PII leaks

**Streaming Pattern (Task 3B):**
- Buffered chunk processing with configurable `buffer_size` and `safety_margin`
- Handles PII split across chunk boundaries
- Two implementations: `StreamingPIIGuardrail` (regex) and `PresidioStreamingPIIGuardrail` (NLP-based)

## Implementation Notes

- All tasks use AzureChatOpenAI client connecting to DIAL proxy at `https://ai-proxy.lab.epam.com`
- Profile data (Amanda Grace Johnson) is consistent across tasks with fake SSN, credit cards, etc.
- System prompts should be enhanced to resist manipulation
- Input validation must minimize false positives on legitimate queries
- Output validation supports both hard blocking and soft redaction modes
- Streaming guardrails are probabilistic - PII detection depends on LLM output format

## Reference

See `tasks/PROMPT_INJECTIONS_TO_TEST.md` for example prompt injection techniques to test against.
