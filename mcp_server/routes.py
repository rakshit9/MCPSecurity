from fastapi import APIRouter, HTTPException
from guardrails.input_validator import InputValidator
from guardrails.attack_detector import AttackDetector
from guardrails.sanitizer import InputSanitizer
from .schemas import (
    ValidateInputRequest, ValidateInputResponse,
    DetectAttackRequest, DetectAttackResponse,
    SanitizeInputRequest, SanitizeInputResponse,
    FullGuardrailCheckRequest, FullGuardrailCheckResponse
)

router = APIRouter(prefix="/guardrails", tags=["Input Guardrails"])

validator = InputValidator()
attack_detector = AttackDetector()
sanitizer = InputSanitizer()


@router.post("/validate", response_model=ValidateInputResponse)
async def validate_input(request: ValidateInputRequest):
    """
    Validate input for secrets, internal IPs, PII, and internal domains.
    Returns validation results with risk score.
    """
    result = validator.validate(request.text)
    return ValidateInputResponse(**result.to_dict())


@router.post("/detect-attack", response_model=DetectAttackResponse)
async def detect_attack(request: DetectAttackRequest):
    """
    Detect jailbreak attempts, prompt injection, and encoded payloads.
    Returns attack detection results with risk score.
    """
    result = attack_detector.detect(request.text)
    return DetectAttackResponse(**result.to_dict())


@router.post("/sanitize", response_model=SanitizeInputResponse)
async def sanitize_input(request: SanitizeInputRequest):
    """
    Sanitize input by redacting secrets, IPs, PII, and internal domains.
    Returns sanitized text with list of redactions.
    """
    result = sanitizer.sanitize(
        request.text,
        redact_secrets=request.redact_secrets,
        redact_ips=request.redact_ips,
        redact_pii=request.redact_pii,
        redact_domains=request.redact_domains
    )
    return SanitizeInputResponse(**result.to_dict())


@router.post("/full-check", response_model=FullGuardrailCheckResponse)
async def full_guardrail_check(request: FullGuardrailCheckRequest):
    """
    Run complete guardrail check: validation + attack detection + optional sanitization.
    Returns comprehensive security analysis.
    """
    validation_result = validator.validate(request.text)
    attack_result = attack_detector.detect(request.text)
    
    overall_risk_score = validation_result.risk_score + attack_result.risk_score
    is_safe = validation_result.is_safe and not attack_result.is_attack
    
    sanitization_result = None
    if request.auto_sanitize and not is_safe:
        san_result = sanitizer.sanitize(request.text)
        sanitization_result = SanitizeInputResponse(**san_result.to_dict())
    
    if overall_risk_score >= 80:
        recommendation = "BLOCK - Critical security risk detected"
    elif overall_risk_score >= 40:
        recommendation = "REVIEW - High risk, requires human review"
    elif overall_risk_score > 0:
        recommendation = "SANITIZE - Medium risk, sanitization recommended"
    else:
        recommendation = "ALLOW - Safe to proceed"
    
    return FullGuardrailCheckResponse(
        is_safe=is_safe,
        validation_result=ValidateInputResponse(**validation_result.to_dict()),
        attack_result=DetectAttackResponse(**attack_result.to_dict()),
        sanitization_result=sanitization_result,
        overall_risk_score=overall_risk_score,
        recommendation=recommendation
    )

