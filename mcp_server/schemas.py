from pydantic import BaseModel, Field
from typing import List, Dict, Optional


class ValidateInputRequest(BaseModel):
    text: str = Field(..., description="Text to validate for security issues")


class ValidateInputResponse(BaseModel):
    is_safe: bool
    violations: List[Dict[str, str]]
    risk_score: int
    total_violations: int


class DetectAttackRequest(BaseModel):
    text: str = Field(..., description="Text to check for attack patterns")


class DetectAttackResponse(BaseModel):
    is_attack: bool
    attack_types: List[str]
    detections: List[Dict[str, str]]
    risk_score: int
    total_detections: int


class SanitizeInputRequest(BaseModel):
    text: str = Field(..., description="Text to sanitize")
    redact_secrets: bool = Field(default=True, description="Redact secrets")
    redact_ips: bool = Field(default=True, description="Redact internal IPs")
    redact_pii: bool = Field(default=False, description="Redact PII")
    redact_domains: bool = Field(default=True, description="Redact internal domains")


class SanitizeInputResponse(BaseModel):
    was_sanitized: bool
    sanitized_text: str
    redactions: List[Dict[str, str]]
    total_redactions: int


class FullGuardrailCheckRequest(BaseModel):
    text: str = Field(..., description="Text to run full guardrail check")
    auto_sanitize: bool = Field(default=False, description="Auto-sanitize if violations found")


class FullGuardrailCheckResponse(BaseModel):
    is_safe: bool
    validation_result: ValidateInputResponse
    attack_result: DetectAttackResponse
    sanitization_result: Optional[SanitizeInputResponse] = None
    overall_risk_score: int
    recommendation: str

