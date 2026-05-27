from pydantic import BaseModel, Field


class ValidationResponse(BaseModel):
    """Model for input validation results."""
    is_safe: bool = Field(description="True if input is safe, False if malicious")
    reason: str = Field(description="Explanation of the decision")
    threat_type: str | None = Field(description="Type of threat detected (e.g., prompt_injection, jailbreak, pii_extraction)", default=None)
