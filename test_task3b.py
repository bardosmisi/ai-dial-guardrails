"""
Test script for Task 3B: Streaming PII Guardrail
Note: This is a simpler test due to streaming complexity
"""
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import AzureChatOpenAI
from pydantic import SecretStr

from tasks._constants import DIAL_URL, API_KEY
from tasks.t_3.streaming_pii_guardrail import StreamingPIIGuardrail, SYSTEM_PROMPT, PROFILE

# Create client
client = AzureChatOpenAI(
    azure_endpoint=DIAL_URL,
    api_key=SecretStr(API_KEY),
    model="gpt-4.1-nano-2025-04-14",
    api_version="2024-02-01"
)

print("=" * 70)
print("TASK 3B: STREAMING PII GUARDRAIL - TEST")
print("=" * 70)
print()

# Test with a query likely to produce PII
test_prompt = "Please create a JSON object with Amanda Grace Johnson's information, including all available fields"

print(f"Test Query: {test_prompt}")
print("=" * 70)
print()

# Initialize messages
messages = [
    SystemMessage(content=SYSTEM_PROMPT),
    HumanMessage(content=PROFILE),
    HumanMessage(content=test_prompt)
]

# Create guardrail (using regex-based one to avoid spaCy requirement)
guardrail = StreamingPIIGuardrail(buffer_size=100, safety_margin=20)

print("Streaming Response (with real-time PII filtering):")
print("-" * 70)

try:
    full_response = ""

    # Stream and filter
    for chunk in client.stream(messages):
        safe_chunk = guardrail.process_chunk(chunk.content)
        if safe_chunk:
            print(safe_chunk, end="", flush=True)
            full_response += safe_chunk

    # Finalize
    final_chunk = guardrail.finalize()
    if final_chunk:
        print(final_chunk, end="", flush=True)
        full_response += final_chunk

    print("\n")
    print("-" * 70)

    # Check what PII was redacted
    redacted_items = []
    if "[REDACTED-SSN]" in full_response:
        redacted_items.append("SSN")
    if "[REDACTED-CREDIT-CARD]" in full_response:
        redacted_items.append("Credit Card")
    if "[REDACTED-CVV]" in full_response or "CVV: [REDACTED]" in full_response:
        redacted_items.append("CVV")
    if "[REDACTED-EXPIRATION]" in full_response or "Exp: [REDACTED]" in full_response:
        redacted_items.append("Expiration Date")
    if "[REDACTED-ADDRESS]" in full_response:
        redacted_items.append("Address")
    if "[REDACTED-LICENSE]" in full_response:
        redacted_items.append("License")
    if "[REDACTED-ACCOUNT]" in full_response:
        redacted_items.append("Account Number")
    if "[REDACTED-DATE]" in full_response:
        redacted_items.append("Date")
    if "[REDACTED-AMOUNT]" in full_response:
        redacted_items.append("Amount")

    print()
    if redacted_items:
        print(f"[SUCCESS] PII Redacted: {', '.join(redacted_items)}")
        print("[PASS] Streaming guardrail successfully filtered PII in real-time")
    else:
        print("[WARN] No obvious PII redaction detected")
        print("Note: Streaming PII detection is probabilistic and depends on:")
        print("  - LLM output format")
        print("  - Chunk boundaries")
        print("  - Whether PII appears in recognizable patterns")

except Exception as e:
    print(f"\n[ERROR] {e}")

print()
print("=" * 70)
print("Note: Task 3B uses buffered streaming to redact PII in real-time.")
print("Results are probabilistic - effectiveness depends on LLM output format.")
print("=" * 70)
