import re
from typing import Dict, List, Tuple
from .patterns import SecurityPatterns


class SanitizationResult:
    def __init__(self, original_text: str):
        self.original_text = original_text
        self.sanitized_text = original_text
        self.redactions: List[Dict[str, str]] = []
        self.was_sanitized = False
    
    @property
    def total_redactions(self) -> int:
        return len(self.redactions)
    
    def add_redaction(self, category: str, original: str, redacted: str):
        self.was_sanitized = True
        self.redactions.append({
            "category": category,
            "original_length": len(original),
            "redacted_as": redacted
        })
        self.sanitized_text = self.sanitized_text.replace(original, redacted)
    
    def to_dict(self) -> Dict:
        return {
            "was_sanitized": self.was_sanitized,
            "sanitized_text": self.sanitized_text,
            "redactions": self.redactions,
            "total_redactions": self.total_redactions
        }


class InputSanitizer:
    def __init__(self):
        self.secret_patterns = SecurityPatterns.get_all_secret_patterns()
        self.ip_patterns = SecurityPatterns.get_all_ip_patterns()
        self.pii_patterns = SecurityPatterns.get_all_pii_patterns()
        self.domain_patterns = SecurityPatterns.get_all_domain_patterns()
    
    def sanitize(self, text: str, redact_secrets: bool = True, 
                 redact_ips: bool = True, redact_pii: bool = False,
                 redact_domains: bool = True) -> SanitizationResult:
        result = SanitizationResult(text)
        
        if redact_secrets:
            self._redact_secrets(result)
        
        if redact_ips:
            self._redact_ips(result)
        
        if redact_pii:
            self._redact_pii(result)
        
        if redact_domains:
            self._redact_domains(result)
        
        return result
    
    def _redact_secrets(self, result: SanitizationResult):
        for name, pattern in self.secret_patterns.items():
            matches = list(pattern.finditer(result.sanitized_text))
            for match in reversed(matches):
                original = match.group(0)
                redacted = self._generate_redaction(name, "SECRET")
                result.add_redaction("secret", original, redacted)
    
    def _redact_ips(self, result: SanitizationResult):
        for name, pattern in self.ip_patterns.items():
            matches = list(pattern.finditer(result.sanitized_text))
            for match in reversed(matches):
                original = match.group(0)
                redacted = "[REDACTED_IP]"
                result.add_redaction("internal_ip", original, redacted)
    
    def _redact_pii(self, result: SanitizationResult):
        for name, pattern in self.pii_patterns.items():
            matches = list(pattern.finditer(result.sanitized_text))
            for match in reversed(matches):
                original = match.group(0)
                if name == "email":
                    redacted = "[REDACTED_EMAIL]"
                elif name == "ssn":
                    redacted = "[REDACTED_SSN]"
                elif name == "credit_card":
                    redacted = "[REDACTED_CC]"
                elif name == "phone_us":
                    redacted = "[REDACTED_PHONE]"
                else:
                    redacted = "[REDACTED_PII]"
                result.add_redaction("pii", original, redacted)
    
    def _redact_domains(self, result: SanitizationResult):
        for name, pattern in self.domain_patterns.items():
            matches = list(pattern.finditer(result.sanitized_text))
            for match in reversed(matches):
                original = match.group(0)
                redacted = "[REDACTED_DOMAIN]"
                result.add_redaction("internal_domain", original, redacted)
    
    def _generate_redaction(self, pattern_name: str, prefix: str) -> str:
        redaction_map = {
            "aws_access_key": "[REDACTED_AWS_KEY]",
            "aws_secret_key": "[REDACTED_AWS_SECRET]",
            "openai_key": "[REDACTED_OPENAI_KEY]",
            "anthropic_key": "[REDACTED_ANTHROPIC_KEY]",
            "github_token": "[REDACTED_GITHUB_TOKEN]",
            "jwt_token": "[REDACTED_JWT]",
            "stripe_key": "[REDACTED_STRIPE_KEY]",
            "slack_token": "[REDACTED_SLACK_TOKEN]",
            "private_key": "[REDACTED_PRIVATE_KEY]",
            "bearer_token": "[REDACTED_BEARER_TOKEN]",
        }
        return redaction_map.get(pattern_name, f"[REDACTED_{prefix}]")
    
    def quick_sanitize(self, text: str) -> str:
        result = self.sanitize(text)
        return result.sanitized_text

