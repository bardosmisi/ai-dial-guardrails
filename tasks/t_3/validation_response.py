from pydantic import BaseModel, Field


class PIIValidationResponse(BaseModel):
    """Model for PII detection in LLM outputs."""
    contains_pii: bool = Field(description="True if PII detected in the text")
    pii_types: list[str] = Field(description="Types of PII found (e.g., ssn, credit_card, address)", default_factory=list)
    explanation: str = Field(description="What PII was detected and where in the text")
